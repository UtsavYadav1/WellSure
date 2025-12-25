import re

class RulesEngine:
    def __init__(self):
        # Refactored: Primary + Supporting Symptom Logic
        self.disease_rules = {
            "Psoriasis": {
                "primary": ["silvery scales", "thick plaques", "chronic scaly rash", "scaly plaques"],
                "supporting": ["itching", "peeling"],
                "exclusions": ["fever"]
            },
            "Chicken pox": {
                "primary": ["fluid filled blisters"],
                "supporting": ["fever", "itching"],
                "exclusions": []
            },
            "Impetigo": {
                "primary": ["honey colored crust", "oozing sores"],
                "supporting": ["blister", "red skin"],
                "exclusions": []
            },
            "Allergy": {
                "primary": ["sneezing", "hives", "runny nose"],
                "supporting": ["itching", "watery eyes"],
                "exclusions": ["sore throat", "fever"]
            },
            "Fungal infection": {
                "primary": ["ring shaped rash", "scaly border", "itchy round rash", "ringworm", "round rash"],
                "supporting": ["itching", "spreading"],
                "exclusions": []
            },
            "GERD": {
                "primary": ["heartburn", "acid reflux"],
                "supporting": ["burning chest", "regurgitation"],
                "exclusions": ["shortness of breath"]
            },
            "Pneumonia": {
                "primary": ["productive cough", "chest infection", "cough with high fever", "high fever with cough", "rusty sputum", "phlegm with fever", "fever with cough", "lung infection", "pneumonia symptoms"],
                "supporting": ["fever", "shortness of breath", "chills", "chest pain", "rapid breathing", "difficulty breathing", "high fever"],
                "exclusions": ["wheezing", "exercise triggered", "night cough only"]
            },
            "Bronchial Asthma": {
                "primary": ["wheezing", "asthma attack", "bronchospasm"],
                "supporting": ["breathlessness", "cough", "chest tightness", "night cough", "exercise triggered symptoms"],
                "exclusions": ["fever", "productive cough", "rusty sputum", "phlegm", "chest infection"]
            },
            
            # ========== DERMATOLOGY ==========
            "Eczema": {
                "primary": ["dry itchy patches", "red inflamed skin", "cracked skin", "eczema flare"],
                "supporting": ["itching", "scaling", "oozing", "thickened skin", "skin discoloration"],
                "exclusions": ["fever", "ring shaped rash", "circular rash", "fungal", "ringworm", "scalp"]
            },
            "Contact Dermatitis": {
                "primary": ["localized rash", "skin irritation after contact", "blistering at contact site", "contact rash"],
                "supporting": ["itching", "burning", "redness", "swelling", "dry patches"],
                "exclusions": ["ring shaped rash", "scalp", "dandruff", "fungal"]
            },
            "Rosacea": {
                "primary": ["facial redness", "visible blood vessels", "facial flushing"],
                "supporting": ["bumps on face", "eye irritation", "burning sensation", "thickened skin", "sensitive skin"],
                "exclusions": []
            },
            "Shingles": {
                "primary": ["painful blisters one side", "band like rash", "burning pain before rash"],
                "supporting": ["fever", "headache", "sensitivity to light", "fatigue", "tingling sensation"],
                "exclusions": []
            },
            "Acne": {
                "primary": ["pimples", "blackheads", "whiteheads"],
                "supporting": ["oily skin", "scarring", "cysts", "nodules", "skin inflammation"],
                "exclusions": []
            },
            "Urticaria": {
                "primary": ["hives", "raised welts", "itchy wheals"],
                "supporting": ["swelling", "itching", "burning", "comes and goes", "triggered by allergen"],
                "exclusions": []
            },
            "Conjunctivitis": {
                "primary": ["red eye", "eye discharge", "itchy eyes", "pink eye"],
                "supporting": ["watery eyes", "burning eyes", "sensitivity to light", "gritty feeling", "swollen eyelids"],
                "exclusions": []
            },
            "Seborrheic Dermatitis": {
                "primary": ["dandruff", "itchy scalp", "flaky scalp", "scalp irritation"],
                "supporting": ["oily skin", "red patches", "hair loss", "crusty scales", "eyebrow flakes"],
                "exclusions": []
            },
            "Ringworm": {
                "primary": ["ring shaped rash", "circular rash", "scaly border", "itchy round rash"],
                "supporting": ["itching", "red patches", "spreading rash", "raised edges", "clear center"],
                "exclusions": []
            },
            
            # ========== RESPIRATORY ==========
            "COPD": {
                "primary": ["chronic cough", "mucus production", "progressive breathlessness"],
                "supporting": ["wheezing", "chest tightness", "fatigue", "frequent respiratory infections", "weight loss"],
                "exclusions": ["high fever", "fever", "rusty sputum"]
            },
            "Pneumonia": {
                "primary": ["high fever", "cough with mucus", "cough with phlegm", "chest pain while breathing", "chest pain while coughing"],
                "supporting": ["chills", "shortness of breath", "fatigue", "weakness", "rapid breathing", "nausea", "vomiting", "rusty sputum", "fever with chills"],
                "exclusions": []
            },
            "Bronchial Asthma": {
                "primary": ["wheezing", "breathlessness", "chest tightness", "difficulty breathing"],
                "supporting": ["cough", "shortness of breath", "cough at night", "triggered by allergens", "triggered by exercise", "tight chest"],
                "exclusions": ["high fever", "fever with chills", "rusty sputum"]
            },
            "Sinusitis": {
                "primary": ["facial pain", "nasal congestion", "thick nasal discharge"],
                "supporting": ["headache", "post nasal drip", "reduced smell", "cough", "fever", "bad breath"],
                "exclusions": []
            },
            "Tonsillitis": {
                "primary": ["sore throat", "swollen tonsils", "difficulty swallowing"],
                "supporting": ["fever", "white patches on tonsils", "swollen lymph nodes", "bad breath", "voice changes"],
                "exclusions": []
            },
            "Post-viral Cough": {
                "primary": ["persistent dry cough", "cough after cold"],
                "supporting": ["tickle in throat", "no fever", "clear airways", "cough worse at night", "recent viral illness"],
                "exclusions": ["productive cough", "fever"]
            },
            "Common Cold": {
                "primary": ["runny nose", "sneezing", "sore throat", "nazla", "zukam", "cold symptoms"],
                "supporting": ["mild fever", "cough", "congestion", "body aches", "fatigue", "nasal congestion"],
                "exclusions": []
            },
            "Pharyngitis": {
                "primary": ["sore throat", "throat pain", "painful swallowing"],
                "supporting": ["fever", "swollen glands", "hoarse voice", "cough", "headache"],
                "exclusions": []
            },
            
            # ========== GASTROENTEROLOGY ==========
            "IBS": {
                "primary": ["abdominal cramping", "bloating", "altered bowel habits"],
                "supporting": ["gas", "mucus in stool", "incomplete evacuation", "symptoms after eating", "stress related"],
                "exclusions": ["blood in stool", "weight loss"]
            },
            "Gastritis": {
                "primary": ["upper abdominal pain", "nausea", "stomach burning"],
                "supporting": ["bloating", "indigestion", "loss of appetite", "vomiting", "feeling full quickly"],
                "exclusions": []
            },
            "Food Poisoning": {
                "primary": ["sudden vomiting", "diarrhea", "abdominal cramps"],
                "supporting": ["nausea", "fever", "weakness", "dehydration", "recent suspicious food"],
                "exclusions": []
            },
            "Peptic Ulcer": {
                "primary": ["burning stomach pain", "pain between meals", "pain relieved by eating"],
                "supporting": ["bloating", "nausea", "heartburn", "dark stool", "weight loss"],
                "exclusions": []
            },
            "Gastroenteritis": {
                "primary": ["watery diarrhea", "vomiting", "stomach cramps"],
                "supporting": ["nausea", "fever", "headache", "muscle aches", "dehydration"],
                "exclusions": []
            },
            
            # ========== NEUROLOGY ==========
            "Tension Headache": {
                "primary": ["band like head pain", "pressure around head", "bilateral headache"],
                "supporting": ["neck stiffness", "shoulder tension", "stress related", "mild sensitivity to light", "no nausea"],
                "exclusions": ["severe vomiting", "visual aura"]
            },
            "Migraine": {
                "primary": ["throbbing headache", "one sided head pain", "severe headache", "one sided headache"],
                "supporting": ["nausea", "vomiting", "sensitivity to light", "sensitivity to sound", "visual aura", "dizziness"],
                "exclusions": []
            },
            "Cervical Radiculopathy": {
                "primary": ["neck pain radiating to arm", "arm numbness", "arm weakness"],
                "supporting": ["tingling in fingers", "neck stiffness", "pain worse with movement", "muscle spasms"],
                "exclusions": []
            },
            "Vertigo": {
                "primary": ["spinning sensation", "room spinning", "loss of balance"],
                "supporting": ["nausea", "vomiting", "sweating", "abnormal eye movements", "hearing changes"],
                "exclusions": []
            },
            
            # ========== ENDOCRINE ==========
            "PCOS": {
                "primary": ["irregular periods", "excess hair growth", "polycystic ovaries"],
                "supporting": ["weight gain", "acne", "hair thinning", "difficulty conceiving", "dark skin patches"],
                "exclusions": []
            },
            "Hypothyroidism": {
                "primary": ["persistent fatigue", "weight gain", "cold intolerance"],
                "supporting": ["constipation", "dry skin", "hair loss", "depression", "slow heart rate", "muscle weakness", "fatigue"],
                "exclusions": ["irregular periods", "excess hair growth"]
            },
            "Hyperthyroidism": {
                "primary": ["weight loss", "rapid heartbeat", "heat intolerance", "fast heartbeat", "racing heart"],
                "supporting": ["anxiety", "tremor", "sweating", "frequent bowel movements", "difficulty sleeping", "nervousness"],
                "exclusions": []
            },
            "Diabetes": {
                "primary": ["increased thirst", "excessive urination", "unexplained weight loss"],
                "supporting": ["fatigue", "blurred vision", "slow healing", "tingling in feet", "frequent infections", "frequent urination"],
                "exclusions": ["burning urination"]
            },
            
            # ========== GENERAL MEDICINE ==========
            "Viral Fever": {
                "primary": ["fever", "high fever", "body aches", "low grade fever", "fatigue", "tiredness", "weakness", "feeling weak"],
                "supporting": ["headache", "chills", "loss of appetite", "mild cough", "lethargy"],
                "exclusions": ["shortness of breath", "productive cough", "chest infection", "difficulty breathing", "rusty sputum"]
            },
            "Flu": {
                "primary": ["sudden fever", "muscle aches", "extreme fatigue"],
                "supporting": ["headache", "dry cough", "sore throat", "runny nose", "chills"],
                "exclusions": []
            },
            "Dengue": {
                "primary": ["high fever", "severe headache", "pain behind eyes", "mosquito fever", "mosquito bite fever"],
                "supporting": ["joint pain", "muscle pain", "rash", "nausea", "bleeding gums", "body aches"],
                "exclusions": []
            },
            "Typhoid": {
                "primary": ["prolonged fever", "abdominal pain", "weakness"],
                "supporting": ["headache", "constipation", "diarrhea", "rose spots", "enlarged spleen"],
                "exclusions": []
            },
            "Malaria": {
                "primary": ["cyclic fever", "chills and rigors", "sweating"],
                "supporting": ["headache", "nausea", "vomiting", "fatigue", "muscle pain"],
                "exclusions": []
            },
            "Tuberculosis": {
                "primary": ["persistent cough", "night sweats", "unexplained weight loss", "coughing blood"],
                "supporting": ["low grade fever", "fatigue", "loss of appetite", "chest pain", "shortness of breath"],
                "exclusions": []
            },
            "COVID-19": {
                "primary": ["fever", "dry cough", "loss of taste", "loss of smell", "shortness of breath"],
                "supporting": ["fatigue", "body aches", "headache", "sore throat", "congestion", "diarrhea"],
                "exclusions": ["productive cough", "rusty sputum", "phlegm"]
            },
            "Hepatitis A": {
                "primary": ["jaundice", "dark urine", "fatigue", "nausea"],
                "supporting": ["abdominal pain", "loss of appetite", "low grade fever", "joint pain", "clay colored stool"],
                "exclusions": ["yellow skin", "yellow eyes", "burning urination", "frequent urination", "pelvic pain"]
            },
            "Hepatitis B": {
                "primary": ["jaundice", "dark urine", "fatigue", "abdominal pain"],
                "supporting": ["nausea", "vomiting", "joint pain", "loss of appetite", "fever"],
                "exclusions": ["yellow skin", "yellow eyes", "burning urination", "frequent urination", "pelvic pain"]
            },
            "Hepatitis C": {
                "primary": ["jaundice", "fatigue", "dark urine"],
                "supporting": ["nausea", "joint pain", "abdominal discomfort", "poor appetite"],
                "exclusions": ["yellow skin", "yellow eyes", "burning urination", "frequent urination", "pelvic pain"]
            },
            "Jaundice": {
                "primary": ["yellow skin", "yellow eyes", "dark urine"],
                "supporting": ["fatigue", "abdominal pain", "itching", "pale stool", "nausea", "weight loss"],
                "exclusions": []
            },
            "Meningitis": {
                "primary": ["stiff neck", "severe headache", "high fever", "sensitivity to light"],
                "supporting": ["nausea", "vomiting", "confusion", "rash", "drowsiness"],
                "exclusions": ["productive cough", "cough", "chest infection"]
            },
            "Anemia": {
                "primary": ["fatigue", "pale skin", "weakness", "shortness of breath"],
                "supporting": ["dizziness", "cold hands", "brittle nails", "fast heartbeat", "headache", "chest pain"],
                "exclusions": ["fever", "cough", "productive cough"]
            },
            
            # ========== CARDIAC (Non-Emergency) ==========
            "Angina": {
                "primary": ["chest discomfort on exertion", "chest tightness with activity", "pain relieved by rest"],
                "supporting": ["shortness of breath", "fatigue", "nausea", "sweating", "pain in arm or jaw"],
                "exclusions": []
            },
            "Palpitations": {
                "primary": ["heart racing", "skipped beats", "fluttering in chest"],
                "supporting": ["anxiety", "dizziness", "shortness of breath", "fatigue", "caffeine related"],
                "exclusions": []
            },
            "Hypertension": {
                "primary": ["high blood pressure", "persistent elevated bp"],
                "supporting": ["headache", "dizziness", "blurred vision", "nosebleeds", "fatigue"],
                "exclusions": []
            },
            
            # ========== UROLOGY ==========
            "Urinary Tract Infection": {
                "primary": ["burning urination", "frequent urination", "urinary urgency", "pelvic pain"],
                "supporting": ["cloudy urine", "blood in urine", "strong urine odor", "low grade fever", "lower abdominal pain"],
                "exclusions": []
            },
            "Kidney Stones": {
                "primary": ["severe flank pain", "pain radiating to groin", "colicky pain"],
                "supporting": ["blood in urine", "nausea", "vomiting", "painful urination", "urinary urgency"],
                "exclusions": []
            },
            
            # ========== PEDIATRICS ==========
            "Diaper Rash": {
                "primary": ["red irritated diaper area", "skin irritation in diaper region"],
                "supporting": ["fussiness", "discomfort during diaper change", "warm skin", "peeling skin"],
                "exclusions": []
            },
            "Otitis Media": {
                "primary": ["ear pain", "ear tugging", "irritability in child"],
                "supporting": ["fever", "difficulty sleeping", "fluid drainage", "hearing difficulty", "loss of appetite"],
                "exclusions": []
            },
            "Hand Foot Mouth Disease": {
                "primary": ["mouth sores", "rash on hands and feet", "fever in child"],
                "supporting": ["sore throat", "drooling", "loss of appetite", "irritability"],
                "exclusions": []
            },
            
            # ========== MUSCULOSKELETAL ==========
            "Arthritis": {
                "primary": ["joint pain", "joint swelling", "joint stiffness"],
                "supporting": ["morning stiffness", "reduced range of motion", "warmth around joint", "fatigue", "weakness"],
                "exclusions": ["pain behind eyes", "high fever"]
            },
            "Muscle Strain": {
                "primary": ["muscle pain", "muscle tenderness", "limited movement"],
                "supporting": ["swelling", "bruising", "muscle spasm", "weakness", "stiffness"],
                "exclusions": []
            },
            "Sciatica": {
                "primary": ["lower back pain radiating to leg", "shooting pain down leg", "leg numbness"],
                "supporting": ["tingling", "muscle weakness", "pain worse sitting", "difficulty standing"],
                "exclusions": []
            },
            "Osteoarthritis": {
                "primary": ["joint pain", "joint stiffness", "morning stiffness"],
                "supporting": ["reduced range of motion", "joint swelling", "cracking sound", "pain after activity", "age related"],
                "exclusions": ["fever", "rash"]
            }
        }
        
        # NLP Mapping: Symptom Aliases (Synonyms)
        self.symptom_aliases = {
            # Psoriasis
            "silvery scales": ["silver scale", "white scales", "flaky white", "silvery plate", "silver rashes"],
            "thick plaques": ["thick skin", "hard patches", "raised plaques"],
            "chronic scaly rash": ["old rash", "persistent scaling", "long term rash"],
            
            # Fungal Infection
            "ring shaped rash": ["round rash", "circular rash", "red ring", "ringworm", "curvy rash"],
            "scaly border": ["rough edges", "peeling border", "crusty edge"],
            
            # Impetigo
            "honey colored crust": ["yellow crust", "gold crust", "pustules with crust"],
            "oozing sores": ["wet sores", "leaking skin", "damp rashes"],
            
            # Common / General
            "itching": ["itchy", "scratchy", "irritated skin", "pruritus", "wants to scratch"],
            "peeling": ["skin falling off", "skin shedding", "flaking"],
            "fever": ["high temperature", "feeling hot", "chills", "pyrexia"],
            "blister": ["fluid filled", "bulla", "vesicle", "skin bubble"],
            "sneezing": ["sneeze", "hay fever"],
            "hives": ["urticaria", "red bumps", "wheals"],
            "heartburn": ["acid in chest", "chest burning after eating"],
            "shortness of breath": ["breathless", "difficulty breathing", "sob", "stuffy breathing", "can't breathe"],
            "wheezing": ["whistling sound when breathing", "noisy breathing"],
            "cough": ["coughing", "hacking"]
        }
        
        # Kept for get_specialist utility
        self.specialist_map = {
            "Dermatologist": ["Fungal infection", "Acne", "Psoriasis", "Impetigo", "Chicken pox", 
                              "Eczema", "Contact Dermatitis", "Rosacea", "Shingles", "Urticaria", "Diaper Rash",
                              "Seborrheic Dermatitis", "Ringworm", "Conjunctivitis"],
            "Allergist/Immunologist": ["Allergy", "Drug Reaction", "Urticaria"],
            "Gastroenterologist": ["GERD", "Chronic cholestasis", "Peptic ulcer disease", "Gastroenteritis", 
                                   "Jaundice", "hepatitis A", "Hepatitis B", "Hepatitis C", "Hepatitis D", 
                                   "Hepatitis E", "Alcoholic hepatitis", "Dimorphic hemmorhoids(piles)",
                                   "IBS", "Gastritis", "Food Poisoning", "Peptic Ulcer"],
            "Endocrinologist": ["Diabetes", "Hypothyroidism", "Hyperthyroidism", "Hypoglycemia", "PCOS"],
            "Pulmonologist": ["Bronchial Asthma", "Pneumonia", "Tuberculosis", "COPD", "Post-viral Cough"],
            "Cardiologist": ["Hypertension", "Heart attack", "Angina", "Palpitations"],
            "Neurologist": ["Migraine", "Paralysis (brain hemorrhage)", "(vertigo) Paroymsal Positional Vertigo",
                           "Tension Headache", "Cervical Radiculopathy", "Vertigo", "Meningitis"],
            "Infectious Disease Specialist": ["Malaria", "Dengue", "Typhoid", "AIDS", "Viral Fever", "Flu", "COVID-19", "Tuberculosis"],
            "Rheumatologist": ["Osteoarthritis", "Arthritis", "Cervical spondylosis", "Sciatica"],
            "Urologist": ["Urinary tract infection", "Urinary Tract Infection", "Kidney Stones"],
            "Vascular Surgeon": ["Varicose veins"],
            "ENT Specialist": ["Sinusitis", "Tonsillitis", "Pharyngitis", "Otitis Media"],
            "Orthopedic": ["Muscle Strain", "Sciatica", "Arthritis"],
            "Pediatrician": ["Diaper Rash", "Otitis Media", "Hand Foot Mouth Disease"],
            "Gynecologist": ["PCOS"],
            "General Physician": ["Common Cold", "Viral Fever", "Flu", "Gastroenteritis", "Food Poisoning", "Anemia"],
            "Ophthalmologist": ["Conjunctivitis"],
            "Hematologist": ["Anemia"]
        }
        
        # Global Aliases for Text Normalization (English + Hinglish)
        # Strategic "Greedy" Mapping: One phrase can map to multiple canonical terms to boost confidence
        self.global_aliases = {
            # ========== SKIN / DERMATOLOGY ==========
            # Itching variations
            "khujli": "itching", "kharish": "itching", "itchy": "itching", "itch": "itching",
            "scratchy": "itching", "pruritus": "itching", "khujli ho rahi": "itching",
            "irritated skin": "itching", "wants to scratch": "itching",
            
            # Rash variations
            "laal daane": "rash red skin", "daane": "rash", "gol daag": "ring shaped rash scaly border",
            "rash": "rash", "red spots": "rash", "skin eruption": "rash",
            "round rash": "ring shaped rash scaly border itching", "circular rash": "ring shaped rash scaly border",
            "ring rash": "ring shaped rash scaly border", "ringworm": "ring shaped rash scaly border",
            "round itchy": "ring shaped rash itching scaly border",
            
            # Psoriasis
            "silvery scales": "silvery scales thick plaques", "white flaky": "silvery scales chronic scaly rash thick plaques",
            "silvery": "silvery scales thick plaques", "white scale": "silvery scales thick plaques",
            "silver scale": "silvery scales", "thick skin": "thick plaques", "hard patch": "thick plaques",
            "scaly rash": "chronic scaly rash scaly border", "old rash": "chronic scaly rash",
            "peeling": "peeling", "skin peeling": "peeling",
            
            # Eczema
            "dry patches": "dry itchy patches", "cracked skin": "cracked skin", "red inflamed": "red inflamed skin",
            "sookhi chamdi": "dry itchy patches", "phati hui skin": "cracked skin",
            "itchy patches": "dry itchy patches",
            "dry itchy patches": "dry itchy patches",
            "dry skin patches": "dry itchy patches",
            
            # Acne
            "pimple": "pimples", "muhase": "pimples", "blackhead": "blackheads", "whitehead": "whiteheads",
            "zit": "pimples", "breakout": "pimples", "acne": "pimples",
            
            # ========== RESPIRATORY ==========
            # Breathing
            "saans phoolna": "wheezing breathlessness shortness of breath",
            "saans phool rahi": "wheezing breathlessness shortness of breath",
            "saans phool": "wheezing breathlessness shortness of breath",
            "saans nahi aa rahi": "shortness of breath breathlessness",
            "saans lene me takleef": "shortness of breath breathlessness",
            "saans ruk rahi": "shortness of breath", "dum ghutna": "breathlessness",
            "breathlessness": "wheezing breathlessness shortness of breath",
            "shortness of breath": "breathlessness shortness of breath",
            "cant breathe": "shortness of breath", "difficulty breathing": "shortness of breath",
            "sob": "shortness of breath", "breathless": "breathlessness",
            
            # Wheezing
            "wheezing": "wheezing", "whistling breath": "wheezing", "saans me siti": "wheezing",
            "siti": "wheezing", "noisy breathing": "wheezing", "weezing": "wheezing",
            
            # Cough
            "cough": "cough", "khansi": "cough", "khaansi": "cough",
            "productive cough": "productive cough mucus production", "balgam": "productive cough mucus production",
            "wet cough": "productive cough", "phlegm": "productive cough mucus production",
            "dry cough": "persistent dry cough cough", "sookhi khansi": "persistent dry cough cough",
            "dry cough for": "persistent dry cough cough after cold",
            "coughing": "cough", "hacking": "cough", "chronic cough": "chronic cough",
            
            # Throat
            "gala dard": "sore throat", "sore throat": "sore throat", "throat pain": "sore throat throat pain",
            "gala jal raha": "sore throat burning", "strep throat": "sore throat",
            "painful swallowing": "difficulty swallowing painful swallowing", "nigalne me takleef": "difficulty swallowing",
            
            # Nasal
            "naak band": "nasal congestion", "nasal congestion": "nasal congestion", "blocked nose": "nasal congestion",
            "runny nose": "runny nose", "naak behna": "runny nose", "stuffy nose": "nasal congestion",
            "sinus": "facial pain nasal congestion", "sinusitis": "facial pain nasal congestion thick nasal discharge",
            
            # ========== GASTROINTESTINAL ==========
            # Abdominal pain
            "pet dard": "abdominal pain abdominal cramping", "stomach ache": "abdominal pain",
            "abdominal pain": "abdominal pain", "tummy ache": "abdominal pain",
            "pet me dard": "abdominal pain stomach cramps", "stomach pain": "abdominal pain upper abdominal pain stomach burning",
            "cramps": "abdominal cramping stomach cramps", "cramping": "abdominal cramping stomach cramps",
            
            # Digestion
            "heartburn": "heartburn acid reflux", "acid reflux": "heartburn acid reflux",
            "burning chest": "heartburn burning chest", "seene me jalan": "heartburn burning chest",
            "acid in throat": "acid reflux regurgitation", "khatta pani": "regurgitation",
            "acidity": "heartburn acid reflux", "indigestion": "indigestion bloating",
            "gas": "bloating gas", "bloating": "bloating gas", "pet phulna": "bloating",
            "afara": "bloating gas", "after spicy food": "heartburn", "after eating": "heartburn",
            
            # Vomiting/Nausea
            "ulti": "vomiting sudden vomiting", "vomit": "vomiting", "vomiting": "vomiting sudden vomiting",
            "nausea": "nausea", "ji machlana": "nausea", "feeling sick": "nausea",
            "nausia": "nausea", "throwing up": "vomiting",
            
            # Diarrhea
            "dast": "diarrhea watery diarrhea abdominal cramps", "loose motion": "diarrhea abdominal cramps", "loose stool": "diarrhea",
            "diarrhea": "diarrhea watery diarrhea", "diarhea": "diarrhea", "runny tummy": "diarrhea",
            "pet kharab": "diarrhea abdominal cramps nausea", "loose motions": "diarrhea abdominal cramps",
            
            # Constipation
            "constipation": "constipation", "qabz": "constipation", "kabz": "constipation",
            
            # ========== URINARY (HINGLISH) ==========
            "peshab me jalan": "burning urination frequent urination urinary urgency",
            "peshab mein jalan": "burning urination frequent urination",
            "peshab me dard": "burning urination pelvic pain", 
            "jalan peshab": "burning urination",
            
            # ========== SKIN (HINGLISH) ==========
            "khujli aur laal daane": "itching red rash skin rash hives",
            "laal daane": "red rash skin rash hives",
            "lal dane": "red rash skin rash",
            
            # ========== FEVER / GENERAL ==========
            "fever": "fever", "bukhaar": "fever", "bukhar": "fever",
            "high fever": "high fever fever", "tez bukhaar": "high fever",
            "body hot": "fever", "temperature": "fever", "pyrexia": "fever",
            "chills": "chills", "thand": "chills", "kapkapi": "chills", "kaapna": "chills",
            "bukhar aur sir dard": "fever headache body aches",
            "bukhar sir dard": "fever headache",
            "rigor": "chills and rigors", "shivering": "chills",
            "fatigue": "fatigue", "thakan": "fatigue", "weakness": "weakness fatigue",
            "kamzori": "weakness fatigue", "tired": "fatigue", "exhausted": "extreme fatigue",
            "body aches": "body aches muscle aches", "badan dard": "body aches muscle pain",
            
            # ========== PAIN SYNONYMS ==========
            "pain": "pain", "dard": "pain", "ache": "pain", "soreness": "pain tenderness",
            "discomfort": "discomfort", "throbbing": "throbbing", "sharp pain": "severe pain",
            "dull pain": "pain", "burning": "burning sensation",
            "tenderness": "tenderness", "stiffness": "stiffness joint stiffness",
            "akdan": "stiffness",
            
            # ========== HEADACHE / NEURO ==========
            "headache": "headache", "sir dard": "headache", "sar dard": "headache",
            "migraine": "throbbing headache one sided head pain severe headache",
            "head pain": "headache", "tension headache": "band like head pain pressure around head",
            "dizziness": "dizziness loss of balance nausea", "chakkar": "dizziness nausea",
            "vertigo": "spinning sensation room spinning nausea", "giddiness": "dizziness nausea",
            "lightheaded": "dizziness", "sir ghoom raha": "dizziness spinning sensation",
            "dizziness with headache": "throbbing headache dizziness nausea sensitivity to light",
            "one sided": "one sided head pain one sided headache",
            
            # ========== EMERGENCY TERMS ==========
            "unconscious": "unconscious", "behosh": "unconscious", "collapsed": "unconscious collapsed",
            "fainting": "unconscious fainting", "gir gaya": "unconscious",
            "chest pain": "chest pain chest discomfort", "seene me dard": "chest pain",
            "thoracic pain": "chest pain", "dil me dard": "chest pain",
            "sudden": "sudden", "ek dum se": "sudden", "achanak": "sudden",
            "slurred speech": "slurred speech", "bolne me takleef": "slurred speech",
            "facial droop": "facial droop", "muh tedha": "facial droop",
            "one side weak": "one side weak arm weakness", "ek side kamzori": "one side weak",
            
            # ========== URINARY ==========
            "burning urination": "burning urination", "peshab me jalan": "burning urination",
            "frequent urination": "frequent urination", "baar baar peshab": "frequent urination",
            "uti": "burning urination frequent urination urinary urgency",
            "urine infection": "burning urination frequent urination",
            
            # ========== EYE / EAR ==========
            "eye irritation": "eye irritation watery eyes", "aankh me jalan": "eye irritation",
            "watery eyes": "watery eyes", "red eyes": "eye irritation",
            "ear pain": "ear pain", "kaan dard": "ear pain", "earache": "ear pain",
            
            # ========== WOMEN HEALTH ==========
            "irregular periods": "irregular periods", "mahwari problem": "irregular periods",
            "period irregular": "irregular periods", "pcod": "irregular periods polycystic ovaries",
            "pcos": "irregular periods excess hair growth polycystic ovaries",
            
            # ========== MISSPELLINGS ==========
            "nausia": "nausea", "diarhea": "diarrhea", "diarrhoea": "diarrhea",
            "weezing": "wheezing", "brething": "breathing", "headach": "headache",
            "stomache": "stomach", "throbing": "throbbing", "itchiness": "itching",
            "fevar": "fever", "fevr": "fever", "cof": "cough", "koff": "cough",
            
            # ========== PEDIATRIC ==========
            "baby rash": "rash red irritated diaper area", "diaper rash": "red irritated diaper area",
            "ear tugging": "ear pain ear tugging", "fussiness": "irritability in child fussiness",
            "irritable child": "irritability in child", "mouth sores": "mouth sores",
            
            # ========== JOINT / MUSCLE ==========
            "joint pain": "joint pain joint swelling", "jodo me dard": "joint pain",
            "arthritis": "joint pain joint swelling joint stiffness", "gathiya": "joint pain arthritis",
            "muscle pain": "muscle pain muscle aches", "muscle strain": "muscle pain muscle tenderness",
            "back pain": "lower back pain radiating to leg back pain", "kamar dard": "lower back pain",
            "neck pain": "neck pain neck stiffness", "gardan dard": "neck pain",
            
            # ========== ADDITIONAL HINGLISH & PATIENT-FRIENDLY ==========
            # Burning sensation
            "jal raha": "burning burning sensation", "jal raha hai": "burning burning sensation",
            "jalन": "burning",
            
            # Dermatology - Fungal / Ring rash
            "gol daane": "ring shaped rash scaly border itching", "gol rash": "ring shaped rash scaly border",
            "itchy round rash": "ring shaped rash itching scaly border",
            "round itchy rash": "ring shaped rash itching scaly border",
            "spreading rash": "rash ring shaped rash", "itchy rash spreading": "ring shaped rash itching scaly border",
            "rash spreading": "ring shaped rash itching",
            
            # Dermatology - Psoriasis
            "scaly plaque": "silvery scales thick plaques chronic scaly rash",
            "scaly plaques": "silvery scales thick plaques chronic scaly rash",
            "thick scaly patches": "thick plaques silvery scales chronic scaly rash",
            "papdi wali chamdi": "silvery scales thick plaques",
            
            # UTI / Urinary
            "pelvic pain": "pelvic pain urinary urgency",
            "jalan with peshab": "burning urination pelvic pain",
            "peshab mein jalan": "burning urination",
            
            # Hyperthyroidism
            "weight loss with fast heartbeat": "weight loss rapid heartbeat heat intolerance",
            "fast heart rate": "rapid heartbeat", "racing heart": "rapid heartbeat",
            "fast heartbeat": "rapid heartbeat", "heart racing": "rapid heartbeat",
            "heat intolerant": "heat intolerance",
            "tez dhadkan": "rapid heartbeat", "dil tez": "rapid heartbeat",
            "garmi bardaasht nahi": "heat intolerance", "garmi se pareshani": "heat intolerance",
            
            # Dengue / Mosquito fever
            "mosquito fever": "high fever severe headache pain behind eyes joint pain",
            "macchar se bukhar": "high fever severe headache pain behind eyes joint pain",
            "machhar": "high fever pain behind eyes", "macchar": "high fever pain behind eyes",
            "aankh ke peeche dard": "pain behind eyes", "eyes ke peeche": "pain behind eyes",
            "mosquito bite fever": "high fever pain behind eyes joint pain",
            
            # Common Cold
            "cold symptoms": "runny nose sneezing sore throat",
            "nazla": "runny nose nasal congestion", "zukam": "runny nose sneezing nasal congestion",
            "common cold": "runny nose sneezing sore throat",
            "thand lag gayi": "runny nose sneezing cough",
            
            # Osteoarthritis
            "old age joint pain": "joint pain joint stiffness morning stiffness",
            "ghutno mein dard": "joint pain joint stiffness", "ghutne mein dard": "joint pain joint stiffness",
            "joint pain worse in morning": "joint pain morning stiffness joint stiffness",
            "subah akdan": "morning stiffness joint stiffness",
            
            # ========== COVID-19 ==========
            "corona": "fever dry cough loss of taste loss of smell shortness of breath",
            "covid": "fever dry cough loss of taste loss of smell",
            "loss of smell": "loss of smell", "loss of taste": "loss of taste",
            "soonghne ki shakti khatam": "loss of smell", "taste nahi pata": "loss of taste",
            
            # ========== TUBERCULOSIS ==========
            "tb symptoms": "persistent cough night sweats unexplained weight loss",
            "persistent cough": "persistent cough", "night sweats": "night sweats",
            "raat ko pasina": "night sweats", "bina wajan kam": "unexplained weight loss",
            "khoon thookna": "coughing blood", "coughing blood": "coughing blood",
            
            # ========== HEPATITIS / JAUNDICE ==========
            "piliya": "jaundice yellow skin yellow eyes dark urine",
            "peeli skin": "yellow skin jaundice", "peeli aankh": "yellow eyes jaundice",
            "yellow skin": "yellow skin jaundice", "yellow eyes": "yellow eyes jaundice",
            "dark urine": "dark urine", "dark peshab": "dark urine",
            "liver disease": "jaundice fatigue abdominal pain",
            
            # ========== MENINGITIS ==========
            "stiff neck": "stiff neck", "gardan akad": "stiff neck",
            "gardan mein dard": "stiff neck", "neck stiffness": "stiff neck",
            
            # ========== ANEMIA ==========
            "pale skin": "pale skin weakness fatigue",
            "khoon ki kami": "fatigue pale skin weakness shortness of breath",
            "anemia symptoms": "fatigue pale skin weakness",
            "kamzori aur thakan": "fatigue weakness",
            
            # ========== CONJUNCTIVITIS ==========
            "pink eye": "red eye eye discharge itchy eyes",
            "aankh laal": "red eye", "red eye": "red eye",
            "eye discharge": "eye discharge", "aankh se paani": "watery eyes eye discharge",
            "itchy eyes": "itchy eyes", "aankh mein khujli": "itchy eyes",
            "eye infection": "red eye eye discharge",
            
            # ========== DANDRUFF / SCALP ==========
            "dandruff": "dandruff flaky scalp itchy scalp",
            "roosi": "dandruff flaky scalp", "sir mein khujli": "itchy scalp dandruff",
            "scalp problem": "dandruff itchy scalp flaky scalp",
            "baal jhadna": "hair loss", "hair fall": "hair loss",
            
            # ========== DERMATITIS / SKIN IRRITATION ==========
            "itchy skin": "itching rash dry itchy patches",
            "red patches": "red patches rash itching",
            "skin irritation": "skin irritation after contact localized rash",
            "skin rash": "rash itching red patches",
            "itchy red patches": "dry itchy patches red inflamed skin",
            "khujli": "itching rash",
            "laal daag": "red patches rash",
            
            # ========== RINGWORM specific ==========
            "ring rash": "ring shaped rash circular rash scaly border",
            "circular rash": "ring shaped rash circular rash scaly border",
            "daad": "ring shaped rash circular rash itching",
            "gol daad": "ring shaped rash circular rash scaly border",
            
            # ========== JAUNDICE differentiation ==========
            "yellow skin yellow eyes": "yellow skin yellow eyes jaundice",
            "jaundice symptoms": "yellow skin yellow eyes dark urine jaundice",
            
            # ========== PNEUMONIA ==========
            "high fever cough": "high fever with cough fever with cough",
            "cough high fever": "cough with high fever high fever with cough",
            "fever cough": "fever with cough high fever with cough",
            "cough fever": "cough with high fever fever with cough",
            "severe cough fever": "productive cough high fever with cough",
            "lung infection": "lung infection chest infection productive cough"
        }
        
        # Plural to Singular Mapping for simple normalization
        self.plurals = {
            # Skin
            "rashes": "rash", "blisters": "blister", "patches": "patch", "sores": "sore",
            "scales": "scale", "pimples": "pimple", "bumps": "bump", "spots": "spot",
            "lesions": "lesion", "welts": "welt", "wheals": "wheal",
            
            # Body Parts
            "eyes": "eye", "ears": "ear", "joints": "joint", "muscles": "muscle",
            "fingers": "finger", "toes": "toe", "legs": "leg", "arms": "arm",
            
            # Symptoms
            "headaches": "headache", "aches": "ache", "pains": "pain", "cramps": "cramp",
            "coughs": "cough", "sneezes": "sneeze", "chills": "chill",
            "fevers": "fever", "infections": "infection",
            
            # Actions
            "vomits": "vomit", "itches": "itch", "burns": "burn",
            
            # Grammar variations
            "motions": "motion", "movements": "movement", "episodes": "episode",
            "attacks": "attack", "flares": "flare"
        }
        
    def normalize_text(self, text):
        return text.lower().strip()

    def normalize_user_text(self, text):
        """
        Industry-grade normalization: handles Hinglish, grammar, and synonyms.
        """
        text = self.normalize_text(text)
        
        # 0. Pre-process compound phrases (handles multi-word Hinglish patterns)
        phrase_fixes = [
            (r"saans\s*phool\s*rahi", "saans phoolna"),
            (r"jal\s*raha\s*hai", "burning"),
            (r"gol\s+daane", "ring shaped rash"),
            (r"itchy\s+round\s+rash", "ring shaped rash itching"),
            (r"round\s+itchy\s+rash", "ring shaped rash itching"),
            (r"rash\s+spreading", "ring shaped rash itching"),
            (r"spreading\s+rash", "ring shaped rash"),
            (r"weight\s+loss.*?fast\s+heart", "weight loss rapid heartbeat"),
            (r"fast\s+heart.*?weight\s+loss", "weight loss rapid heartbeat"),
            (r"burning\s+urin.*?pelvic", "burning urination pelvic pain"),
            (r"pelvic.*?burning\s+urin", "burning urination pelvic pain"),
            (r"mosquito.*?fever", "high fever pain behind eyes joint pain"),
            (r"fever.*?mosquito", "high fever pain behind eyes joint pain"),
        ]
        for pattern, replacement in phrase_fixes:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # 1. Handle Plurals/Variations
        words = text.split()
        normalized_words = [self.plurals.get(word, word) for word in words]
        text = " ".join(normalized_words)
        
        # 2. Map Global Aliases (Hinglish + Synonyms)
        # We sort by length descending to replace longer phrases first
        sorted_aliases = sorted(self.global_aliases.items(), key=lambda x: len(x[0]), reverse=True)
        for alias, canonical in sorted_aliases:
            # Check for alias in text using word boundaries for safety but allow simple replace for common Hinglish
            if len(alias) > 3:
                text = re.sub(rf'\b{re.escape(alias)}\b', canonical, text)
            else:
                text = text.replace(alias, canonical)
            
        return text

    def match_symptom(self, canonical, user_text):
        """
        Helper to match a canonical symptom or any of its aliases.
        """
        # Direct match
        if canonical in user_text:
            return True
        
        # Alias match
        aliases = self.symptom_aliases.get(canonical, [])
        for alias in aliases:
            if alias in user_text:
                return True
        
        return False

    def check_red_flags(self, user_symptoms):
        """
        Check for emergency conditions with robust keyword matching.
        """
        text = user_symptoms # Already normalized by run_analysis
        
        # Rule 1: Cardiac Emergency (BALANCED)
        # Chest pain alone is NOT an emergency (could be GERD, muscle strain, anxiety, Pneumonia)
        # Triggers when chest pain is accompanied by CARDIAC warning signs
        # IMPORTANT: If cough/productive respiratory symptoms present → likely Pneumonia NOT cardiac
        has_chest_pain = "chest" in text and ("pain" in text or "pressure" in text or "tightness" in text)
        
        # Check if this is likely PRODUCTIVE respiratory (Pneumonia) rather than cardiac
        # Note: shortness of breath can be cardiac OR respiratory - don't exclude on that alone
        is_productive_respiratory = "cough" in text or "mucus" in text or "phlegm" in text or "wheezing" in text
        
        cardiac_warning_signs = False
        if has_chest_pain:
            # Classic heart attack signs - ALWAYS trigger even if some respiratory overlap
            # These are DEFINITIVE cardiac indicators
            if ("left arm" in text) or ("arm" in text and ("pain" in text or "spreading" in text)) or "radiating" in text:
                cardiac_warning_signs = True
            elif "jaw" in text and ("pain" in text or "spreading" in text):
                cardiac_warning_signs = True
            elif "back" in text and "pain" in text and "spreading" in text:
                cardiac_warning_signs = True
            elif "crushing" in text or "squeezing" in text or "severe" in text:
                cardiac_warning_signs = True
            elif "cold sweat" in text or ("sweating" in text and "chest" in text) or ("sweat" in text and "nausea" in text):
                cardiac_warning_signs = True
            elif "nausea" in text and ("arm" in text or "jaw" in text or "dizz" in text):
                cardiac_warning_signs = True
            elif "sudden" in text and ("weakness" in text or "dizz" in text):
                cardiac_warning_signs = True
            # Shortness of breath with chest pain is cardiac IF no productive cough
            elif ("shortness of breath" in text or "breathless" in text) and not is_productive_respiratory:
                cardiac_warning_signs = True
        
        # Palpitations with breathing issues is also concerning (but not if productive cough)
        palpitations_emergency = "palpitations" in text and ("breath" in text or "unconscious" in text) and not is_productive_respiratory
        
        if cardiac_warning_signs or palpitations_emergency:
            return True, "Cardiologist", "Red Flag: Potential Cardiac Emergency detected (Chest pain with warning signs)."
            
        # Rule 2: Stroke Signs
        if ("weakness" in text and "sudden" in text) or "slurred" in text or "droop" in text or "facial" in text:
             if "slurred speech" in text or "facial droop" in text or ("one side" in text and "weak" in text):
                return True, "Neurologist", "Red Flag: Potential Stroke signs detected."

        # Rule 3: Respiratory Emergency
        # STRICTER: Breathlessness must be accompanied by severe signs
        # Prevents false positives for Asthma/Pneumonia
        has_sob = "shortness of breath" in text
        
        sob_emergency = False
        if has_sob:
            # Only trigger if accompanied by CRITICAL severity indicators (not just "severe" or "sudden")
            # These are truly life-threatening signs, NOT typical asthma/pneumonia symptoms
            if (("chest" in text and "pain" in text and "radiating" in text)) or \
               ("blue" in text and "lips" in text) or \
               "cyanosis" in text or \
               "unconscious" in text or \
               "collapse" in text or \
               ("gasping" in text) or \
               ("cannot" in text and "breath" in text):
                sob_emergency = True

        # Cyanosis with wheezing is always critical
        if sob_emergency or \
           ("blue" in text and "lips" in text) or \
           ("wheezing" in text and "cyanosis" in text):
            return True, "Pulmonologist", "Red Flag: Severe Respiratory Distress (Breathlessness with critical signs)."

        # Rule 4: General Emergency
        if "unconscious" in text or "fainting" in text or "collapsed" in text:
             return True, "General Physician", "Red Flag: Loss of consciousness."

        # Rule 5: Meningitis Emergency
        if ("stiff neck" in text or "neck stiffness" in text) and \
           ("high fever" in text or "fever" in text) and \
           ("sensitivity to light" in text or "headache" in text):
            return True, "Neurologist", "Red Flag: Potential Meningitis - Requires immediate medical attention."

        return False, None, ""

    def check_rules(self, user_symptoms):
        """
        Validates symptoms against strictly defined Primary + Supporting rules.
        Calculates a deterministic confidence score based on weighted matching.
        
        Formula:
          Score = (Primary_Match_Ratio * 0.7) + (Supporting_Match_Ratio * 0.3)
        
        Returns: List of allowed diseases (names only) and the top candidate's full metadata.
        """
        text = self.normalize_text(user_symptoms)
        candidates = []

        for disease, rules in self.disease_rules.items():
            # 1. Exclusions (Discard immediately)
            if any(excl in text for excl in rules["exclusions"]):
                continue

            # 2. Symptom Matching (NLP Aware)
            primary_matches = [p for p in rules["primary"] if self.match_symptom(p, text)]
            supporting_matches = [s for s in rules["supporting"] if self.match_symptom(s, text)]

            # 3. Acceptance Criteria:
            # - At least 1 primary match
            # OR
            # - At least 2 supporting matches (NLP fallback for descriptive patients)
            if not primary_matches and len(supporting_matches) < 2:
                continue

            # 4. Calculate Scores (Deterministic)
            # Primary Calculation (Weight: 0.7)
            total_primary = len(rules["primary"])
            p_ratio = len(primary_matches) / total_primary if total_primary > 0 else 0

            # Supporting Calculation (Weight: 0.3)
            # supporting_matches already calculated above
            total_supporting = len(rules["supporting"])
            s_ratio = len(supporting_matches) / total_supporting if total_supporting > 0 else 0

            # Weighted Confidence Score
            primary_weight = 0.7
            supporting_weight = 0.3
            confidence_score = (p_ratio * primary_weight) + (s_ratio * supporting_weight)

            # 4. Confidence Level Mapping
            if confidence_score >= 0.75:
                # 0.75+ -> Strong match
                confidence_level = "HIGH"
            elif confidence_score >= 0.40:
                # 0.40+ -> Decent match
                confidence_level = "MEDIUM"
            else:
                # < 0.40 -> Weak evidence
                confidence_level = "LOW"
            
            # UX Feature: Calculate missing important symptoms for explanation
            missing_primary = [p for p in rules["primary"] if p not in primary_matches]
            
            candidates.append({
                "disease": disease,
                "confidence_level": confidence_level,
                "confidence_score": confidence_score,
                "score": confidence_score,
                # Explanation data (for UI display - does not affect scoring)
                "matched_primary": primary_matches,
                "matched_supporting": supporting_matches,
                "missing_primary": missing_primary[:3]  # Limit to top 3 for UI
            })

        # Sort by Score (Highest first)
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # Limit to Top 2
        top_candidates = candidates[:2]
        
        allowed_names = [c["disease"] for c in top_candidates]
        
        # Extract top candidate metadata for return
        if top_candidates:
            top_meta = top_candidates[0]
            return allowed_names, top_meta
        else:
            return [], None

    def get_specialist(self, disease):
        for specialist, diseases in self.specialist_map.items():
            if disease in diseases:
                return specialist
        return "General Physician"

    def run_analysis(self, user_symptoms):
        """
        Main entry point. 
        Returns strict payload with ALL mandated keys.
        """
        # 0. UNIVERSAL NORMALIZATION (Industry Header)
        normalized_text = self.normalize_user_text(user_symptoms)
        
        # 1. Red Flags (Emergency Override) - EXECUTE FIRST
        # Emergency is always HIGH confidence (1.0)
        is_emergency, forced_spec, reason = self.check_red_flags(normalized_text)
        
        if is_emergency:
            # Emergency override — never downgrade confidence
            confidence_level = "HIGH"
            confidence_score = 1.0
            
            # Defensive Assertion: Ensure Emergency is ALWAYS HIGH
            assert not (is_emergency and confidence_level != "HIGH"), "Critical Safety Violation: Emergency detected but confidence not HIGH"
            
            # HARD EARLY RETURN
            return {
                "disease": "EMERGENCY ALERT", # Requested Key
                "confidence_score": confidence_score,
                "confidence_level": confidence_level,
                "reason": reason,
                "forced_specialist": forced_spec,
                "is_emergency": True,
                
                # Validation / Legacy Keys
                "block_prediction": True,
                "emergency": True,
                "allowed_diseases": []
            }
            
        # 2. SHORT INPUT DETECTION (Single non-specific symptoms)
        # If input is very short (1-2 words), likely too vague for confident prediction
        # Force General Physician to avoid false positives from BERT
        word_count = len(normalized_text.split())
        non_specific_terms = ["fatigue", "tired", "tiredness", "weakness", "weak", "fever", 
                              "headache", "pain", "ache", "nausea", "dizziness", "dizzy",
                              "unwell", "sick", "malaise", "not feeling well", "feeling sick"]
        
        is_non_specific_single = word_count <= 3 and any(term in normalized_text for term in non_specific_terms)
        
        if is_non_specific_single:
            fallback_disease = "General Physician Consultation"
            confidence_level = "LOW"
            confidence_score = 0.20
            reason = f"'{user_symptoms.strip()}' is too non-specific for a confident diagnosis. Please describe more symptoms or consult a General Physician."
            
            return {
                "disease": fallback_disease,
                "confidence_score": confidence_score,
                "confidence_level": confidence_level,
                "reason": reason,
                "forced_specialist": "General Physician",
                "is_emergency": False,
                
                # Validation / Legacy Keys
                "block_prediction": False,
                "emergency": False,
                "allowed_diseases": [fallback_disease]
            }
            
        # 3. Symptom Rules Validation (Only runs if NOT emergency and NOT short input)
        allowed_diseases, best_match_meta = self.check_rules(normalized_text)
        
        # 4. Fallback (No Match Found)
        if not allowed_diseases or not best_match_meta:
            fallback_disease = "General Physician Consultation"
            confidence_level = "LOW"
            confidence_score = 0.25
            reason = "Symptoms are non-specific and do not form a strong clinical pattern."
            
            return {
                "disease": fallback_disease,
                "confidence_score": confidence_score,
                "confidence_level": confidence_level,
                "reason": reason,
                "forced_specialist": "General Physician",
                "is_emergency": False,
                
                # Validation / Legacy Keys
                "block_prediction": False,
                "emergency": False,
                "allowed_diseases": [fallback_disease]
            }
            
        # 4. Successful Match (Disease Found)
        best_disease = allowed_diseases[0]
        confidence_level = best_match_meta["confidence_level"]
        confidence_score = best_match_meta["confidence_score"]
        
        return {
            "disease": best_disease,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "reason": f"Matched {len(allowed_diseases)} disease(s) based on clinical rules. Primary match indicates {confidence_level} confidence.",
            "forced_specialist": None,
            "is_emergency": False,

            # Validation / Legacy Keys
            "block_prediction": False,
            "emergency": False,
            "allowed_diseases": allowed_diseases,
            
            # UX Feature: Explanation data for "Why this diagnosis?" panel
            "matched_primary": best_match_meta.get("matched_primary", []),
            "matched_supporting": best_match_meta.get("matched_supporting", []),
            "missing_primary": best_match_meta.get("missing_primary", [])
        }

    def apply_demographic_context(self, analysis_result, age=None, gender=None):
        """
        POST-PROCESSING ONLY: Adjusts confidence score based on age/gender context.
        
        CRITICAL CONSTRAINTS:
        - NEVER changes the predicted disease
        - NEVER affects emergency cases
        - Only adjusts confidence_score by ±0.05 to ±0.15 max
        - Returns original result unchanged if age/gender not provided
        
        Args:
            analysis_result: The result dict from run_analysis()
            age: Optional integer age (None = skip adjustment)
            gender: Optional string 'male'/'female'/'other' (None = skip adjustment)
            
        Returns:
            Modified analysis_result with adjusted confidence (disease unchanged)
        """
        # SAFETY: If no demographics provided, return unchanged
        if age is None and gender is None:
            return analysis_result
        
        # SAFETY: Never modify emergency cases
        if analysis_result.get('is_emergency') or analysis_result.get('emergency'):
            return analysis_result
        
        # SAFETY: Never modify General Physician fallback
        if "General Physician" in analysis_result.get('disease', ''):
            return analysis_result
        
        disease = analysis_result.get('disease', '')
        original_score = analysis_result.get('confidence_score', 0.5)
        adjustment = 0.0
        adjustment_reasons = []
        
        # Normalize gender
        gender_lower = gender.lower() if gender else None
        
        # ========== AGE-BASED ADJUSTMENTS ==========
        if age is not None:
            try:
                age = int(age)
                
                # Elderly (65+) - higher risk for chronic conditions
                if age >= 65:
                    elderly_diseases = ["Osteoarthritis", "COPD", "Hypertension", "Heart Disease", 
                                       "Diabetes", "Hypothyroidism", "Cervical Spondylosis"]
                    if disease in elderly_diseases:
                        adjustment += 0.10
                        adjustment_reasons.append(f"age ≥65 increases likelihood of {disease}")
                
                # Middle-aged (45-64) - common for degenerative conditions
                elif age >= 45:
                    middle_age_diseases = ["Osteoarthritis", "Hypertension", "PCOS", "Hypothyroidism", 
                                          "Diabetes", "Migraine"]
                    if disease in middle_age_diseases:
                        adjustment += 0.08
                        adjustment_reasons.append(f"age 45-64 is typical for {disease}")
                
                # Young adults (18-30) - certain conditions more common
                elif 18 <= age <= 30:
                    young_adult_diseases = ["Acne", "PCOS", "Migraine", "Anxiety", "Depression",
                                           "Viral Fever", "Common Cold"]
                    if disease in young_adult_diseases:
                        adjustment += 0.05
                        adjustment_reasons.append(f"age 18-30 aligns with typical {disease} demographics")
                
                # Children/Teens (<18) - pediatric considerations
                elif age < 18:
                    pediatric_diseases = ["Dengue", "Viral Fever", "Common Cold", "Tonsillitis", 
                                         "Conjunctivitis", "Chicken Pox"]
                    if disease in pediatric_diseases:
                        adjustment += 0.07
                        adjustment_reasons.append(f"pediatric age increases {disease} likelihood")
                    
                    # Suppress adult-onset diseases for children
                    adult_onset_diseases = ["Osteoarthritis", "COPD", "Cervical Spondylosis", 
                                           "Heart Disease", "PCOS"]
                    if disease in adult_onset_diseases:
                        adjustment -= 0.10
                        adjustment_reasons.append(f"{disease} is rare in pediatric patients")
                        
            except (ValueError, TypeError):
                pass  # Invalid age, skip age adjustment
        
        # ========== GENDER-BASED ADJUSTMENTS ==========
        if gender_lower in ['female', 'f']:
            female_predominant = {
                "UTI": 0.12,  # 8x more common in females
                "PCOS": 0.15,  # Female-only
                "Migraine": 0.08,  # 3x more common
                "Hypothyroidism": 0.08,  # 5-8x more common
                "Hyperthyroidism": 0.06,
                "Osteoporosis": 0.10,
                "Urticaria": 0.05,
            }
            if disease in female_predominant:
                adjustment += female_predominant[disease]
                adjustment_reasons.append(f"{disease} is more common in females")
                
        elif gender_lower in ['male', 'm']:
            male_predominant = {
                "Gout": 0.10,  # 3-4x more common in males
                "Heart Disease": 0.08,
                "COPD": 0.06,  # Due to smoking prevalence
                "Kidney Stones": 0.08,
            }
            if disease in male_predominant:
                adjustment += male_predominant[disease]
                adjustment_reasons.append(f"{disease} is more common in males")
        
        # ========== APPLY ADJUSTMENT WITH SAFETY CAPS ==========
        # Cap adjustment to ±0.15 max as per industry standard
        adjustment = max(-0.15, min(0.15, adjustment))
        
        new_score = original_score + adjustment
        
        # Cap final score between 0.0 and 1.0
        new_score = max(0.0, min(1.0, new_score))
        
        # Update confidence level based on new score
        if new_score >= 0.75:
            new_level = "HIGH"
        elif new_score >= 0.40:
            new_level = "MEDIUM"
        else:
            new_level = "LOW"
        
        # Build result (disease UNCHANGED)
        result = analysis_result.copy()
        result['confidence_score'] = round(new_score, 2)
        result['confidence_level'] = new_level
        
        if adjustment_reasons:
            original_reason = result.get('reason', '')
            demographic_note = f" [Demographic context: {'; '.join(adjustment_reasons)}]"
            result['reason'] = original_reason + demographic_note
            result['demographic_adjustment'] = round(adjustment, 2)
        
        return result
