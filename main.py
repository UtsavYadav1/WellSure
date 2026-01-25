from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash, send_from_directory
import numpy as np
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import ast
from authlib.integrations.flask_client import OAuth

# Optional ML imports (not required for rules-based diagnosis)
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    ML_AVAILABLE = True
except ImportError:
    print("PyTorch/transformers not installed. ML predictions disabled. Rules-based diagnosis will work.")
    torch = None
    ML_AVAILABLE = False

import database  # our PostgreSQL connection helper
import utils     # Telemedicine utilities
from rules_engine import RulesEngine
import followup_questions  # UX Feature: Follow-up questions for clarification

# Load environment variables from .env file (if exists)
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'medimind_secure_secret_key')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

# Fix for Railway/Render proxy - ensures correct HTTPS URL generation
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Ensure Flask treats everything as HTTPS on Render
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SESSION_COOKIE_SECURE'] = True  # Cookies only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Required for OAuth callbacks

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Initialize Rules Engine
rules_engine = RulesEngine()

# ==========================================
# Load datasets
# ==========================================
sym_des = pd.read_csv(os.path.join(basedir, "symptoms_df_clean.csv"))
precautions = pd.read_csv(os.path.join(basedir, "precautions_clean.csv"))
workout = pd.read_csv(os.path.join(basedir, "workout_clean.csv"))
description = pd.read_csv(os.path.join(basedir, "description.csv"))
medications = pd.read_csv(os.path.join(basedir, 'medications_clean.csv'))
diets = pd.read_csv(os.path.join(basedir, "diet_clean.csv"))
doctors = pd.read_csv(os.path.join(basedir, "doctor_specialization_clean.csv"))  # disease → recommended specialist

# ==========================================
# Load BioBERT / DistilBERT Model and Tokenizer (OPTIONAL)
# ==========================================
MODEL_PATH = os.path.join(basedir, "medical_bert_model")
model = None
tokenizer = None
device = None

if ML_AVAILABLE:
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        print("Medical model loaded successfully.")
    except Exception as e:
        print(f"ML model not loaded (optional): {e}")
        model = None
        tokenizer = None
else:
    print("Running in rules-only mode (no ML model).")

# Load Label Encoder
le = None
try:
    with open(os.path.join(basedir, 'label_encoder.pkl'), 'rb') as f:
        le = pickle.load(f)
    print("Label encoder loaded.")
except Exception as e:
    print(f"Label encoder not loaded (optional for rules-based mode): {e}")


# ==========================================
# Helper: fetch description, precautions, meds, diet, workout, doctor
# ==========================================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    if not desc.empty:
        desc = " ".join([w for w in desc])
    else:
        desc = "No description available."

    pre = precautions[precautions['Disease'] == dis][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']
    ]
    if not pre.empty:
        pre = [col for col in pre.values]
    else:
        pre = [[]]

    med = medications[medications['Disease'] == dis]['Medication']
    if not med.empty:
        med_list = []
        for m in med.values:
            # Parse string list representations like "['item1', 'item2']"
            if isinstance(m, str) and m.startswith('[') and m.endswith(']'):
                import ast
                try:
                    parsed = ast.literal_eval(m)
                    if isinstance(parsed, list):
                        med_list.extend(parsed)
                    else:
                        med_list.append(m)
                except:
                    med_list.append(m)
            else:
                med_list.append(m)
        med = med_list
    else:
        med = []

    die = diets[diets['Disease'] == dis]['Diet']
    if not die.empty:
        die_list = []
        for d in die.values:
            # Parse string list representations like "['item1', 'item2']"
            if isinstance(d, str) and d.startswith('[') and d.endswith(']'):
                import ast
                try:
                    parsed = ast.literal_eval(d)
                    if isinstance(parsed, list):
                        die_list.extend(parsed)
                    else:
                        die_list.append(d)
                except:
                    die_list.append(d)
            else:
                die_list.append(d)
        die = die_list
    else:
        die = []

    wrkout = workout[workout['disease'] == dis]['workout']
    if not wrkout.empty:
        wrkout = [w for w in wrkout.values]
    else:
        wrkout = []

    doc = doctors[doctors['Disease'] == dis]['Doctor']
    if not doc.empty:
        doc = [d for d in doc.values]
    else:
        doc = []

    return desc, pre, med, die, wrkout, doc


def get_predicted_value(user_text):
    if model is None or tokenizer is None or le is None:
        return "System Error: Model not loaded"

    inputs = tokenizer(
        user_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()

    predicted_disease = le.inverse_transform([predicted_class_id])[0]
    return predicted_disease


# ==========================================
# PUBLIC ROUTES
# ==========================================

# Google Search Console Verification
@app.route('/googleb2777ecea8879182.html')
def google_verification():
    return send_from_directory('static', 'googleb2777ecea8879182.html')

# SEO: Serve sitemap and robots.txt at root
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route("/")
def index():
    # Fetch real stats from database for home page
    stats = {
        'users': 0,
        'doctors': 0,
        'diagnoses': 0,
        'appointments': 0
    }
    try:
        conn = database.get_db_connection()
        cursor = database.get_dict_cursor(conn)
        
        # Count all users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        stats['users'] = result['count'] if result else 0
        
        # Count doctors
        cursor.execute("SELECT COUNT(*) as count FROM doctors")
        result = cursor.fetchone()
        stats['doctors'] = result['count'] if result else 0
        
        # Count diagnoses
        cursor.execute("SELECT COUNT(*) as count FROM symptoms_logs")
        result = cursor.fetchone()
        stats['diagnoses'] = result['count'] if result else 0
        
        # Count appointments
        cursor.execute("SELECT COUNT(*) as count FROM appointments")
        result = cursor.fetchone()
        stats['appointments'] = result['count'] if result else 0
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Stats Error: {e}")
    
    return render_template("index.html", stats=stats)


@app.route('/check_symptoms')
def check_symptoms():
    if 'user_id' not in session:
        flash("Please login to use AI Diagnosis.", "info")
        return redirect(url_for('login'))
    
    # Check for pending symptoms from guest session
    pending_symptoms = session.pop('pending_symptoms', None)
    pending_age = session.pop('pending_age', None)
    pending_gender = session.pop('pending_gender', None)
    
    return render_template('check_symptoms.html', 
                           pending_symptoms=pending_symptoms,
                           pending_age=pending_age,
                           pending_gender=pending_gender)


@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form.get('symptoms')
    age = request.form.get('age')
    gender = request.form.get('gender')
    
    # Store symptoms in session for guests (will be processed after login)
    if 'user_id' not in session:
        if symptoms and symptoms != "Symptoms":
            session['pending_symptoms'] = symptoms
            session['pending_age'] = age
            session['pending_gender'] = gender
            flash("Please login to get your diagnosis results.", "info")
        return redirect(url_for('login'))


    symptoms = request.form.get('symptoms')
    if not symptoms or symptoms == "Symptoms":
        flash("Please describe your symptoms.", "warning")
        return redirect(url_for('check_symptoms'))
    else:
        try:
            # --- UX FEATURE: Process follow-up answers ---
            is_followup = request.form.get('is_followup') == 'true'
            newly_confirmed_symptoms = []  # Track symptoms confirmed via follow-up
            original_disease = request.form.get('original_disease', '')  # Track original disease for confidence capping
            
            if is_followup:
                # Use the new symptom keyword mapping for precise conversion
                answers = {k: v for k, v in request.form.items()}
                symptom_keywords, newly_confirmed_symptoms = followup_questions.get_symptom_keywords_from_answers(answers)
                
                # Append mapped symptom keywords to original symptoms
                if symptom_keywords:
                    symptoms = symptoms + ", " + symptom_keywords
            
            # --- OPTIONAL AGE/GENDER INPUTS ---
            age = request.form.get('age')
            gender = request.form.get('gender')
            
            # Convert age to int if provided, else None
            try:
                age = int(age) if age and age.strip() else None
            except (ValueError, TypeError):
                age = None
            
            # Normalize gender (None if not provided)
            gender = gender.strip().lower() if gender and gender.strip() else None
            
            # --- RULES ENGINE INTEGRATION ---
            analysis = rules_engine.run_analysis(symptoms)
            
            # --- POST-PROCESSING: Apply demographic context (OPTIONAL, NON-INVASIVE) ---
            # This ONLY adjusts confidence score, NEVER changes disease prediction
            analysis = rules_engine.apply_demographic_context(analysis, age=age, gender=gender)

            # 1. EMERGENCY HANDLING
            if analysis['emergency']:
                # --- START EMERGENCY LOGGING ---
                import os
                # 1. Define Emergency Variables
                predicted_disease = "EMERGENCY ALERT"
                dis_des = f"The system detected potential signs of a medical emergency: {analysis['reason']}. Please proceed to a hospital or consult the recommended specialist immediately."
                my_precautions = ["Do not self-medicate", "Call Emergency Services", "Go to the nearest hospital"]
                meds = ["Seek Incident Care"]
                my_diet = []
                workout = []
                
                # 2. Generate PDF
                # 2. Generate PDF
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                pdf_filename = f"report_{session.get('user_id', 'guest')}_{timestamp}.pdf"
                # Store relative in DB for portability
                pdf_path = os.path.join("static", "reports", pdf_filename)
                
                # Use absolute for generation
                abs_pdf_path = os.path.join(basedir, pdf_path)
                os.makedirs(os.path.dirname(abs_pdf_path), exist_ok=True)
                
                patient_name = session.get('name', 'Guest')
                utils.generate_pdf_report(
                    abs_pdf_path, patient_name, predicted_disease, symptoms, 
                    dis_des, meds, my_precautions, my_diet, workout, age=age, gender=gender
                )

                # 3. Log to DB
                log_id = None
                try:
                    conn = database.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO symptoms_logs 
                        (patient_id, symptoms_text, disease_predicted, description, medications, precautions, diets, workouts, pdf_path)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (session['user_id'], symptoms, predicted_disease, dis_des, str(meds), str(my_precautions), str(my_diet), str(workout), pdf_path)
                    )
                    log_id = cursor.fetchone()[0]
                    conn.commit()
                    cursor.close()
                    conn.close()
                except Exception as e:
                    print(f"Logging Error: {e}")
                # --- END EMERGENCY LOGGING ---

                flash(f"CRITICAL WARNING: {analysis['reason']} Immediate medical attention recommended.", "danger")
                return redirect(url_for('view_diagnosis', log_id=log_id))

            # 2. SAFE FALLBACK (General Physician)
            is_fallback = "General Physician Consultation" in analysis.get('allowed_diseases', [])
            
            if is_fallback:
                predicted_disease = "General Physician Consultation"
                dis_des = f"{analysis['reason']} Please provide more specific details or consult a General Physician for a broad checkup."
                my_precautions = ["Monitor symptoms", "Consult a doctor if symptoms persist"]
                meds = []
                rec_diet = []
                wrk = []
                my_doctor = ["General Physician"] 
                # Strict: Get from analysis, default LOW
                confidence_level = analysis.get('confidence_level', 'LOW')
            else:
                # 3. STANDARD PREDICTION
                raw_prediction = get_predicted_value(symptoms)
                
                if raw_prediction in analysis['allowed_diseases']:
                    predicted_disease = raw_prediction
                else:
                    predicted_disease = analysis['allowed_diseases'][0]

                dis_des, pre_arr, meds, rec_diet, wrk, my_doctor = helper(predicted_disease)
                
                # Strict: Get from analysis, default LOW
                confidence_level = analysis.get('confidence_level', 'LOW')

                my_precautions = []
                if len(pre_arr) > 0:
                    for i in pre_arr[0]:
                        my_precautions.append(i)

            session['last_predicted_disease'] = predicted_disease
            session['last_symptoms_text'] = symptoms

            import os
            # 1. Generate PDF
            # 1. Generate PDF
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_filename = f"report_{session.get('user_id', 'guest')}_{timestamp}.pdf"
            # Store relative in DB
            pdf_path = os.path.join("static", "reports", pdf_filename)
            pdf_url = url_for('static', filename=f'reports/{pdf_filename}')
            
            # Use absolute for generation
            abs_pdf_path = os.path.join(basedir, pdf_path)
            os.makedirs(os.path.dirname(abs_pdf_path), exist_ok=True)
            
            patient_name = session.get('name', 'Guest')
            utils.generate_pdf_report(
                abs_pdf_path, patient_name, predicted_disease, symptoms, 
                dis_des, meds, my_precautions, rec_diet, wrk, age=age, gender=gender
            )

            # 2. Log to DB
            log_id = None
            try:
                conn = database.get_db_connection()
                cursor = conn.cursor()
                # Get specialist for history
                specialist = my_doctor[0] if my_doctor and len(my_doctor) > 0 else 'General Physician'
                cursor.execute(
                    """
                    INSERT INTO symptoms_logs 
                    (patient_id, symptoms_text, disease_predicted, description, medications, precautions, diets, workouts, pdf_path, confidence_level, recommended_specialist, patient_age, patient_gender)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (session['user_id'], symptoms, predicted_disease, dis_des, str(meds), str(my_precautions), str(rec_diet), str(wrk), pdf_path, confidence_level, specialist, age, gender)
                )
                log_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Logging Error: {e}")
            
            # UX Feature: Get follow-up questions for LOW/MEDIUM confidence
            # Use the new should_show_followup function (HIGH confidence skips follow-up)
            show_followup = followup_questions.should_show_followup(confidence_level, is_followup)
            fq = followup_questions.get_followup_questions(predicted_disease) if show_followup else []
            
            # --- CONFIDENCE CAPPING: Follow-up can only improve by one level ---
            # If this is a follow-up request, cap at one level improvement
            if is_followup and original_disease:
                # Original was LOW -> can only reach MEDIUM at most
                # Original was MEDIUM -> can reach HIGH
                # This prevents LOW -> HIGH in a single follow-up
                original_confidence = request.form.get('original_confidence', 'LOW')
                if original_confidence == 'LOW' and confidence_level == 'HIGH':
                    confidence_level = 'MEDIUM'  # Cap to one level improvement
            
            # UX Feature: Explanation data for "Why this diagnosis?" panel
            explanation = {
                'matched_primary': analysis.get('matched_primary', []),
                'matched_supporting': analysis.get('matched_supporting', []),
                'missing_primary': analysis.get('missing_primary', []),
                'newly_confirmed': newly_confirmed_symptoms if is_followup else []  # Symptoms confirmed via follow-up
            }
            
            # Generate updated reason text if follow-up improved confidence
            reason_text = analysis.get('reason', '')
            if is_followup and newly_confirmed_symptoms:
                reason_text = f"Follow-up answers confirmed additional symptoms, improving diagnosis confidence."
            
            # POST/REDIRECT/GET Pattern: Redirect to view_diagnosis to prevent form resubmission on back button
            # Pass followup_result flag via URL parameter if this was a follow-up analysis
            redirect_url = url_for('view_diagnosis', log_id=log_id)
            if show_followup:
                redirect_url += '?show_followup=true'
            return redirect(redirect_url)

        except Exception as e:
            flash(f"Error during prediction: {e}", "danger")
            return redirect(url_for('check_symptoms'))


@app.route('/view_diagnosis/<int:log_id>')
def view_diagnosis(log_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM symptoms_logs WHERE id=%s AND patient_id=%s", (log_id, session['user_id']))
    log = cursor.fetchone()
    cursor.close()
    conn.close()

    if not log:
        flash("Diagnosis record not found.", "danger")
        return redirect(url_for('patient_dashboard'))

    def parse_list(data_str):
        try:
            return ast.literal_eval(data_str) if data_str else []
        except:
            return []

    predicted_disease = log['disease_predicted']
    
    # Helper to clean description
    dis_des = log['description']
    
    # Recalculate doctor safely
    if predicted_disease == "EMERGENCY ALERT":
        my_doctor = ["Emergency Specialist"]
        confidence_level = "HIGH"
        reason = "Emergency symptoms detected."
    elif predicted_disease == "General Physician Consultation":
        my_doctor = ["General Physician"]
        confidence_level = "LOW"
        reason = "Symptoms are non-specific."
    else:
        try:
            _, _, _, _, _, my_doctor = helper(predicted_disease)
            confidence_level = "MEDIUM" # Default for old logs
        except:
            my_doctor = ["General Physician"]
            confidence_level = "LOW"
            reason = "Prediction data unavailable."
    
    medications = parse_list(log['medications'])
    my_precautions = parse_list(log['precautions'])
    my_diet = parse_list(log['diets'])
    workout = parse_list(log['workouts'])
    
    pdf_path_rel = log['pdf_path']
    if pdf_path_rel:
        filename = os.path.basename(pdf_path_rel)
        pdf_report_url = url_for('static', filename=f'reports/{filename}')
    else:
        pdf_report_url = "#"

    # Logic moved above for safety
    if 'reason' not in locals():
        reason = ""
    
    # Handle show_followup query parameter (for PRG pattern from /predict)
    show_followup_param = request.args.get('show_followup', 'false').lower() == 'true'
    
    # Generate follow-up questions if needed
    fq = []
    show_followup = False
    explanation = {}
    
    if show_followup_param and confidence_level in ['LOW', 'MEDIUM']:
        # Check if we should show follow-up questions
        if followup_questions.should_show_followup(confidence_level):
            fq = followup_questions.get_followup_questions(predicted_disease)
            show_followup = True if fq else False
    
    # Run rules analysis to get explanation data
    if predicted_disease not in ["EMERGENCY ALERT", "General Physician Consultation"]:
        analysis = rules_engine.run_analysis(log['symptoms_text'])
        explanation = {
            'matched_primary': analysis.get('matched_primary', []),
            'matched_supporting': analysis.get('matched_supporting', []),
            'missing_primary': analysis.get('missing_primary', []),
            'newly_confirmed': []
        }
        # Use stored confidence if available, else use analysis
        if log.get('confidence_level'):
            confidence_level = log['confidence_level']
        else:
            confidence_level = analysis.get('confidence_level', 'MEDIUM')
        reason = analysis.get('reason', reason)

    return render_template('check_symptoms.html', 
        predicted_disease=predicted_disease, 
        dis_des=dis_des, 
        my_precautions=my_precautions, 
        medications=medications, 
        my_diet=my_diet, 
        workout=workout, 
        my_doctor=my_doctor, 
        user_input=log['symptoms_text'], 
        pdf_report_url=pdf_report_url, 
        log_id=log['id'],
        confidence_level=confidence_level,
        reason=reason,
        followup_questions=fq,
        show_followup=show_followup,
        explanation=explanation
    )


@app.route('/download_report/<int:log_id>')
def download_report(log_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)
    cursor.execute("SELECT pdf_path FROM symptoms_logs WHERE id=%s AND patient_id=%s", (log_id, session['user_id']))
    log = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if log and log['pdf_path']:
        from flask import send_file
        # Ensure absolute path for sending
        abs_path = os.path.join(basedir, log['pdf_path'])
        return send_file(abs_path, as_attachment=True)
    else:
        flash("Report not found or access denied.", "danger")
        return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


# ==========================================
# AUTHENTICATION ROUTES
# ==========================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = database.get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already registered!", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('signup'))
        # New Fields
        city = request.form['city']
        address = request.form['address']
        pincode = request.form['pincode']
        history = request.form.get('medical_history', '')
        
        # Geocode (OpenStreetMap)
        lat, lng = utils.geocode_address(address, city, pincode)

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, city, address, pincode, medical_history, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (name, email, hashed_password, city, address, pincode, history, lat, lng)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            
            # Log Activity
            utils.log_activity(user_id, 'patient', 'signup', f"New patient registered: {email}")
            
            flash("Registration Successful! Please Login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        role = request.form['role']  # 'patient', 'doctor', 'admin'

        conn = database.get_db_connection()
        cursor = database.get_dict_cursor(conn)

        user = None
        if role == 'patient':
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        elif role == 'doctor':
            cursor.execute("SELECT * FROM doctors WHERE email = %s", (email,))
            user = cursor.fetchone()
        elif role == 'admin':
            cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
            user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = role
            session['name'] = user.get('name', 'Admin')

            utils.log_activity(user['id'], role, 'login', "User logged in")

            flash("Login Successful!", "success")
            
            # Check for pending symptoms from guest session
            if role == 'patient' and session.get('pending_symptoms'):
                return redirect(url_for('check_symptoms'))
            
            if role == 'patient':
                return redirect(url_for('patient_dashboard'))
            elif role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        utils.log_activity(session['user_id'], session.get('role', 'unknown'), 'logout', "User logged out")
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


# ==========================================
# GOOGLE OAUTH ROUTES
# ==========================================
@app.route('/auth/google')
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash("Failed to get user info from Google.", "danger")
            return redirect(url_for('login'))
        
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        
        if not email:
            flash("No email provided by Google.", "danger")
            return redirect(url_for('login'))
        
        conn = database.get_db_connection()
        cursor = database.get_dict_cursor(conn)
        
        # Check if user exists in users table (patients)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            # Existing user - log them in
            session['user_id'] = user['id']
            session['role'] = 'patient'
            session['name'] = user['name']
            utils.log_activity(user['id'], 'patient', 'login', "Google OAuth login")
            flash(f"Welcome back, {user['name']}!", "success")
            cursor.close()
            conn.close()
            # Check for pending symptoms
            if session.get('pending_symptoms'):
                return redirect(url_for('check_symptoms'))
            return redirect(url_for('patient_dashboard'))
        else:
            # New user - create account and log them in
            try:
                # Generate a random password (user won't need it, they'll use Google)
                import secrets
                random_password = secrets.token_urlsafe(16)
                hashed_password = generate_password_hash(random_password)
                
                cursor.execute(
                    "INSERT INTO users (name, email, password, city, address, pincode) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (name, email, hashed_password, '', '', '')
                )
                user_id = cursor.fetchone()['id']
                conn.commit()
                
                session['user_id'] = user_id
                session['role'] = 'patient'
                session['name'] = name
                
                utils.log_activity(user_id, 'patient', 'signup', f"New user via Google OAuth: {email}")
                flash(f"Welcome to WellSure, {name}! Please complete your profile.", "success")
                cursor.close()
                conn.close()
                # Check for pending symptoms
                if session.get('pending_symptoms'):
                    return redirect(url_for('check_symptoms'))
                return redirect(url_for('patient_dashboard'))
            except Exception as e:
                conn.rollback()
                flash(f"Error creating account: {e}", "danger")
                cursor.close()
                conn.close()
                return redirect(url_for('signup'))
                
    except Exception as e:
        flash(f"Google login failed: {e}", "danger")
        return redirect(url_for('login'))


# ==========================================
# PATIENT MODULE ROUTES
# ==========================================
@app.route('/patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))
        
    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    # READ-ONLY: Fetch health history (does NOT influence predictions)
    cursor.execute("""
        SELECT sl.id, sl.symptoms_text, sl.disease_predicted, sl.created_at,
               COALESCE(sl.confidence_level, 'N/A') as confidence_level,
               COALESCE(sl.recommended_specialist, 'General Physician') as specialist
        FROM symptoms_logs sl
        WHERE sl.patient_id = %s
        ORDER BY sl.created_at DESC
        LIMIT 10
    """, (session['user_id'],))
    health_history = cursor.fetchall()
    
    # READ-ONLY: Fetch completed appointments with prescriptions
    cursor.execute("""
        SELECT a.id, a.appointment_date, a.status, a.disease_predicted,
               d.name as doctor_name, d.specialization,
               a.prescription_path
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.patient_id = %s AND a.status = 'Completed'
        ORDER BY a.appointment_date DESC
        LIMIT 10
    """, (session['user_id'],))
    completed_appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('patient_dashboard.html', user=user, 
                           health_history=health_history,
                           completed_appointments=completed_appointments)


@app.route('/update_patient_profile', methods=['POST'])
def update_patient_profile():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    user_id = session['user_id']
    name = request.form['name']
    city = request.form['city']
    address = request.form['address']
    pincode = request.form['pincode']
    history = request.form.get('medical_history', '')
    
    # New: Age and Gender
    age = request.form.get('age')
    gender = request.form.get('gender')
    
    # Convert age to int if provided
    try:
        age = int(age) if age and age.strip() else None
    except (ValueError, TypeError):
        age = None

    # Re-geocode
    lat, lng = utils.geocode_address(address, city, pincode)

    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        if lat and lng:
             cursor.execute(
                "UPDATE users SET name=%s, city=%s, address=%s, pincode=%s, medical_history=%s, age=%s, gender=%s, lat=%s, lng=%s WHERE id=%s",
                (name, city, address, pincode, history, age, gender, lat, lng, user_id)
            )
        else:
            # Keep old coords if geocode fails
            cursor.execute(
                "UPDATE users SET name=%s, city=%s, address=%s, pincode=%s, medical_history=%s, age=%s, gender=%s WHERE id=%s",
                (name, city, address, pincode, history, age, gender, user_id)
            )
        conn.commit()
        session['name'] = name # Update session name
        flash("Profile Updated Successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('patient_dashboard'))


@app.route('/view_doctors')
def view_doctors():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    specialization = request.args.get('specialization')
    log_id = request.args.get('log_id')
    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)

    if specialization:
        cursor.execute("SELECT * FROM doctors WHERE specialization = %s", (specialization,))
    else:
        cursor.execute("SELECT * FROM doctors")
    doctors_list = cursor.fetchall()

    cursor.execute("SELECT name FROM specializations ORDER BY name ASC")
    specs = [row['name'] for row in cursor.fetchall()]

    patient_coords = None
    address_incomplete = False
    if 'user_id' in session and session.get('role') == 'patient':
        cursor.execute("SELECT lat, lng, address, city, pincode FROM users WHERE id=%s", (session['user_id'],))
        patient = cursor.fetchone()
        if patient:
            # Check if address is incomplete
            if not patient.get('address') or not patient.get('city') or not patient.get('pincode'):
                address_incomplete = True
            if patient.get('lat') and patient.get('lng'):
                patient_coords = {'lat': patient['lat'], 'lng': patient['lng']}
                # Use Utility
                utils.process_doctors_data(doctors_list, patient['lat'], patient['lng'])

    # Normalize time fields for JSON serialization compatibility
    # Normalize fields for JSON serialization compatibility (Decimal, Time, Date)
    from decimal import Decimal
    from datetime import date, datetime, timedelta

    for doc in doctors_list:
        for k, v in doc.items():
            if isinstance(v, Decimal):
                doc[k] = float(v)
            elif isinstance(v, (date, datetime)):
                doc[k] = str(v)
            elif isinstance(v, timedelta):
                # Handle timedelta (already partly handled but ensuring safety)
                seconds = int(v.total_seconds())
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                doc[k] = f"{hours:02}:{minutes:02}"
                
        # Existing logic for string time format fallback
        for field in ['available_start_time', 'available_end_time']:
             val = doc.get(field)
             if isinstance(val, str) and len(val.split(':')) == 3:
                doc[field] = val[:5]

    cursor.close()
    conn.close()

    return render_template(
        'view_doctors.html',
        doctors=doctors_list,
        specializations=specs,
        patient_coords=patient_coords,
        address_incomplete=address_incomplete,
        log_id=log_id
    )


@app.route('/book_appointment/<int:doctor_id>')
def book_appointment(doctor_id):
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if not doctor:
        flash("Doctor not found", "danger")
        return redirect(url_for('view_doctors'))

    return render_template(
        'book_appointment.html',
        doctor=doctor,
        get_today_date=lambda: datetime.today().strftime('%Y-%m-%d')
    )


@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    doctor_id = request.form['doctor_id']
    appt_date = request.form['appointment_date']
    appt_time = request.form['appointment_time']
    doctor_spec = request.form['doctor_specialization']
    symptom_log_id = request.form.get('symptom_log_id') or None
    payment_mode = request.form.get('payment_mode', 'at_clinic')
    patient_id = session['user_id']

    disease = session.get('last_predicted_disease', 'General Checkup')

    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)

    # 1. Double Booking Check
    cursor.execute(
        "SELECT * FROM appointments WHERE doctor_id=%s AND appointment_date=%s AND appointment_time=%s AND status != 'Cancelled'",
        (doctor_id, appt_date, appt_time)
    )
    conflict = cursor.fetchone()
    if conflict:
        flash("Doctor is unavailable at this time. Please choose another slot.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for('book_appointment', doctor_id=doctor_id, log_id=symptom_log_id))

    try:
        # 2. Book Appointment with payment mode
        cursor.execute(
            """
            INSERT INTO appointments
            (patient_id, doctor_id, disease_predicted, doctor_specialization,
             appointment_date, appointment_time, status, symptom_log_id, payment_mode)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending', %s, %s)
            """,
            (patient_id, doctor_id, disease, doctor_spec, appt_date, appt_time, symptom_log_id, payment_mode)
        )
        conn.commit()
        
        # Log Activity
        utils.log_activity(patient_id, 'patient', 'book_appointment', f"Booked Dr. ID {doctor_id} on {appt_date} at {appt_time}")

        return render_template('appointment_confirmed.html')
    except Exception as e:
        conn.rollback()
        flash(f"Error booking: {e}", "danger")
        return redirect(url_for('patient_dashboard'))
    finally:
        cursor.close()
        conn.close()


@app.route('/my_appointments')
def my_appointments():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    patient_id = session['user_id']
    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)

    query = """
        SELECT a.*, d.name AS doctor_name, d.address AS doctor_address, 
               d.city AS doctor_city, d.specialization AS speciality,
               d.fees AS doctor_fees
        FROM appointments a 
        JOIN doctors d ON a.doctor_id = d.id 
        WHERE a.patient_id = %s 
        ORDER BY a.appointment_date DESC
    """
    cursor.execute(query, (patient_id,))
    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('my_appointments.html', appointments=appointments)


# ==========================================
# DOCTOR MODULE ROUTES
# ==========================================
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))

    doctor_id = session['user_id']
    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()

    # Get appointments
    cursor.execute("""
        SELECT a.*, u.name as patient_name, u.age, u.gender
        FROM appointments a
        JOIN users u ON a.patient_id = u.id
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_date DESC, a.appointment_time ASC
    """, (doctor_id,))
    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('doctor_dashboard.html', doctor=doctor, appointments=appointments)


@app.route('/update_doctor_profile', methods=['POST'])
def update_doctor_profile():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))

    doctor_id = session['user_id']
    name = request.form['name']
    specialization = request.form['specialization']
    fees = request.form['fees']
    description = request.form['description']
    city = request.form['city']
    address = request.form['address']
    pincode = request.form['pincode']
    
    # Manage Meeting Link
    meeting_link = request.form.get('meeting_link', '').strip()
    
    # Re-geocode
    lat, lng = utils.geocode_address(address, city, pincode)

    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        if lat and lng:
            cursor.execute(
                "UPDATE doctors SET name=%s, specialization=%s, fees=%s, description=%s, city=%s, address=%s, pincode=%s, lat=%s, lng=%s, default_meeting_link=%s WHERE id=%s",
                (name, specialization, fees, description, city, address, pincode, lat, lng, meeting_link, doctor_id)
            )
        else:
            cursor.execute(
                "UPDATE doctors SET name=%s, specialization=%s, fees=%s, description=%s, city=%s, address=%s, pincode=%s, default_meeting_link=%s WHERE id=%s",
                (name, specialization, fees, description, city, address, pincode, meeting_link, doctor_id)
            )
        conn.commit()
        utils.log_activity(doctor_id, 'doctor', 'update_profile', "Updated profile details")
        flash("Profile Updated", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Update failed: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('doctor_dashboard'))


@app.route('/upload_prescription/<int:appt_id>', methods=['POST'])
def upload_prescription(appt_id):
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))

    file = request.files.get('prescription')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"presc_{appt_id}_{timestamp}.pdf"
        
        # Determine path (static/prescriptions)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'prescriptions')
        os.makedirs(save_path, exist_ok=True)
        
        full_path = os.path.join(save_path, unique_filename)
        file.save(full_path)
        
        # Store relative path in DB
        db_path = os.path.join('static', 'uploads', 'prescriptions', unique_filename)

        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE appointments SET prescription_path=%s, status='Completed' WHERE id=%s",
                (db_path, appt_id)
            )
            conn.commit()
            utils.log_activity(session['user_id'], 'doctor', 'upload_prescription', f"Uploaded for Appt ID {appt_id}")
            flash("Prescription uploaded and appointment marked completed.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('doctor_dashboard'))


@app.route('/complete_appointment/<int:appt_id>')
def complete_appointment(appt_id):
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))
        
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE appointments SET status='Completed' WHERE id=%s", (appt_id,))
        conn.commit()
        flash("Appointment marked as completed.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('doctor_dashboard'))


# ==========================================
# ADMIN MODULE ROUTES
# ==========================================
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = database.get_db_connection()
    cursor = database.get_dict_cursor(conn)
    cursor.execute("SELECT * FROM doctors ORDER BY id DESC")
    doctors = cursor.fetchall()
    
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    patients = cursor.fetchall()

    cursor.execute("SELECT * FROM specializations ORDER BY name ASC")
    specializations = cursor.fetchall()
    
    # Activity Logs
    cursor.execute("SELECT * FROM activity_logs ORDER BY created_at DESC LIMIT 50")
    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', doctors=doctors, patients=patients, 
                           specializations=specializations, logs=logs)


@app.route('/admin/add_doctor', methods=['POST'])
def add_doctor():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    specialization = request.form['specialization']
    fees = request.form['fees']
    description = request.form.get('description', '')
    city = request.form['city']
    address = request.form['address']
    pincode = request.form['pincode']

    hashed_password = generate_password_hash(password)
    
    lat, lng = utils.geocode_address(address, city, pincode)

    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO doctors (name, email, password, specialization, fees, description, city, address, pincode, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (name, email, hashed_password, specialization, fees, description, city, address, pincode, lat, lng)
        )
        doctor_id = cursor.fetchone()[0]
        conn.commit()
        utils.log_activity(session['user_id'], 'admin', 'add_doctor', f"Added doctor {name} ({specialization})")
        flash("Doctor Added Successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error adding doctor: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        # Get doctor name for log
        cursor.execute("SELECT name FROM doctors WHERE id=%s", (doctor_id,))
        res = cursor.fetchone()
        doc_name = res[0] if res else "Unknown"

        cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
        conn.commit()
        utils.log_activity(session['user_id'], 'admin', 'delete_doctor', f"Deleted doctor {doc_name} (ID: {doctor_id})")
        flash("Doctor Deleted", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting doctor: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/add_specialization', methods=['POST'])
def add_specialization():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    name = request.form['name'].strip()
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO specializations (name) VALUES (%s) RETURNING id", (name,))
        conn.commit()
        flash("Specialization Added", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('admin_dashboard'))


# ==========================================
# FEEDBACK ROUTES
# ==========================================
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))
        
    doctor_id = request.form['doctor_id']
    appt_id = request.form['appointment_id']
    rating = request.form['rating']
    review = request.form['review']
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO doctor_feedback (appointment_id, doctor_id, patient_id, rating, review) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (appt_id, doctor_id, session['user_id'], rating, review)
        )
        conn.commit()
        
        # Update Doctor Rating Aggregates
        cursor.execute("""
            UPDATE doctors 
            SET rating_count = rating_count + 1,
                rating_average = ((rating_average * rating_count) + %s) / (rating_count + 1)
            WHERE id = %s
        """, (float(rating), doctor_id))
        conn.commit()
        
        utils.log_activity(session['user_id'], 'patient', 'submit_feedback', f"Rated Dr. ID {doctor_id} with {rating} stars")
        flash("Feedback submitted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('patient_dashboard'))


# SEO Routes
@app.route('/robots.txt')
def robots_txt():
    content = "User-agent: *\nDisallow:\nSitemap: https://wellsure-an0b.onrender.com/sitemap.xml"
    return Response(content, mimetype="text/plain")

@app.route('/sitemap.xml')
def sitemap_xml():
    base_url = "https://wellsure-an0b.onrender.com"
    pages = [
        '/', '/about', '/check_symptoms', '/login', '/signup', 
        '/view_doctors', '/contact'
    ]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{base_url}{page}</loc>\n'
        xml_content += '    <changefreq>daily</changefreq>\n'
        xml_content += '    <priority>0.8</priority>\n'
        xml_content += '  </url>\n'
        
    xml_content += '</urlset>'
    return Response(xml_content, mimetype="application/xml")

# ==========================================
# MAIN ENTRY POINT
# ==========================================
if __name__ == "__main__":
    app.run(debug=True, port=8000)



