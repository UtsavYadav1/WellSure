import pandas as pd
import numpy as np

# Master Disease List from description.csv (preserving exact spelling)
DISEASES = [
    # Dermatology
    "Fungal infection", "Acne", "Psoriasis", "Impetigo", "Chicken pox",
    # Allergies / Immune
    "Allergy", "Drug Reaction", "AIDS",
    # Gastroenterology
    "GERD", "Chronic cholestasis", "Peptic ulcer disease", "Gastroenteritis", "Jaundice", 
    "Dimorphic hemmorhoids(piles)", "hepatitis A", "Hepatitis B", "Hepatitis C", "Hepatitis D", 
    "Hepatitis E", "Alcoholic hepatitis",
    # Endocrinology
    "Diabetes", "Hypothyroidism", "Hyperthyroidism", "Hypoglycemia",
    # Respiratory
    "Bronchial Asthma", "Common Cold", "Pneumonia", "Tuberculosis",
    # Cardiology
    "Hypertension", "Heart attack", "Varicose veins",
    # Neurology
    "Migraine", "Paralysis (brain hemorrhage)", "(vertigo) Paroymsal Positional Vertigo",
    # Infectious / Vector-borne
    "Malaria", "Dengue", "Typhoid",
    # Orthopedics / Rheumatology
    "Cervical spondylosis", "Osteoarthristis", "Arthritis",
    # Urology
    "Urinary tract infection"
]

# Data Dictionary
DATA = {
    # --- DERMATOLOGY ---
    "Fungal infection": {
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches", "redness_of_skin", "ring_shaped_rash", "itchy_scalp", "dry_skin", "blisters_on_skin"], # Removed generic 'burning'
        "medications": ["Antifungal Creams", "Fluconazole", "Ketoconazole", "Clotrimazole", "Terbinafine", "Itraconazole", "Miconazole"],
        "diet": ["Probiotic-rich foods", "Garlic", "Ginger", "Coconut oil", "Low-sugar diet", "Apple cider vinegar", "Avoid refined carbs", "Hydration"],
        "precautions": ["Keep skin dry and clean", "Avoid sharing personal items", "Wear loose cotton clothes", "Change socks daily", "Dry skin thoroughly after bath", "Use antifungal powder", "Wash clothes in hot water", "Avoid tight footwear"],
        "workout": ["Light walking", "Yoga for stress relief", "Breathing exercises", "Avoid excessive sweating exercises", "Stretching"],
        "doctor": "Dermatologist"
    },
    "Acne": {
        "symptoms": ["skin_rash", "pus_filled_pimples", "blackheads", "scurring", "whiteheads", "cysts", "nodules", "inflammation", "oily_skin"],
        "medications": ["Benzoyl peroxide", "Salicylic acid", "Retinoids", "Antibiotics (topical/oral)", "Isotretinoin", "Hormonal therapy", "Chemical peels"],
        "diet": ["Low-glycemic index diet", "Zinc-rich foods", "Omega-3 fatty acids", "Antioxidants", "Probiotics", "Hydration", "Green tea", "Avoid dairy (if trigger)"],
        "precautions": ["Keep face clean", "Don't pop pimples", "Use non-comedogenic products", "Remove makeup", "Shower after sweat", "Sun protection", "Avoid touching face", "Manage stress"],
        "workout": ["Exercise regularly", "Shower immediately after", "Wear loose clothing"],
        "doctor": "Dermatologist"
    },
    "Psoriasis": {
        "symptoms": ["skin_rash", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "red_patches_of_skin", "dry_cracked_skin", "silvery_scales", "cyclic_rashes"], # Removed joint_pain (make it distinct from arthritis)
        "medications": ["Corticosteroids", "Vitamin D analogues", "Retinoids", "Calcineurin inhibitors", "Salicylic acid", "Biologics", "Methotrexate", "Photo therapy"],
        "diet": ["Anti-inflammatory diet", "Gluten-free (if sensitive)", "Omega-3s", "Antioxidants", "Weight management", "Avoid alcohol", "Turmeric", "Vitamin D"],
        "precautions": ["Moisturize daily", "Avoid triggers (stress, injury)", "Sun exposure (controlled)", "Quit smoking", "Manage stress", "Avoid scratching", "Warm baths", "Use humidifiers"],
        "workout": ["Swimming", "Walking", "Yoga", "Stretching", "Low impact"],
        "doctor": "Dermatologist"
    },
    "Impetigo": {
        "symptoms": ["skin_rash", "blister", "red_sore_around_nose", "yellow_crust_ooze", "itchy_rash", "fluid_filled_sores", "painful_sores", "honey_colored_crusts"], # Removed high_fever (usually mild)
        "medications": ["Topical antibiotics (Mupirocin)", "Oral antibiotics", "Antiseptic washes", "Pain relievers"],
        "diet": ["High-protein for healing", "Vitamin C and A", "Zinc", "Hydration", "Fruits and vegetables", "Whole foods"],
        "precautions": ["Keep hygiene", "Wash hands", "Clip fingernails", "Don't share towels/clothes", "Wash linens in hot water", "Keep sores covered", "Stay home", "Disinfect toys"],
        "workout": ["Rest", "Avoid contact sports", "No swimming"],
        "doctor": "Dermatologist"
    },
    "Chicken pox": {
        "symptoms": ["itching", "skin_rash", "fatigue", "high_fever", "headache", "small_fluid_filled_blisters", "scabs", "crusts", "red_spots"],
        "medications": ["Antihistamines (for itch)", "Paracetamol (for fever)", "Acyclovir (antiviral)", "Calamine lotion", "Oatmeal baths", "Topical ointments"],
        "diet": ["Soft foods", "Cool foods (popsycles)", "Bland diet", "Hydration", "Avoid acidic/spicy foods", "Smoothies", "Mashed potatoes", "Yogurt"],
        "precautions": ["Isolate to prevent spread", "Trim fingernails", "Don't scratch blisters", "Wear loose clothing", "Daily bath with lukewarm water", "Hand hygiene", "Vaccination", "Monitor for secondary infections"],
        "workout": ["Rest", "No exercise"],
        "doctor": "General Physician"
    },

    # --- ALLERGIES / IMMUNE ---
    "Allergy": {
        "symptoms": ["continuous_sneezing", "watering_from_eyes", "itchy_eyes", "red_eyes", "swollen_eyes", "runny_nose", "skin_rash", "hives", "itchy_throat", "shortness_of_breath", "wheezing"], # Removed chills, shivering, headache
        "medications": ["Antihistamines", "Cetirizine", "Loratadine", "Fexofenadine", "Decongestants", "Nasal Corticosteroids", "Eye Drops", "Epinephrine (for severe cases)"],
        "diet": ["Anti-inflammatory foods", "Local honey", "Probiotics", "Vitamin C rich foods", "Omega-3 fatty acids", "Ginger tea", "Turmeric milk", "Avoid known allergens"],
        "precautions": ["Identify and avoid triggers", "Keep windows closed during pollen season", "Wear a mask in dusty areas", "Wash hands frequently", "Use hypoallergenic bedding", "Shower after being outdoors", "Avoid touching eyes", "Carry allergy medication"],
        "workout": ["Indoor yoga", "Light cardio indoors", "Breathing exercises (Pranayama)", "Avoid outdoor running during high pollen"],
        "doctor": "Allergist/Immunologist"
    },
    "Drug Reaction": {
        "symptoms": ["itching", "skin_rash", "stomach_pain", "hives", "swelling_of_lips", "swelling_of_face", "wheezing", "shortness_of_breath", "redness_of_skin"],
        "medications": ["Antihistamines", "Corticosteroids", "Epinephrine (for anaphylaxis)", "Calamine lotion", "Oral steroids", "Discontinue offending drug"],
        "diet": ["Bland diet", "Clear fluids", "Hydrating foods", "Anti-inflammatory foods", "Avoid spicy foods", "Avoid processed foods"],
        "precautions": ["Stop taking the suspected drug immediately", "Seek medical attention if severe", "Keep a record of drug allergies", "Wear medical alert bracelet", "Inform doctors about allergies", "Avoid self-medication", "Stay hydrated", "Monitor vital signs"],
        "workout": ["Rest mainly", "Very light walking if mild", "Breathing exercises"],
        "doctor": "Allergist/Immunologist"
    },
    "AIDS": {
        "symptoms": ["muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts", "fatigue", "swollen_lymph_nodes", "weight_loss", "chronic_diarrhea", "opportunistic_infections"],
        "medications": ["Antiretroviral Therapy (ART)", "Nucleoside Reverse Transcriptase Inhibitors", "Protease Inhibitors", "Integrase Inhibitors", "Entry Inhibitors", "Antibiotics for secondary infections"],
        "diet": ["High-protein diet", "High-calorie foods", "Plenty of fruits and vegetables", "Whole grains", "Healthy fats", "Food safety (avoid raw eggs/meat)", "Multivitamins", "Hydration"],
        "precautions": ["Practice safe sex", "Adhere strictly to ART (medication)", "Avoid sharing needles", "Regular health check-ups", "Hygiene maintenance", "Avoid raw or undercooked food", "Vaccinations (as advised)", "Stress management"],
        "workout": ["Moderate resistance training", "Aerobic exercise", "Yoga for flexibility", "Meditation", "Physician-approved routine"],
        "doctor": "Infectious Disease Specialist"
    },

    # --- GASTROENTEROLOGY ---
    "GERD": {
        "symptoms": ["stomach_pain", "acidity", "ulcers_on_tongue", "regurgitation_of_food", "dysphagia", "heartburn", "burning_sensation_in_chest", "bitter_taste", "belching"], # Removed chest_pain to avoid heart attack confusion, kept burning_sensation
        "medications": ["Antacids", "H2 Blockers", "Proton Pump Inhibitors (PPIs)", "Omeprazole", "Ranitidine", "Famotidine", "Lifestyle changes", "Alginate drugs"],
        "diet": ["Non-acidic foods", "Oatmeal", "Ginger", "Green vegetables", "Lean proteins", "Egg whites", "Bananas", "Melon", "Avoid spicy foods", "Small frequent meals"],
        "precautions": ["Avoid lying down after eating", "Elevate head while sleeping", "Lose excess weight", "Avoid alcohol and smoking", "Avoid triggering foods", "Eat slowly", "Wear loose clothing", "Don't eat late at night"],
        "workout": ["Walking", "Light jogging", "Upright stationary biking", "Avoid high-impact jumping", "Avoid crunches/sit-ups"],
        "doctor": "Gastroenterologist"
    },
    "Chronic cholestasis": {
        "symptoms": ["itching", "vomiting", "yellowish_skin", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes", "pale_stools"],
        "medications": ["Ursodeoxycholic acid", "Cholestyramine", "Rifampicin", "Naltrexone", "Vitamin K supplements", "Vitamin D supplements", "Antihistamines for itch"],
        "diet": ["Low-fat diet", "High-fiber foods", "Lean proteins", "Fruits and vegetables", "Whole grains", "Avoiding alcohol", "Plenty of water", "Small frequent meals"],
        "precautions": ["Avoid alcohol completely", "Maintain healthy weight", "Follow prescribed medication strictly", "Regular liver function tests", "Avoid hepatotoxic drugs", "Stay hydrated", "Manage stress", "Monitor symptoms"],
        "workout": ["Light walking", "Gentle stretching", "Restorative yoga", "Avoid strenuous activities"],
        "doctor": "Gastroenterologist"
    },
    "Peptic ulcer disease": {
        "symptoms": ["vomiting", "abdominal_pain", "indigestion", "burning_stomach_pain", "feeling_full", "bloating", "belching", "blood_in_vomit", "dark_stool"],
        "medications": ["Proton Pump Inhibitors (PPIs)", "Antibiotics (for H. pylori)", "H2 Blockers", "Antacids", "Cytoprotective agents", "Bismuth subsalicylate"],
        "diet": ["Probiotic-rich foods", "Fiber-rich foods", "Vitamin A rich foods", "Flavonoid-rich foods", "Avoid spicy foods", "Avoid excessive caffeine", "Avoid alcohol", "Cooked vegetables"],
        "precautions": ["Avoid NSAIDs (painkillers)", "Quit smoking", "Limit alcohol intake", "Manage stress", "Eat small frequent meals", "Don't eat right before bed", "Chew food thoroughly", "Follow hygiene to avoid H. pylori"],
        "workout": ["Walking", "Yoga", "Tai Chi", "Avoid intense core workouts", "Stress-reducing exercises"],
        "doctor": "Gastroenterologist"
    },
    "Gastroenteritis": {
        "symptoms": ["vomiting", "diarrhea", "stomach_cramps", "nausea", "fever", "dehydration", "abdominal_pain", "bloating"],
        "medications": ["Oral Rehydration Salts (ORS)", "Antiemetics", "Probiotics", "Zinc supplements", "Antibiotics (if bacterial)", "Antidiarrheals (use caution)", "Paracetamol for fever"],
        "diet": ["BRAT diet (Bananas, Rice, Applesauce, Toast)", "Clear broths", "Crackers", "Herbal tea", "Avoid dairy", "Avoid fatty/spicy foods", "Electrolyte drinks", "Boiled potatoes"],
        "precautions": ["Frequent hand washing", "Food hygiene", "Drink safe/boiled water", "Avoid sharing personal items", "Rest as much as possible", "Isolate to prevent spread", "Disinfect surfaces", "Hydrate frequently"],
        "workout": ["Complete rest", "No exercise until recovered"],
        "doctor": "Gastroenterologist"
    },
    "Jaundice": {
        "symptoms": ["itching", "yellowish_skin", "dark_urine", "pale_stool", "abdominal_pain", "fatigue", "vomiting", "yellowing_of_eyes"],
        "medications": ["Antivirals (if viral)", "Steroids", "Urso", "Cholestyramine (for itch)", "Treating underlying cause", "IV fluids"],
        "diet": ["High-carb diet", "Low-fat diet", "Moderate protein", "Hydration", "Fruits and vegetables", "Avoid alcohol", "Avoid raw fish", "Coffee (in moderation may be protective)"],
        "precautions": ["Rest completely", "Avoid alcohol", "Avoid hepatotoxic medications", "Hygiene", "Vaccination (Hep A, B)", "Drink clean water", "Safe sex practices", "Regular blood tests"],
        "workout": ["Complete rest", "Very light walking (only during recovery)"],
        "doctor": "Gastroenterologist"
    },
    "Dimorphic hemmorhoids(piles)": {
        "symptoms": ["constipation", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "itching", "swelling_in_anal_region", "lump_near_anus"],
        "medications": ["Stool softeners", "Topical creams (Hydrocortisone)", "Pain relievers", "Vasoconstrictors", "Fiber supplements", "Sitz baths"],
        "diet": ["High-fiber diet", "Whole grains", "Legumes", "Fruits (prunes, pears)", "Vegetables", "Plenty of water", "Avoid spicy foods", "Probiotics"],
        "precautions": ["Avoid straining", "Don't delay bowel movement", "Exercise regularly", "Sitz baths", "Avoid prolonged sitting", "Cleanliness", "Weight management", "Manage constipation"],
        "workout": ["Walking", "Kegel exercises", "Yoga", "Avoid heavy lifting", "Avoid cycling"],
        "doctor": "Proctologist/Surgeon"
    },
    "hepatitis A": {
        "symptoms": ["joint_pain", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "fever", "fatigue", "clay_colored_stools"],
        "medications": ["Supportive care", "Rest", "IV fluids", "Anti-nausea medication", "Avoid liver-stressing drugs"],
        "diet": ["Small frequent meals", "High-calorie foods", "Fruit juices", "Avoid alcohol", "Low-fat diet", "Hydration", "Soft foods", "Ginger tea"],
        "precautions": ["Hand washing", "Safe food and water", "Vaccination", "Separate bathroom use if possible", "Disinfect surfaces", "Avoid sexual contact during infection", "Rest", "Personal hygiene"],
        "workout": ["Rest", "Light activities only as tolerated"],
        "doctor": "Hepatologist"
    },
    "Hepatitis B": {
        "symptoms": ["fatigue", "yellowish_skin", "dark_urine", "abdominal_pain", "loss_of_appetite", "nausea", "clay_colored_stools", "joint_pain"],
        "medications": ["Antiviral medications (Entecavir, Tenofovir)", "Interferon injections", "Liver transplant (severe)", "Supportive care", "Vitamin supplements"],
        "diet": ["Balanced diet", "Fruits and vegetables", "Whole grains", "Lean proteins", "Avoid alcohol", "Limit processed foods", "Low-salt", "Hydration"],
        "precautions": ["Vaccination", "Safe sex", "Avoid sharing needles/razors", "Cover open cuts", "Regular check-ups", "Screening for liver cancer", "Avoid alcohol", "Inform partners"],
        "workout": ["Moderate exercise (walking)", "Avoid intense training during flares", "Yoga", "Listen to body"],
        "doctor": "Hepatologist"
    },
    "Hepatitis C": {
        "symptoms": ["fatigue", "yellowish_skin", "nausea", "loss_of_appetite", "dark_urine", "clay_colored_stool", "fever", "abdominal_pain"],
        "medications": ["Direct-acting antivirals (DAAs)", "Sofosbuvir", "Ledipasvir", "Velpatasvir", "Ribavirin", "Peginterferon (older)", "Lifestyle support"],
        "diet": ["Healthy balanced diet", "Limit iron intake (if advised)", "Avoid alcohol", "Low-salt diet", "Limit sugar", "Hydration", "Coffee", "Fruits"],
        "precautions": ["Avoid sharing needles/personal items", "Cover wounds", "Safe sex", "Avoid alcohol", "Regular medical monitoring", "Vaccinate for Hep A/B", "Review medications", "Dental hygiene"],
        "workout": ["Regular moderate exercise", "Walking", "Cycling", "Strength training (light)", "Rest when tired"],
        "doctor": "Hepatologist"
    },
    "Hepatitis D": {
        "symptoms": ["joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "abdominal_pain", "nausea", "loss_of_appetite", "confusion", "bruising_easily", "swelling_of_belly", "itchy_skin", "worsening_of_hep_b", "fever", "clay_colored_stools"],
        "medications": ["Pegylated interferon alpha", "Antivirals for Hep B", "Liver transplant (end stage)", "Supportive therapy"],
        "diet": ["High-calorie", "Protein-rich (unless encephalopathy)", "Hypoallergenic foods", "Absolute alcohol avoidance", "Hydration", "Vitamin B complex"],
        "precautions": ["Prevent Hep B infection (vaccine)", "Safe sex", "Avoid IV drugs", "Regular liver monitoring", "Hygiene", "Avoid hepatotoxins", "Family screening", "Support groups"],
        "workout": ["Mild activity", "Rest prioritised"],
        "doctor": "Hepatologist"
    },
    "Hepatitis E": {
        "symptoms": ["joint_pain", "vomiting", "fatigue", "high_fever", "yellowish_skin", "nausea", "dark_urine", "loss_of_appetite", "abdominal_pain", "pale_stools", "enlarged_liver", "itching", "skin_rash", "weakness"],
        "medications": ["Supportive care", "Ribavirin (chronic cases)", "Rest", "Fluids", "Nutritional support"],
        "diet": ["Boiled water", "Cooked foods", "Fruits (peeled)", "Avoid street food", "Hydration", "Light meals", "Avoid alcohol", "Electrolytes"],
        "precautions": ["Drink purified water", "Proper sanitation", "Hand washing", "Avoid raw shellfish", "Hygiene during pregnancy", "Rest", "Safe food practices", "Disposal of waste"],
        "workout": ["Complete rest", "No exercise during acute phase"],
        "doctor": "Hepatologist"
    },
    "Alcoholic hepatitis": {
        "symptoms": ["vomiting", "yellowish_skin", "abdominal_pain", "swelling_of_stomach", "distention_of_abdomen", "nausea", "fever", "fatigue", "confusion", "history_of_alcohol_consumption"],
        "medications": ["Corticosteroids", "Pentoxifylline", "Alcohol cessation support", "Nutritional supplements", "Liver transplant (if eligible and sober)"],
        "diet": ["High-calorie diet", "High-protein diet", "Vitamin supplements (B1, B12, K)", "Low-sodium", "Small frequent meals", "No alcohol", "Hydration", "Enteral feeding if needed"],
        "precautions": ["Stop drinking alcohol immediately", "Join support group (AA)", "Regular checkups", "Monitor weight", "Infection prevention", "Vaccinations", "Avoid harmful drugs", "Psychological counseling"],
        "workout": ["Doctor_supervised_rehabilitation", "Light walking", "Breathing exercises"],
        "doctor": "Hepatologist"
    },

    # --- ENDOCRINOLOGY ---
    "Diabetes": {
        "symptoms": ["weight_loss", "polyuria", "increased_thirst", "increased_hunger", "blurred_vision", "frequent_infections", "numbness_in_hands_feet", "dry_skin", "irregular_sugar_level"],
        "medications": ["Insulin therapy", "Metformin", "Sulfonylureas", "Meglitinides", "Thiazolidinediones", "DPP-4 inhibitors", "GLP-1 receptor agonists", "SGLT2 inhibitors"],
        "diet": ["Low-glycemic index foods", "Whole grains", "Leafy green vegetables", "Lean proteins", "Healthy fats (nuts, seeds)", "Avoid sugary drinks", "Portion control", "Regular meal timings"],
        "precautions": ["Monitor blood sugar regularly", "Foot care", "Regular eye exams", "Manage blood pressure", "Manage cholesterol", "Quit smoking", "Limit alcohol", "Stress management"],
        "workout": ["Brisk walking", "Cycling", "Swimming", "Strength training", "Aerobic exercises", "Yoga"],
        "doctor": "Endocrinologist"
    },
    "Hypothyroidism": {
        "symptoms": ["fatigue", "weight_gain", "cold_hands_and_feets", "mood_swings", "lethargy", "dizziness", "puffy_face_and_eyes", "brittle_nails", "dry_skin"],
        "medications": ["Levothyroxine (Synthetic T4)", "Liothyronine", "Dessicated thyroid extract", "Vitamin D", "Vitamin B12 supplements"],
        "diet": ["Iodine-rich foods (if deficiency)", "Selenium-rich foods (Brazilian nuts)", "Zinc-rich foods", "Fiber", "Bone broth", "Avoid soy in excess", "Avoid goitrogenic veggies raw", "Gluten-free (if sensitive)"],
        "precautions": ["Regular thyroid function tests", "Take medication empty stomach", "Monitor weight", "Skin care", "Manage stress", "Wear warm clothes", "Regular exercise", "Awareness of drug interactions"],
        "workout": ["Aerobic exercise", "Strength training", "Yoga", "Walking", "Pilates"],
        "doctor": "Endocrinologist"
    },
    "Hyperthyroidism": {
        "symptoms": ["weight_loss", "restlessness", "sweating", "diarrhea", "fast_heart_rate", "excessive_hunger", "muscle_weakness", "irritability", "palpitations", "shaking/tremors", "heat_sensitivity", "goiter"],
        "medications": ["Anti-thyroid medications (Methimazole)", "Propylthiouracil", "Beta blockers", "Radioactive iodine", "Surgery", "Vitamin supplements"],
        "diet": ["Low-iodine diet", "Cruciferous vegetables", "Calcium-rich foods", "Vitamin D", "Healthy fats", "High-calorie (if weight loss severe)", "Avoid caffeine", "Selenium"],
        "precautions": ["Stress management", "Eye protection (if Graves')", "Regular monitoring", "Calcium intake", "Avoid iodine supplements", "Quit smoking", "Heart rate monitoring", "Cool environment"],
        "workout": ["Low-impact exercise", "Relaxation techniques", "Yoga", "Tai Chi", "Avoid intense cardio slightly"],
        "doctor": "Endocrinologist"
    },
    "Hypoglycemia": {
        "symptoms": ["shakiness", "dizziness", "sweating", "excessive_hunger", "irritability", "palpitations", "confusion", "slurred_speech", "loss_of_consciousness"],
        "medications": ["Glucose tablets", "Glucagon injection", "IV dextrose", "Adjust diabetes meds", "Treating underlying cause"],
        "diet": ["Complex carbohydrates", "Fiber-rich foods", "Protein with carbs", "Regular meals", "Avoid sugary snacks alone", "Whole grains", "Fruits", "Nuts"],
        "precautions": ["Monitor blood sugar", "Carry fast-acting sugar", "Wear medical ID", "Educate family/friends", "Don't skip meals", "Alcohol caution", "Safety while driving", "Regular check-ups"],
        "workout": ["Light to moderate exercise", "Check sugar before workout", "Carry snack", "Avoid exercise if low"],
        "doctor": "Endocrinologist"
    },

    # --- RESPIRATORY ---
    "Bronchial Asthma": {
        "symptoms": ["cough", "breathlessness", "wheezing", "chest_tightness", "shortness_of_breath", "difficulty_talking", "allergy_signs"], # Removed high_fever
        "medications": ["Inhaled Corticosteroids", "Short-acting Beta Agonists (Inhalers)", "Long-acting Beta Agonists", "Leukotriene Modifiers", "Theophylline", "Combination inhalers", "Oral corticosteroids"],
        "diet": ["Magnesium-rich foods", "Omega-3 fatty acids", "Vitamin D rich foods", "Antioxidant-rich fruits", "Avoiding sulfites (dried fruits)", "Avoiding gas-inducing foods", "Ginger and turmeric", "Hydration"],
        "precautions": ["Identify and avoid triggers", "Carry rescue inhaler", "Get vaccinated (flu/pneumonia)", "Avoid smoking/secondhand smoke", "Keep home dust-free", "Monitor peak flow", "Warm up before exercise", "Stress control"],
        "workout": ["Swimming (indoor)", "Walking", "Yoga/Breathing exercises", "Short bursts of activity", "Medicinal warm-up"],
        "doctor": "Pulmonologist"
    },
    "Common Cold": {
        "symptoms": ["continuous_sneezing", "cough", "headache", "swollen_lymph_nodes", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "loss_of_smell"], # Removed chest_pain
        "medications": ["Decongestants", "Antihistamines", "Pain relievers (Ibuprofen)", "Cough suppressants", "Expectorants", "Zinc lozenges", "Vitamin C"],
        "diet": ["Chicken soup", "Warm tea with honey", "Citrus fruits", "Garlic", "Ginger", "Spicy foods (clear sinuses)", "Hydration", "Probiotics"],
        "precautions": ["Wash hands often", "Cover cough/sneeze", "Avoid touching face", "Disinfect surfaces", "Stay home", "Rest", "Hydrate", "Use disposable tissues"],
        "workout": ["Mild walking", "Rest", "Avoid heavy cardio"],
        "doctor": "General Physician"
    },
    "Pneumonia": {
        "symptoms": ["cough", "high_fever", "breathlessness", "phlegm", "chest_pain", "fast_heart_rate", "rusty_sputum", "chills", "sweating"],
        "medications": ["Antibiotics (if bacterial)", "Antivirals (if viral)", "Fungal medications (if fungal)", "Antipyretics", "Cough medicine", "Pain relievers", "Oxygen therapy"],
        "diet": ["High-calorie foods", "Protein-rich foods", "Fruits and vegetables", "Hydration", "Warm fluids", "Honey and lemon", "Soups", "Smoothies"],
        "precautions": ["Finish antibiotics", "Rest is crucial", "Humidifier use", "No smoking", "Vaccination (pneumococcal/flu)", "Hand hygiene", "Follow-up X-ray", "Avoid pollutants"],
        "workout": ["Respiratory physiotherapy", "Deep breathing exercises", "Avoid exertion until cleared"],
        "doctor": "Pulmonologist"
    },
    "Tuberculosis": {
        "symptoms": ["cough", "high_fever", "breathlessness", "blood_in_sputum", "chest_pain", "weight_loss", "night_sweats", "fatigue"],
        "medications": ["Isoniazid", "Rifampicin", "Ethambutol", "Pyrazinamide", "Streptomycin", "Vitamin B6 supplements"],
        "diet": ["High-protein diet", "Calorie-dense foods", "Citrus fruits", "Leafy vegetables", "Whole grains", "Eggs", "Milk", "Nuts"],
        "precautions": ["Complete full course of medication", "Cover mouth when coughing", "Mask usage", "Ventilation", "Isolation during infectious phase", "Hand hygiene", "Regular follow-up", "Screen contacts"],
        "workout": ["Light walking", "Breathing exercises", "Avoid strenuous labor"],
        "doctor": "Pulmonologist"
    },

    # --- CARDIOLOGY ---
    "Hypertension": {
        "symptoms": ["headache", "chest_pain", "dizziness", "shortness_of_breath", "pounding_in_chest_ears", "nosebleeds", "irregular_heartbeat", "visual_disturbances"],
        "medications": ["Diuretics", "ACE Inhibitors", "Angiotensin II Receptor Blockers (ARBs)", "Calcium Channel Blockers", "Beta Blockers", "Alpha Blockers", "Vasodilators"],
        "diet": ["DASH diet", "Low-sodium foods", "Potassium-rich foods", "Whole grains", "Low-fat dairy", "Fruits and vegetables", "Limit alcohol", "Reduce caffeine"],
        "precautions": ["Monitor blood pressure regularly", "Reduce salt intake", "Manage stress", "Maintain healthy weight", "Limit alcohol", "Quit smoking", "Follow medication schedule", "Regular doctor visits"],
        "workout": ["Aerobic exercise", "Brisk walking", "Jogging", "Cycling", "Swimming", "avoid heavy weight lifting (check with doctor)"],
        "doctor": "Cardiologist"
    },
    "Heart attack": {
        "symptoms": ["chest_pain", "pain_radiating_to_arm", "shortness_of_breath", "sweating", "nausea", "dizziness", "palpitations", "anxiety", "impending_doom_feeling", "cold_sweat"], # Removed vomiting, fatigue (generic)
        "medications": ["Aspirin", "Thrombolytics", "Antiplatelet agents", "Pain relievers (Morphine)", "Nitroglycerin", "Beta blockers", "ACE inhibitors", "Statins"],
        "diet": ["Heart-healthy diet", "Low-sodium", "Low-saturated fat", "Fruits and vegetables", "Whole grains", "Omega-3 fatty acids", "Nuts", "Avoid processed foods"],
        "precautions": ["Immediate medical help", "Cardiac rehabilitation", "Quit smoking", "Manage stress", "Control BP and cholesterol", "Weight management", "Regular checkups", "Adhere to meds"],
        "workout": ["Cardiac_rehabilitation_program", "Walking", "Light jogging (post recovery)", "Resistance training (guided)", "Yoga"],
        "doctor": "Cardiologist"
    },
    "Varicose veins": {
        "symptoms": ["swollen_legs", "swollen_blood_vessels", "prominent_veins_on_calf", "aching_legs", "fatigue", "cramps", "bruising"],
        "medications": ["Sclerotherapy", "Endovenous ablation", "Compression stockings (not drug)", "Anti-inflammatory drugs", "Flavonoids", "Blood thinners (if clotting risk)"],
        "diet": ["High-fiber diet", "Vitamin C and E", "Flavonoid-rich foods (berries)", "Potassium-rich foods", "Low-salt diet", "Hydration", "Chia seeds", "Ginger"],
        "precautions": ["Wear compression stockings", "Elevate legs", "Avoid long standing/sitting", "Weight control", "Exercise regularly", "Avoid tight clothing", "Skin care", "Change position often"],
        "workout": ["Walking", "Cycling", "Swimming", "Leg lifts", "Calf raises", "Avoid high-impact running"],
        "doctor": "Vascular Surgeon"
    },

    # --- NEUROLOGY ---
    "Migraine": {
        "symptoms": ["headache", "nausea", "vomiting", "sensitivity_to_light", "sensitivity_to_sound", "aura", "pulsing_pain", "dizziness"], # Removed acidity, indigestion
        "medications": ["Pain relievers (NSAIDs)", "Triptans", "Ergotamines", "Anti-nausea medications", "Beta blockers (preventive)", "Antidepressants (preventive)", "Botox injections"],
        "diet": ["Magnesium-rich foods", "Riboflavin (B2) foods", "Identify food triggers", "Hydration", "Ginger tea", "Regular meals", "Avoid aged cheeses", "Avoid processed meats"],
        "precautions": ["Regular sleep schedule", "Manage stress", "Avoid sensory overload", "Keep a headache diary", "Limit caffeine", "Avoid known triggers", "Relaxation techniques", "Hydration"],
        "workout": ["Regular moderate aerobic exercise", "Yoga", "Tai Chi", "Neck stretches", "Avoid extreme exertion"],
        "doctor": "Neurologist"
    },
    "Paralysis (brain hemorrhage)": {
        "symptoms": ["weakness_of_one_body_side", "slurred_speech", "altered_sensorium", "facial_droop", "loss_of_balance", "confusion", "headache", "vomiting"],
        "medications": ["Blood pressure medications", "Diuretics", "Anticonvulsants", "Pain relievers", "Rehabilitation therapy", "Surgery (if needed)", "Anticoagulants (careful use)"],
        "diet": ["Low-sodium diet", "Heart-healthy foods", "High-fiber diet", "Easy to chew/swallow foods (if needed)", "Hydration", "Balanced nutrition"],
        "precautions": ["Control blood pressure", "Fall prevention", "Regular extensive rehabilitation", "Pressure ulcer prevention", "Assistive devices use", "Caregiver support", "Regular medical follow-up", "Lifestyle modification"],
        "workout": ["Doctor_supervised_rehabilitation", "Physiotherapy", "Range of motion exercises", "Occupational therapy", "Muscle strengthening", "Balance training"],
        "doctor": "Neurologist"
    },
    "(vertigo) Paroymsal Positional Vertigo": {
        "symptoms": ["spinning_movements", "loss_of_balance", "dizziness", "nausea", "vomiting", "unsteadiness", "nystagmus (eye jerking)"], # Removed headache (not typical BPPV)
        "medications": ["Canalith repositioning maneuvers (Epley)", "Meclizine", "Benzodiazepines", "Antiemetics", "Vestibular rehabilitation", "Betahistine"],
        "diet": ["Low-salt diet", "Hydration", "Avoid caffeine", "Avoid alcohol", "Vitamin B6", "Ginger", "Ginkgo biloba", "Whole foods"],
        "precautions": ["Avoid sudden head movements", "Sleep with head elevated", "Sit down if dizzy", "Use night light", "Fall prevention", "Stress management", "Avoid driving if dizzy", "Hydration"],
        "workout": ["Balance exercises", "Brandt-Daroff exercises", "Tai Chi", "Walking (with unstable support)"],
        "doctor": "ENT Specialist/Neurologist"
    },

    # --- INFECTIOUS ---
    "Malaria": {
        "symptoms": ["chills", "high_fever", "sweating", "headache", "nausea", "vomiting", "muscle_pain", "diarrhea", "anemia"],
        "medications": ["Artemisinin-based combination therapies (ACTs)", "Chloroquine", "Quinine", "Primaquine", "Doxycycline", "Mefloquine", "Antipyretics (for fever)"],
        "diet": ["High-calorie diet", "High-protein diet", "Fluid intake", "Vitamin C rich fruits", "Electroyltes", "Easily digestible foods", "Khichdi/Porridge", "Coconut water"],
        "precautions": ["Use mosquito nets", "Apply mosquito repellent", "Wear long sleeves", "Eliminate standing water", "Take prophylactic meds if traveling", "Early diagnosis", "Rest", "Hydration"],
        "workout": ["Complete rest", "No exercise during infection"],
        "doctor": "General Physician/Infectious Disease Specialist"
    },
    "Dengue": {
        "symptoms": ["skin_rash", "high_fever", "headache", "pain_behind_eyes", "joint_pain", "muscle_pain", "fatigue", "nausea", "vomiting", "bleeding_gums", "low_platelet_count"],
        "medications": ["Pain relievers (Acetaminophen/Paracetamol)", "AVOID aspirin/ibuprofen", "IV fluids", "Platelet transfusion (if severe)", "ORS"],
        "diet": ["Papaya leaf juice", "Coconut water", "High-protein diet", "Vitamin C rich fruits", "Pomegranate", "Spinach", "Hydration", "Soft easy-to-digest foods"],
        "precautions": ["Prevent mosquito bites", "Use mosquito nets", "Rest completely", "Monitor platelet count", "Hydration", "Watch for warning signs (bleeding)", "Wear protective clothing", "Eliminate breeding sites"],
        "workout": ["Complete rest", "No exercise"],
        "doctor": "General Physician/Infectious Disease Specialist"
    },
    "Typhoid": {
        "symptoms": ["high_fever", "headache", "abdominal_pain", "constipation", "diarrhea", "weakness", "muscle_ache", "rash_rose_spots"],
        "medications": ["Antibiotics (Ciprofloxacin, Azithromycin)", "Antipyretics", "Corticosteroids (severe cases)", "IV fluids", "Replacement electrolytes"],
        "diet": ["High-calorie diet", "High-protein diet", "Soft cooked foods", "Boiled water", "Yogurt", "Avoid fiber-rich foods (during acute phase)", "Fruit juices (hygienic)", "Mashed bananas"],
        "precautions": ["Hand hygiene", "Drink treated/boiled water", "Eat cooked hot foods", "Vaccination", "Avoid street food", "Proper sanitation", "Complete antibiotic course", "Rest"],
        "workout": ["Complete rest during fever", "Gradual walking during recovery"],
        "doctor": "General Physician"
    },

    # --- ORTHOPEDICS / RHEUMATOLOGY ---
    "Cervical spondylosis": {
        "symptoms": ["neck_pain", "stiffness_in_neck", "shoulder_pain", "arm_pain", "back_pain", "weakness_in_limbs", "dizziness", "numbness_in_arms"],
        "medications": ["NSAIDs", "Muscle relaxants", "Corticosteroids", "Anti-seizure medications (for nerve pain)", "Antidepressants", "Topical analgesics"],
        "diet": ["Anti-inflammatory diet", "Calcium-rich foods", "Vitamin D rich foods", "Omega-3 fatty acids", "Protein for muscle repair", "Hydration", "Fruits and vegetables"],
        "precautions": ["Maintain good posture", "Ergonomic workspace", "Avoid heavy lifting", "Use a cervical pillow", "Take regular breaks from screens", "Neck exercises", "Apply heat/ice", "Massage therapy"],
        "workout": ["Neck stretches", "Neck strengthening exercises", "Yoga for spine", "Walking", "Low-impact aerobics", "Physiotherapy"],
        "doctor": "Orthopedic/Rheumatologist"
    },
    "Osteoarthristis": {
        "symptoms": ["joint_pain", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking", "stiffness", "grating_sensation", "pain_worse_with_activity"],
        "medications": ["Acetaminophen", "NSAIDs", "Topical pain relievers", "Corticosteroid injections", "Hyaluronic acid injections", "Duloxetine", "Glucosamine/Chondroitin"],
        "diet": ["Anti-inflammatory diet", "Omega-3 fatty acids", "Vitamin D and C", "Calcium-rich foods", "Weight loss diet", "Green tea", "Nuts and seeds", "Avoid sugar"],
        "precautions": ["Weight management", "Joint protection", "Use assistive devices", "Heat/Cold therapy", "Good posture", "Choosing right footwear", "Avoid repetitive strain", "Physical therapy"],
        "workout": ["Low-impact aerobics", "Swimming", "Water aerobics", "Strength training", "Range of motion exercises", "Tai Chi"],
        "doctor": "Rheumatologist"
    },
    "Arthritis": {
        "symptoms": ["joint_pain", "swelling_joints", "stiff_neck", "movement_stiffness", "painful_walking", "redness", "tenderness", "morning_stiffness"], # Removed fatigue, fever, weight_loss (generic)
        "medications": ["DMARDs", "Biologics", "NSAIDs", "Steroids", "Analgesics", "Jak inhibitors", "Physical therapy"],
        "diet": ["Mediterranean diet", "Fatty fish", "Olive oil", "Berries", "Nuts", "Garlic", "Spinach", "Avoid processed foods"],
        "precautions": ["Joint care", "Maintain healthy weight", "Quit smoking", "Heat and cold treatment", "Assistive devices", "Regular exercise", "Massage", "Stress reduction"],
        "workout": ["Range-of-motion exercises", "Strengthening exercises", "Aerobic exercise (low impact)", "Yoga", "Swimming"],
        "doctor": "Rheumatologist"
    },

    # --- UROLOGY ---
    "Urinary tract infection": {
        "symptoms": ["burning_micturition", "frequent_urination", "bladder_discomfort", "pelvic_pain", "foul_smell_of_urine", "cloudy_urine", "blood_in_urine", "back_pain"],
        "medications": ["Antibiotics (Nitrofurantoin, Bactrim)", "Phenazopyridine (pain relief)", "Cranberry supplements", "Probiotics", "D-Mannose"],
        "diet": ["Cranberry juice/extract", "Water (lots)", "Probiotic yogurt", "Vitamin C", "Avoid caffeine", "Avoid alcohol", "Avoid spicy foods", "Blueberries"],
        "precautions": ["Hydration", "Wipe front to back", "Urinate after sex", "Avoid irritating products", "Cotton underwear", "Don't hold urine", "Showers instead of baths", "Change pads frequently"],
        "workout": ["Light walking", "Pelvic floor exercises (when healed)", "Rest"],
        "doctor": "Urologist"
    }
}

def clean_snake_case(text):
    return text.lower().replace(" ", "_")

def generate_datasets():
    # A. Symptoms DF
    symptoms_rows = []
    # Columns: Disease, Symptom_1, ... Symptom_20
    
    unique_symptoms = set()

    for disease in DISEASES:
        data = DATA.get(disease)
        if not data: 
            print(f"Warning: No data for {disease}")
            continue
        
        symptoms_list = data["symptoms"]
        # Ensure 20 columns
        row = {"Disease": disease}
        for i in range(20):
            sym = symptoms_list[i] if i < len(symptoms_list) else np.nan
            row[f"Symptom_{i+1}"] = sym
            if sym is not np.nan:
                unique_symptoms.add(sym)
        
        symptoms_rows.append(row)
    
    symptoms_df = pd.DataFrame(symptoms_rows)
    symptoms_df.to_csv("symptoms_df_clean.csv", index=False)
    print("Created symptoms_df_clean.csv")

    # B. Symptom Severity
    # Assign random but plausible severity 1-10
    severity_rows = []
    severity_map = {
        "itching": 1, "skin_rash": 3, "nodal_skin_eruptions": 4, "continuous_sneezing": 4, 
        "shivering": 5, "chills": 3, "joint_pain": 3, "stomach_pain": 5, "acidity": 3, 
        "ulcers_on_tongue": 4, "muscle_wasting": 3, "vomiting": 5, "burning_micturition": 6, 
        "fatigue": 4, "weight_gain": 3, "anxiety": 4, "cold_hands_and_feets": 5, 
        "mood_swings": 3, "weight_loss": 3, "restlessness": 5, "lethargy": 2, 
        "patches_in_throat": 6, "irregular_sugar_level": 5, "cough": 4, "high_fever": 7, 
        "sunken_eyes": 3, "breathlessness": 4, "sweating": 3, "dehydration": 4, 
        "indigestion": 5, "headache": 3, "yellowish_skin": 3, "dark_urine": 4, 
        "nausea": 5, "loss_of_appetite": 4, "pain_behind_the_eyes": 4, "back_pain": 3, 
        "constipation": 4, "abdominal_pain": 4, "diarrhea": 6, "mild_fever": 5, 
        "yellow_urine": 4, "yellowing_of_eyes": 4, "acute_liver_failure": 6, 
        "fluid_overload": 6, "swelling_of_stomach": 7, "swelled_lymph_nodes": 6, 
        "malaise": 6, "blurred_and_distorted_vision": 5, "phlegm": 5, "throat_irritation": 4, 
        "redness_of_eyes": 5, "sinus_pressure": 4, "runny_nose": 5, "congestion": 5, 
        "chest_pain": 7, "weakness_in_limbs": 7, "fast_heart_rate": 5, 
        "pain_during_bowel_movements": 5, "pain_in_anal_region": 6, "bloody_stool": 5, 
        "irritation_in_anus": 6, "neck_pain": 5, "dizziness": 4, "cramps": 4, 
        "bruising": 4, "obesity": 4, "swollen_legs": 5, "swollen_blood_vessels": 5, 
        "puffy_face_and_eyes": 5, "enlarged_thyroid": 6, "brittle_nails": 5, 
        "swollen_extremeties": 5, "excessive_hunger": 4, "extra_marital_contacts": 5, 
        "drying_and_tingling_lips": 4, "slurred_speech": 4, "knee_pain": 3, 
        "hip_joint_pain": 2, "muscle_weakness": 2, "stiff_neck": 4, "swelling_joints": 5, 
        "movement_stiffness": 5, "spinning_movements": 6, "loss_of_balance": 4, 
        "unsteadiness": 4, "weakness_of_one_body_side": 4, "loss_of_smell": 3, 
        "bladder_discomfort": 4, "foul_smell_of_urine": 5, "continuous_feel_of_urine": 6, 
        "passage_of_gases": 5, "internal_itching": 4, "toxic_look_(typhos)": 5, 
        "depression": 3, "irritability": 2, "muscle_pain": 2, "altered_sensorium": 2, 
        "red_spots_over_body": 3, "belly_pain": 4, "abnormal_menstruation": 6, 
        "dischromic_patches": 6, "watering_from_eyes": 4, "increased_appetite": 5, 
        "polyuria": 4, "family_history": 5, "mucoid_sputum": 4, "rusty_sputum": 4, 
        "lack_of_concentration": 3, "visual_disturbances": 3, 
        "receiving_blood_transfusion": 5, "receiving_unsterile_injections": 2, 
        "coma": 7, "stomach_bleeding": 6, "distention_of_abdomen": 4, 
        "history_of_alcohol_consumption": 5, "fluid_overload": 4, "blood_in_sputum": 5, 
        "prominent_veins_on_calf": 6, "palpitations": 4, "painful_walking": 2, 
        "pus_filled_pimples": 2, "blackheads": 2, "scurring": 2, "skin_peeling": 3, 
        "silver_like_dusting": 2, "small_dents_in_nails": 2, "inflammatory_nails": 2, 
        "blister": 4, "red_sore_around_nose": 2, "yellow_crust_ooze": 3
    }

    # Default logic for new symptoms not in map
    for sym in unique_symptoms:
        severity = severity_map.get(sym)
        if not severity:
            if "pain" in sym or "bleeding" in sym or "fever" in sym:
                severity = np.random.randint(5, 8)
            elif "failure" in sym or "heart" in sym or "coma" in sym:
                severity = np.random.randint(7, 10)
            else:
                severity = np.random.randint(2, 5)
        
        severity_rows.append({"Symptom": sym, "weight": severity})
    
    severity_df = pd.DataFrame(severity_rows)
    severity_df.to_csv("symptom_severity_clean.csv", index=False)
    print("Created symptom_severity_clean.csv")

    # C. Medications
    meds_rows = []
    for disease in DISEASES:
        d = DATA.get(disease, {})
        meds = str(d.get("medications", []))
        meds_rows.append({"Disease": disease, "Medication": meds})
    pd.DataFrame(meds_rows).to_csv("medications_clean.csv", index=False)
    print("Created medications_clean.csv")

    # D. Diet
    diet_rows = []
    for disease in DISEASES:
        d = DATA.get(disease, {})
        diet = str(d.get("diet", []))
        diet_rows.append({"Disease": disease, "Diet": diet})
    pd.DataFrame(diet_rows).to_csv("diet_clean.csv", index=False)
    print("Created diet_clean.csv")

    # E. Precautions
    prec_rows = []
    # Columns: Disease, Precaution_1 ... Precaution_4
    for disease in DISEASES:
        d = DATA.get(disease, {})
        precs = d.get("precautions", [])
        row = {"Disease": disease}
        for i in range(8): # User requested 5-8 precautions
            # Wait, user asked for 5-8. But original app helper() function expects `precautions` to have specific structure. 
            # I will check precautions_df columns logic.
            # actually user asked for "precautions_clean.csv".
            # I will output comma separated string or multiple columns? Original: Precaution_1...4.
            # I will output 4 columns to be safe with existing app logic, or maybe more.
            # The prompt says "Generate 5-8 precautions". I'll put them in columns.
            p = precs[i] if i < len(precs) else np.nan
            row[f"Precaution_{i+1}"] = p
        prec_rows.append(row)
    pd.DataFrame(prec_rows).to_csv("precautions_clean.csv", index=False)
    print("Created precautions_clean.csv")

    # F. Workout
    work_rows = []
    for disease in DISEASES:
        d = DATA.get(disease, {})
        # Original CSV has 'disease' and 'workout'. I will keep it.
        # Workout list as string or multiple columns? Original was one column 'workout' with duplicates?
        # User requirement: "Create Disease–Workout/Lifestyle mapping".
        # I'll create a list.
        w = d.get("workout", [])
        for item in w:
             work_rows.append({"disease": disease, "workout": item})
             
    pd.DataFrame(work_rows).to_csv("workout_clean.csv", index=False)
    print("Created workout_clean.csv")

    # G. Doctor
    doc_rows = []
    for disease in DISEASES:
        d = DATA.get(disease, {})
        doc = d.get("doctor", "General Physician")
        doc_rows.append({"Disease": disease, "Doctor": doc})
    pd.DataFrame(doc_rows).to_csv("doctor_specialization_clean.csv", index=False)
    print("Created doctor_specialization_clean.csv")

if __name__ == "__main__":
    generate_datasets()
