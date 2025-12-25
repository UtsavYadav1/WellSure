# followup_questions.py
# Disease-Aware Follow-Up Questions for LOW/MEDIUM Confidence Cases
# This module provides clinically relevant questions that map to symptom keywords

# ============================================================================
# SYMPTOM KEYWORD MAPPING
# Maps each question ID to exact symptom keywords that exist in disease_rules
# ============================================================================

QUESTION_SYMPTOM_MAP = {
    # ========== DERMATOLOGY ==========
    # Psoriasis
    "psoriasis_silvery": "silvery scales, thick plaques",
    "psoriasis_chronic": "chronic scaly rash",
    "psoriasis_nails": "nail changes",
    
    # Fungal Infection / Ringworm
    "fungal_ring": "ring shaped rash, scaly border",
    "fungal_itch": "itching",
    "fungal_spread": "spreading rash",
    "fungal_moist": "moist area",
    
    # Eczema
    "eczema_dry": "dry itchy patches, cracked skin",
    "eczema_inflamed": "red inflamed skin",
    "eczema_ooze": "oozing",
    
    # Acne
    "acne_pimples": "pimples",
    "acne_blackheads": "blackheads, whiteheads",
    "acne_oily": "oily skin",
    
    # Contact Dermatitis
    "contact_localized": "localized rash, skin irritation after contact",
    "contact_blister": "blistering at contact site",
    
    # Seborrheic Dermatitis (Dandruff)
    "dandruff_flaky": "dandruff, flaky scalp",
    "dandruff_itchy": "itchy scalp",
    "dandruff_oily": "oily skin, red patches",
    
    # Urticaria
    "urticaria_hives": "hives, raised welts",
    "urticaria_comes_goes": "comes and goes",
    
    # ========== RESPIRATORY ==========
    # Pneumonia
    "pneumonia_mucus": "cough with mucus, productive cough",
    "pneumonia_chest": "chest pain while breathing",
    "pneumonia_fever": "high fever, chills",
    
    # Bronchial Asthma
    "asthma_wheeze": "wheezing",
    "asthma_trigger": "triggered by allergens, triggered by exercise",
    "asthma_night": "cough at night",
    "asthma_tight": "chest tightness",
    
    # COPD
    "copd_chronic": "chronic cough",
    "copd_mucus": "mucus production",
    "copd_breathless": "progressive breathlessness",
    
    # Sinusitis
    "sinusitis_facial": "facial pain",
    "sinusitis_discharge": "thick nasal discharge",
    "sinusitis_congestion": "nasal congestion",
    
    # Common Cold
    "cold_runny": "runny nose",
    "cold_sneeze": "sneezing",
    "cold_throat": "sore throat",
    
    # ========== GASTROINTESTINAL ==========
    # GERD
    "gerd_heartburn": "heartburn, acid reflux",
    "gerd_regurg": "regurgitation",
    "gerd_lying": "burning chest",
    
    # Gastritis
    "gastritis_burning": "stomach burning, upper abdominal pain",
    "gastritis_nausea": "nausea",
    "gastritis_bloat": "bloating, indigestion",
    
    # Peptic Ulcer
    "ulcer_pain": "burning stomach pain, pain between meals",
    "ulcer_relief": "pain relieved by eating",
    "ulcer_nsaid": "nsaid use",
    
    # IBS
    "ibs_cramping": "abdominal cramping",
    "ibs_bloating": "bloating",
    "ibs_bowel": "altered bowel habits",
    
    # Gastroenteritis
    "gastro_diarrhea": "watery diarrhea",
    "gastro_vomit": "vomiting",
    "gastro_cramps": "stomach cramps",
    
    # Food Poisoning
    "foodpois_sudden": "sudden vomiting, diarrhea",
    "foodpois_food": "recent suspicious food",
    
    # ========== URINARY ==========
    # Urinary Tract Infection
    "uti_burn": "burning urination",
    "uti_frequent": "frequent urination, urinary urgency",
    "uti_cloudy": "cloudy urine, strong urine odor",
    "uti_pelvic": "pelvic pain, lower abdominal pain",
    
    # Kidney Stones
    "kidney_flank": "severe flank pain, pain radiating to groin",
    "kidney_blood": "blood in urine",
    "kidney_nausea": "nausea, painful urination",
    
    # ========== ENDOCRINE ==========
    # Diabetes
    "diabetes_thirst": "increased thirst, excessive urination",
    "diabetes_weight": "unexplained weight loss",
    "diabetes_fatigue": "fatigue, blurred vision",
    
    # Hypothyroidism
    "hypo_fatigue": "persistent fatigue",
    "hypo_cold": "cold intolerance",
    "hypo_weight": "weight gain",
    "hypo_constip": "constipation, dry skin",
    
    # Hyperthyroidism
    "hyper_weight": "weight loss",
    "hyper_heart": "rapid heartbeat, racing heart",
    "hyper_heat": "heat intolerance",
    "hyper_anxiety": "anxiety, tremor",
    
    # PCOS
    "pcos_periods": "irregular periods",
    "pcos_hair": "excess hair growth",
    "pcos_acne": "acne, weight gain",
    
    # ========== MUSCULOSKELETAL ==========
    # Arthritis / Osteoarthritis
    "arthritis_joint": "joint pain, joint swelling",
    "arthritis_stiff": "joint stiffness, morning stiffness",
    "arthritis_motion": "reduced range of motion",
    
    # Sciatica
    "sciatica_radiating": "lower back pain radiating to leg, shooting pain down leg",
    "sciatica_numb": "leg numbness, tingling",
    "sciatica_sitting": "pain worse sitting",
    
    # Muscle Strain
    "strain_tender": "muscle pain, muscle tenderness",
    "strain_limited": "limited movement",
    "strain_swelling": "swelling, bruising",
    
    # ========== NEUROLOGY ==========
    # Migraine
    "migraine_one_side": "one sided head pain, one sided headache",
    "migraine_throb": "throbbing headache",
    "migraine_light": "sensitivity to light, sensitivity to sound",
    "migraine_nausea": "nausea, vomiting",
    
    # Tension Headache
    "tension_band": "band like head pain, pressure around head",
    "tension_neck": "neck stiffness, shoulder tension",
    
    # Vertigo
    "vertigo_spinning": "spinning sensation, room spinning",
    "vertigo_balance": "loss of balance",
    "vertigo_nausea": "nausea, sweating",
    
    # ========== GENERAL / INFECTIOUS ==========
    # Viral Fever
    "viral_fever": "fever, high fever",
    "viral_body": "body aches",
    "viral_fatigue": "fatigue, weakness",
    
    # Dengue
    "dengue_eyes": "pain behind eyes",
    "dengue_rash": "rash",
    "dengue_joint": "joint pain, muscle pain",
    "dengue_mosquito": "mosquito bite",
    
    # Typhoid
    "typhoid_prolonged": "prolonged fever",
    "typhoid_weakness": "weakness, abdominal pain",
    "typhoid_appetite": "loss of appetite",
    
    # Malaria
    "malaria_cyclic": "cyclic fever, chills and rigors",
    "malaria_sweating": "sweating",
    "malaria_travel": "malaria-endemic area travel",
    
    # COVID-19
    "covid_taste": "loss of taste, loss of smell",
    "covid_cough": "dry cough",
    "covid_sob": "shortness of breath",
    
    # Tuberculosis
    "tb_cough": "persistent cough",
    "tb_night": "night sweats",
    "tb_weight": "unexplained weight loss",
    
    # ========== CARDIAC ==========
    # Angina
    "angina_exertion": "chest discomfort on exertion, chest tightness with activity",
    "angina_rest": "pain relieved by rest",
    
    # Palpitations
    "palp_racing": "heart racing, skipped beats",
    "palp_flutter": "fluttering in chest",
    
    # ========== EYE ==========
    # Conjunctivitis
    "conj_red": "red eye, pink eye",
    "conj_discharge": "eye discharge",
    "conj_itchy": "itchy eyes",
}


# ============================================================================
# DISEASE-SPECIFIC FOLLOW-UP QUESTIONS
# Each disease maps to 2-4 clinically relevant questions targeting missing symptoms
# ============================================================================

DISEASE_FOLLOWUP_QUESTIONS = {
    # ========== DERMATOLOGY ==========
    "Psoriasis": [
        {"id": "psoriasis_silvery", "text": "Do you see silvery-white scales on raised, thick skin patches?", "type": "yes_no"},
        {"id": "psoriasis_chronic", "text": "Have these skin patches been present for weeks or longer?", "type": "yes_no"},
    ],
    "Fungal infection": [
        {"id": "fungal_ring", "text": "Is the rash ring-shaped with a clearer center and scaly border?", "type": "yes_no"},
        {"id": "fungal_itch", "text": "Is the affected area intensely itchy?", "type": "yes_no"},
        {"id": "fungal_spread", "text": "Has the rash been spreading or getting larger?", "type": "yes_no"},
    ],
    "Ringworm": [
        {"id": "fungal_ring", "text": "Is the rash circular with raised scaly edges?", "type": "yes_no"},
        {"id": "fungal_itch", "text": "Is the area itchy?", "type": "yes_no"},
        {"id": "fungal_spread", "text": "Is the rash spreading to other areas?", "type": "yes_no"},
    ],
    "Eczema": [
        {"id": "eczema_dry", "text": "Is your skin dry, cracked, or rough in patches?", "type": "yes_no"},
        {"id": "eczema_inflamed", "text": "Are the affected areas red and inflamed?", "type": "yes_no"},
        {"id": "eczema_ooze", "text": "Do the patches sometimes ooze or weep fluid?", "type": "yes_no"},
    ],
    "Contact Dermatitis": [
        {"id": "contact_localized", "text": "Did the rash appear after contact with something specific (soap, jewelry, plants)?", "type": "yes_no"},
        {"id": "contact_blister", "text": "Are there blisters at the contact site?", "type": "yes_no"},
    ],
    "Acne": [
        {"id": "acne_pimples", "text": "Do you have pimples, pustules, or cysts on your face, chest, or back?", "type": "yes_no"},
        {"id": "acne_blackheads", "text": "Do you see blackheads or whiteheads?", "type": "yes_no"},
        {"id": "acne_oily", "text": "Is your skin oilier than normal?", "type": "yes_no"},
    ],
    "Seborrheic Dermatitis": [
        {"id": "dandruff_flaky", "text": "Do you have dandruff or flaky patches on your scalp?", "type": "yes_no"},
        {"id": "dandruff_itchy", "text": "Is your scalp itchy?", "type": "yes_no"},
        {"id": "dandruff_oily", "text": "Is your scalp or face oily with red patches?", "type": "yes_no"},
    ],
    "Urticaria": [
        {"id": "urticaria_hives", "text": "Do you have raised, itchy welts or hives on your skin?", "type": "yes_no"},
        {"id": "urticaria_comes_goes", "text": "Do the welts appear and disappear within hours?", "type": "yes_no"},
    ],
    
    # ========== RESPIRATORY ==========
    "Pneumonia": [
        {"id": "pneumonia_mucus", "text": "Do you have a cough with phlegm or mucus?", "type": "yes_no"},
        {"id": "pneumonia_chest", "text": "Do you feel chest pain when breathing deeply or coughing?", "type": "yes_no"},
        {"id": "pneumonia_fever", "text": "Do you have high fever with chills?", "type": "yes_no"},
    ],
    "Bronchial Asthma": [
        {"id": "asthma_wheeze", "text": "Do you hear a whistling or wheezing sound when breathing?", "type": "yes_no"},
        {"id": "asthma_trigger", "text": "Do symptoms worsen with exercise, cold air, or allergens?", "type": "yes_no"},
        {"id": "asthma_tight", "text": "Does your chest feel tight?", "type": "yes_no"},
    ],
    "COPD": [
        {"id": "copd_chronic", "text": "Have you had a cough that has persisted for many weeks or months?", "type": "yes_no"},
        {"id": "copd_mucus", "text": "Do you regularly cough up mucus?", "type": "yes_no"},
        {"id": "copd_breathless", "text": "Do you get short of breath even with mild activity?", "type": "yes_no"},
    ],
    "Sinusitis": [
        {"id": "sinusitis_facial", "text": "Do you have pain or pressure around your forehead, cheeks, or eyes?", "type": "yes_no"},
        {"id": "sinusitis_discharge", "text": "Do you have thick, colored nasal discharge?", "type": "yes_no"},
        {"id": "sinusitis_congestion", "text": "Is your nose blocked or congested?", "type": "yes_no"},
    ],
    "Common Cold": [
        {"id": "cold_runny", "text": "Do you have a runny or stuffy nose?", "type": "yes_no"},
        {"id": "cold_sneeze", "text": "Are you sneezing frequently?", "type": "yes_no"},
        {"id": "cold_throat", "text": "Is your throat sore or scratchy?", "type": "yes_no"},
    ],
    "Tonsillitis": [
        {"id": "cold_throat", "text": "Is your throat very sore?", "type": "yes_no"},
        {"id": "pneumonia_fever", "text": "Do you have fever?", "type": "yes_no"},
    ],
    "Pharyngitis": [
        {"id": "cold_throat", "text": "Do you have throat pain, especially when swallowing?", "type": "yes_no"},
        {"id": "pneumonia_fever", "text": "Do you have fever?", "type": "yes_no"},
    ],
    
    # ========== GASTROINTESTINAL ==========
    "GERD": [
        {"id": "gerd_heartburn", "text": "Do you experience burning in your chest after eating?", "type": "yes_no"},
        {"id": "gerd_regurg", "text": "Do you have acid or food coming back up into your throat?", "type": "yes_no"},
        {"id": "gerd_lying", "text": "Do symptoms worsen when lying down?", "type": "yes_no"},
    ],
    "Gastritis": [
        {"id": "gastritis_burning", "text": "Do you have burning pain in your upper stomach?", "type": "yes_no"},
        {"id": "gastritis_nausea", "text": "Do you feel nauseous?", "type": "yes_no"},
        {"id": "gastritis_bloat", "text": "Do you feel bloated or have indigestion?", "type": "yes_no"},
    ],
    "Peptic Ulcer": [
        {"id": "ulcer_pain", "text": "Do you have burning stomach pain between meals or at night?", "type": "yes_no"},
        {"id": "ulcer_relief", "text": "Does eating or taking antacids temporarily relieve the pain?", "type": "yes_no"},
    ],
    "IBS": [
        {"id": "ibs_cramping", "text": "Do you experience abdominal cramping or pain?", "type": "yes_no"},
        {"id": "ibs_bloating", "text": "Do you feel bloated frequently?", "type": "yes_no"},
        {"id": "ibs_bowel", "text": "Do you have irregular bowel movements (alternating constipation/diarrhea)?", "type": "yes_no"},
    ],
    "Gastroenteritis": [
        {"id": "gastro_diarrhea", "text": "Do you have watery diarrhea?", "type": "yes_no"},
        {"id": "gastro_vomit", "text": "Have you been vomiting?", "type": "yes_no"},
        {"id": "gastro_cramps", "text": "Do you have stomach cramps?", "type": "yes_no"},
    ],
    "Food Poisoning": [
        {"id": "foodpois_sudden", "text": "Did vomiting or diarrhea start suddenly?", "type": "yes_no"},
        {"id": "foodpois_food", "text": "Did you eat anything suspicious or undercooked recently?", "type": "yes_no"},
    ],
    
    # ========== URINARY ==========
    "Urinary Tract Infection": [
        {"id": "uti_burn", "text": "Do you feel burning or pain when urinating?", "type": "yes_no"},
        {"id": "uti_frequent", "text": "Are you urinating more frequently or feeling urgent need?", "type": "yes_no"},
        {"id": "uti_cloudy", "text": "Is your urine cloudy or has an unusual smell?", "type": "yes_no"},
        {"id": "uti_pelvic", "text": "Do you have pain in your lower abdomen or pelvic area?", "type": "yes_no"},
    ],
    "UTI": [
        {"id": "uti_burn", "text": "Do you feel burning or pain when urinating?", "type": "yes_no"},
        {"id": "uti_frequent", "text": "Are you urinating more frequently or feeling urgent need?", "type": "yes_no"},
        {"id": "uti_cloudy", "text": "Is your urine cloudy or has an unusual smell?", "type": "yes_no"},
    ],
    "Kidney Stones": [
        {"id": "kidney_flank", "text": "Do you have severe pain in your side or back that radiates to groin?", "type": "yes_no"},
        {"id": "kidney_blood", "text": "Have you noticed blood in your urine?", "type": "yes_no"},
        {"id": "kidney_nausea", "text": "Do you have nausea or pain when urinating?", "type": "yes_no"},
    ],
    
    # ========== ENDOCRINE ==========
    "Diabetes": [
        {"id": "diabetes_thirst", "text": "Are you experiencing excessive thirst and frequent urination?", "type": "yes_no"},
        {"id": "diabetes_weight", "text": "Have you had unexplained weight loss?", "type": "yes_no"},
        {"id": "diabetes_fatigue", "text": "Do you feel unusually tired or have blurred vision?", "type": "yes_no"},
    ],
    "Hypothyroidism": [
        {"id": "hypo_fatigue", "text": "Are you feeling unusually tired or sluggish?", "type": "yes_no"},
        {"id": "hypo_cold", "text": "Are you more sensitive to cold than usual?", "type": "yes_no"},
        {"id": "hypo_weight", "text": "Have you gained weight without changing your diet?", "type": "yes_no"},
        {"id": "hypo_constip", "text": "Do you have constipation or dry skin?", "type": "yes_no"},
    ],
    "Hyperthyroidism": [
        {"id": "hyper_weight", "text": "Have you lost weight despite eating normally?", "type": "yes_no"},
        {"id": "hyper_heart", "text": "Is your heart racing or beating rapidly?", "type": "yes_no"},
        {"id": "hyper_heat", "text": "Do you feel overheated or intolerant to heat?", "type": "yes_no"},
        {"id": "hyper_anxiety", "text": "Do you feel anxious, nervous, or have hand tremors?", "type": "yes_no"},
    ],
    "PCOS": [
        {"id": "pcos_periods", "text": "Are your periods irregular or infrequent?", "type": "yes_no"},
        {"id": "pcos_hair", "text": "Do you have excess facial or body hair growth?", "type": "yes_no"},
        {"id": "pcos_acne", "text": "Do you have acne or have you gained weight recently?", "type": "yes_no"},
    ],
    
    # ========== MUSCULOSKELETAL ==========
    "Arthritis": [
        {"id": "arthritis_joint", "text": "Do you have pain and swelling in your joints?", "type": "yes_no"},
        {"id": "arthritis_stiff", "text": "Are your joints stiff, especially in the morning?", "type": "yes_no"},
        {"id": "arthritis_motion", "text": "Is your range of motion in affected joints reduced?", "type": "yes_no"},
    ],
    "Osteoarthritis": [
        {"id": "arthritis_joint", "text": "Do you have joint pain that worsens with activity?", "type": "yes_no"},
        {"id": "arthritis_stiff", "text": "Do you have morning stiffness lasting less than 30 minutes?", "type": "yes_no"},
    ],
    "Sciatica": [
        {"id": "sciatica_radiating", "text": "Does pain radiate from your lower back down your leg?", "type": "yes_no"},
        {"id": "sciatica_numb", "text": "Do you have numbness or tingling in your leg?", "type": "yes_no"},
        {"id": "sciatica_sitting", "text": "Is the pain worse when sitting?", "type": "yes_no"},
    ],
    "Muscle Strain": [
        {"id": "strain_tender", "text": "Is the affected muscle tender to touch?", "type": "yes_no"},
        {"id": "strain_limited", "text": "Is your movement limited in that area?", "type": "yes_no"},
        {"id": "strain_swelling", "text": "Is there swelling or bruising?", "type": "yes_no"},
    ],
    "Cervical Spondylosis": [
        {"id": "sciatica_numb", "text": "Do you have numbness or tingling in your arms or hands?", "type": "yes_no"},
        {"id": "tension_neck", "text": "Do you have neck pain or stiffness?", "type": "yes_no"},
    ],
    
    # ========== NEUROLOGY ==========
    "Migraine": [
        {"id": "migraine_one_side", "text": "Is the headache on one side of your head?", "type": "yes_no"},
        {"id": "migraine_throb", "text": "Is the pain throbbing or pulsating?", "type": "yes_no"},
        {"id": "migraine_light", "text": "Does light or sound make the headache worse?", "type": "yes_no"},
        {"id": "migraine_nausea", "text": "Do you feel nauseous or have you vomited?", "type": "yes_no"},
    ],
    "Tension Headache": [
        {"id": "tension_band", "text": "Does it feel like a tight band around your head?", "type": "yes_no"},
        {"id": "tension_neck", "text": "Do you have neck stiffness or shoulder tension?", "type": "yes_no"},
    ],
    "Vertigo": [
        {"id": "vertigo_spinning", "text": "Does the room feel like it's spinning around you?", "type": "yes_no"},
        {"id": "vertigo_balance", "text": "Do you have trouble keeping your balance?", "type": "yes_no"},
        {"id": "vertigo_nausea", "text": "Do you feel nauseous or sweaty with these episodes?", "type": "yes_no"},
    ],
    
    # ========== GENERAL / INFECTIOUS ==========
    "Viral Fever": [
        {"id": "viral_fever", "text": "Do you have a fever?", "type": "yes_no"},
        {"id": "viral_body", "text": "Do you have body aches or muscle pain?", "type": "yes_no"},
        {"id": "viral_fatigue", "text": "Are you feeling very tired or weak?", "type": "yes_no"},
    ],
    "Flu": [
        {"id": "viral_fever", "text": "Did fever come on suddenly?", "type": "yes_no"},
        {"id": "viral_body", "text": "Do you have severe body aches?", "type": "yes_no"},
        {"id": "viral_fatigue", "text": "Are you feeling extremely fatigued?", "type": "yes_no"},
    ],
    "Dengue": [
        {"id": "dengue_eyes", "text": "Do you have pain behind your eyes?", "type": "yes_no"},
        {"id": "dengue_rash", "text": "Have you noticed any skin rash?", "type": "yes_no"},
        {"id": "dengue_joint", "text": "Do you have severe joint or muscle pain?", "type": "yes_no"},
    ],
    "Typhoid": [
        {"id": "typhoid_prolonged", "text": "Has your fever been persistent for several days?", "type": "yes_no"},
        {"id": "typhoid_weakness", "text": "Do you feel very weak with abdominal discomfort?", "type": "yes_no"},
        {"id": "typhoid_appetite", "text": "Have you lost your appetite?", "type": "yes_no"},
    ],
    "Malaria": [
        {"id": "malaria_cyclic", "text": "Do you have fever episodes with chills and sweating that come and go?", "type": "yes_no"},
        {"id": "malaria_sweating", "text": "Do you experience intense sweating after the fever subsides?", "type": "yes_no"},
    ],
    "COVID-19": [
        {"id": "covid_taste", "text": "Have you lost your sense of taste or smell?", "type": "yes_no"},
        {"id": "covid_cough", "text": "Do you have a dry cough?", "type": "yes_no"},
        {"id": "covid_sob", "text": "Are you experiencing shortness of breath?", "type": "yes_no"},
    ],
    "Tuberculosis": [
        {"id": "tb_cough", "text": "Have you had a persistent cough for more than 2 weeks?", "type": "yes_no"},
        {"id": "tb_night", "text": "Do you have night sweats?", "type": "yes_no"},
        {"id": "tb_weight", "text": "Have you had unexplained weight loss?", "type": "yes_no"},
    ],
    
    # ========== CARDIAC ==========
    "Angina": [
        {"id": "angina_exertion", "text": "Do you get chest discomfort or tightness during physical activity?", "type": "yes_no"},
        {"id": "angina_rest", "text": "Does the discomfort go away with rest?", "type": "yes_no"},
    ],
    "Palpitations": [
        {"id": "palp_racing", "text": "Does your heart feel like it's racing or skipping beats?", "type": "yes_no"},
        {"id": "palp_flutter", "text": "Do you feel a fluttering sensation in your chest?", "type": "yes_no"},
    ],
    
    # ========== EYE ==========
    "Conjunctivitis": [
        {"id": "conj_red", "text": "Are your eyes red or pink?", "type": "yes_no"},
        {"id": "conj_discharge", "text": "Do you have discharge from your eyes?", "type": "yes_no"},
        {"id": "conj_itchy", "text": "Are your eyes itchy?", "type": "yes_no"},
    ],
    
    # ========== ALLERGY ==========
    "Allergy": [
        {"id": "cold_sneeze", "text": "Are you sneezing frequently?", "type": "yes_no"},
        {"id": "urticaria_hives", "text": "Do you have hives or itchy skin?", "type": "yes_no"},
        {"id": "cold_runny", "text": "Do you have a runny nose or watery eyes?", "type": "yes_no"},
    ],
    
    # ========== HEPATITIS / JAUNDICE ==========
    "Jaundice": [
        {"id": "viral_fatigue", "text": "Are you feeling fatigued?", "type": "yes_no"},
        {"id": "gastritis_nausea", "text": "Do you feel nauseous?", "type": "yes_no"},
    ],
    "Hepatitis A": [
        {"id": "viral_fatigue", "text": "Are you feeling very tired?", "type": "yes_no"},
        {"id": "gastritis_nausea", "text": "Do you have nausea or loss of appetite?", "type": "yes_no"},
    ],
    "Hepatitis B": [
        {"id": "viral_fatigue", "text": "Are you feeling very tired?", "type": "yes_no"},
        {"id": "gastritis_nausea", "text": "Do you have nausea or abdominal pain?", "type": "yes_no"},
    ],
    
    # ========== ANEMIA ==========
    "Anemia": [
        {"id": "viral_fatigue", "text": "Are you feeling unusually tired or weak?", "type": "yes_no"},
        {"id": "vertigo_balance", "text": "Do you feel dizzy or lightheaded?", "type": "yes_no"},
    ],
}


# Default questions for diseases not in the mapping
DEFAULT_FOLLOWUP_QUESTIONS = [
    {"id": "viral_fatigue", "text": "Are you feeling unusually tired or weak?", "type": "yes_no"},
    {"id": "viral_fever", "text": "Do you have a fever?", "type": "yes_no"},
    {"id": "gastritis_nausea", "text": "Do you feel nauseous?", "type": "yes_no"},
]


# ============================================================================
# FUNCTIONS
# ============================================================================

def should_show_followup(confidence_level, is_followup_request=False):
    """
    Determine if follow-up questions should be shown.
    
    Rules:
    - HIGH confidence: Never show follow-up
    - Already a follow-up request: Don't show again
    - LOW or MEDIUM confidence (first time): Show follow-up
    """
    if confidence_level == "HIGH":
        return False
    if is_followup_request:
        return False
    return True


def get_followup_questions(predicted_disease, max_questions=4):
    """
    Get disease-specific follow-up questions.
    
    Args:
        predicted_disease: The disease name from prediction
        max_questions: Maximum number of questions to return
        
    Returns:
        List of question dicts with id, text, and type
    """
    questions = DISEASE_FOLLOWUP_QUESTIONS.get(predicted_disease, DEFAULT_FOLLOWUP_QUESTIONS)
    return questions[:max_questions]


def get_symptom_keywords_from_answers(answers, disease=None):
    """
    Convert follow-up answers to exact symptom keywords for re-analysis.
    
    Only "yes" answers are converted to symptoms.
    Uses QUESTION_SYMPTOM_MAP for precise keyword mapping.
    
    Args:
        answers: Dict of {question_id: answer_value}
        disease: Optional disease name (for context, not currently used)
        
    Returns:
        Tuple of (symptom_string, confirmed_symptoms_list)
        - symptom_string: Comma-separated symptoms to append
        - confirmed_symptoms_list: List of individual symptoms confirmed
    """
    symptom_additions = []
    confirmed_symptoms = []
    
    for qid, answer in answers.items():
        # Skip non-question fields
        if qid in ['symptoms', 'is_followup', 'age', 'gender', 'original_disease', 'original_confidence']:
            continue
            
        # Only process "yes" answers
        if answer and answer.lower() in ['yes', 'y']:
            # Look up the symptom keywords for this question
            if qid in QUESTION_SYMPTOM_MAP:
                keywords = QUESTION_SYMPTOM_MAP[qid]
                symptom_additions.append(keywords)
                # Track individual symptoms for explanation panel
                for symptom in keywords.split(", "):
                    if symptom.strip() and symptom.strip() not in confirmed_symptoms:
                        confirmed_symptoms.append(symptom.strip())
    
    symptom_string = ", ".join(symptom_additions) if symptom_additions else ""
    return symptom_string, confirmed_symptoms


def format_answers_as_symptoms(answers):
    """
    Legacy function for backward compatibility.
    Converts follow-up answers into symptom text.
    
    Args:
        answers: Dict of {question_id: answer_value}
        
    Returns:
        String of formatted symptom context
    """
    symptom_string, _ = get_symptom_keywords_from_answers(answers)
    return symptom_string
