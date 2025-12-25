# MediSense – Intelligent Medical Diagnosis & Appointment Platform

MediSense is a comprehensive healthcare platform that combines **AI-assisted symptom analysis** with a robust **telemedicine system**. It provides confidence-based disease predictions using a clinical rules engine, connects patients with specialists based on their diagnosis and location, and facilitates seamless appointment booking.

> ⚠️ **Disclaimer:** This platform is designed for educational and assistance purposes only. It does not replace professional medical advice, diagnosis, or treatment.

---

## 🌟 Key Features

### 🧠 Symptom-Based Diagnosis
- **Natural Language Input** – Describe symptoms in everyday language (supports Hinglish and patient-friendly phrases)
- **Confidence Scoring** – Results shown as LOW, MEDIUM, or HIGH confidence
- **Emergency Detection** – Automatic red-flag detection for critical symptoms
- **Disease-Aware Follow-up Questions** – Targeted clarification questions for LOW/MEDIUM confidence cases
- **Explainable Diagnosis** – "Why this diagnosis?" panel showing matched symptoms

### 🏥 Telemedicine & Appointments
- **Find Doctors Near You** – Visual map with OpenStreetMap, distance-sorted specialists
- **Appointment Booking** – Schedule consultations with recommended doctors
- **Prescription Management** – Doctors can upload prescriptions, patients can download

### 👥 Role-Based Dashboards
- **Patient** – Book appointments, view health history, download reports, rate doctors
- **Doctor** – Manage schedule, view patient history, upload prescriptions
- **Admin** – Manage doctors, view system analytics, oversee appointments

### 🎨 Modern UI/UX
- **Responsive Design** – Works on mobile, tablet, and desktop
- **Dark/Light Mode** – Toggle between themes
- **Professional Design** – Glassmorphism and modern aesthetics

---

## 🔬 How the Diagnosis Works

MediSense uses a **rules-first safety layer** combined with intelligent symptom analysis:

```
User Input → Symptom Normalization → Rules Engine → Confidence Scoring → Result
```

### 1. Symptom Normalization
- Converts patient language to medical terms (e.g., "tummy ache" → "stomach pain")
- Supports 100+ symptom aliases including Hinglish phrases
- Handles typos and common variations

### 2. Rules Engine
- **49 disease rules** with primary and supporting symptoms
- **Weighted confidence scoring:**
  - Primary symptoms = 70% weight
  - Supporting symptoms = 30% weight
- **Exclusion rules** to prevent misdiagnosis

### 3. Confidence Levels
| Level | Meaning |
|-------|---------|
| **HIGH** | Strong match with primary symptoms |
| **MEDIUM** | Partial match, may need clarification |
| **LOW** | Weak match, follow-up recommended |

### 4. Follow-up Questions
- Only shown for LOW/MEDIUM confidence cases
- Disease-specific questions that map to exact symptom keywords
- Confidence can improve by one level after follow-up (LOW→MEDIUM, MEDIUM→HIGH)

### 5. Emergency Override
- Detects critical symptoms (chest pain, difficulty breathing, etc.)
- Bypasses normal flow and recommends immediate medical attention

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | MySQL |
| **AI/Logic** | Rule-based clinical engine with confidence scoring |
| **Maps** | OpenStreetMap (Leaflet.js + Nominatim) |
| **PDF Reports** | ReportLab |
| **Deployment** | Gunicorn, Docker-ready (Render / Railway / Heroku) |

---

## 👤 User Roles

| Role | Capabilities |
|------|--------------|
| **Patient** | Check symptoms, view diagnosis, find doctors, book appointments, view history |
| **Doctor** | Manage profile, view appointments, access patient history, upload prescriptions |
| **Admin** | Manage doctors, view analytics, oversee all appointments |

---

## 📸 Screenshots

> *Add screenshots to the `static/screenshots/` folder and update paths below*

| Feature | Screenshot |
|---------|------------|
| Home Page | `![Home](static/screenshots/home.png)` |
| Diagnosis Results | `![Diagnosis](static/screenshots/diagnosis.png)` |
| Follow-up Questions | `![Follow-up](static/screenshots/followup.png)` |
| Patient Dashboard | `![Patient](static/screenshots/patient_dashboard.png)` |
| Doctor Dashboard | `![Doctor](static/screenshots/doctor_dashboard.png)` |
| Admin Dashboard | `![Admin](static/screenshots/admin_dashboard.png)` |

---

## ⚙️ Installation & Run Locally

### Prerequisites
- Python 3.8+
- MySQL Server

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/medisense.git
   cd medisense
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Create a MySQL database named `medimind`
   - Import the schema:
     ```bash
     mysql -u root -p medimind < medimind_schema.sql
     ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the Application**
   ```bash
   python main.py
   ```

7. **Access the Platform**
   Open: `http://127.0.0.1:5000`

---

## 🔑 Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@medimind.com` | `admin123` |
| Doctor | `doctor@example.com` | `doctor123` |
| Patient | `patient@example.com` | `patient123` |

---

## ⚠️ Safety Disclaimer

- This platform is for **educational and assistance purposes only**
- It is **not a replacement for professional medical advice**
- Always consult a qualified healthcare provider for medical decisions
- Emergency symptoms should be addressed by calling emergency services immediately

---

## 🚀 Future Enhancements

- [ ] Teleconsultation (video calls)
- [ ] Push notifications for appointments
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app version

---

## 📝 Notes

- **Maps:** Uses free OpenStreetMap tiles – no API key required
- **Model Files:** The `medical_bert_model/` folder must be present for ML predictions
- **Deployment:** Procfile included for Heroku/Render/Railway

---

## 👤 Author

**Utsav** – Personal/Educational Project

---

## 📄 License

This project is for educational purposes. See LICENSE file for details.

---

*Built with ❤️ for smarter healthcare assistance.*
