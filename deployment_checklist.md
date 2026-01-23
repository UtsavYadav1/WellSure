# Render + Supabase Deployment Checklist

## 1. Supabase Database Setup
- [ ] **Create Account**: Go to [supabase.com](https://supabase.com) → Sign up.
- [ ] **Create Project**: New Project → Choose region → Set DB password.
- [ ] **Create Schema**: Go to SQL Editor → Paste contents of `schema_postgres.sql` → Run.
- [ ] **Import Data**:
  - Run locally: `python convert_to_postgres.py`
  - Paste `backup_postgres.sql` contents into Supabase SQL Editor → Run.
- [ ] **Get Connection String**: Settings → Database → Connection String (URI) → Copy.

## 2. Render Deployment
- [ ] **Create Account**: Go to [render.com](https://render.com) → Sign up with GitHub.
- [ ] **New Web Service**: Connect your GitHub repo → Select `WellSure`.
- [ ] **Build Settings**:
  - Build Command: `pip install -r requirements_render.txt`
  - Start Command: `gunicorn main:app`
- [ ] **Environment Variables**:
  ```env
  DATABASE_URL=postgresql://...  (from Supabase)
  SECRET_KEY=your_secret_key
  GOOGLE_CLIENT_ID=your_id
  GOOGLE_CLIENT_SECRET=your_secret
  ```
- [ ] **Deploy**: Click "Create Web Service".

## 3. Verification
- [ ] Test Login (Patient/Doctor/Admin)
- [ ] Run Symptom Check → Download PDF
- [ ] Book Appointment
- [ ] View Maps on Doctor Page
