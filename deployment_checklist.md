# PythonAnywhere Deployment Checklist

Follow these steps exactly to deploy WellSure on PythonAnywhere Free Tier.

## 1. Code Setup
- [ ] **Open Bash Console** on PythonAnywhere.
- [ ] **Clone Repository**:
  ```bash
  git clone https://github.com/YOUR_GITHUB_USERNAME/WellSure.git
  cd WellSure
  ```
- [ ] **Install Dependencies**:
  ```bash
  pip3 install -r requirements_pa.txt --user
  ```

## 2. Database Setup (Internal MySQL)
- [ ] **Create Database**: Go to **Databases** tab -> Create database (e.g., `wellsure`).
- [ ] **Set Password**: Set a database password at the top of the page.
- [ ] **Import Data**:
  - Upload your local `backup.sql` to PythonAnywhere (via "Files" tab).
  - Run in Bash Console:
    ```bash
    mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com -p 'yourusername$wellsure' < backup.sql
    ```
- [ ] **Configure .env**: Create a `.env` file in `WellSure/` directory:
  ```env
  SECRET_KEY=secure_key_here
  GOOGLE_CLIENT_ID=your_id
  GOOGLE_CLIENT_SECRET=your_secret
  # Database Config
  MYSQLHOST=yourusername.mysql.pythonanywhere-services.com
  MYSQLUSER=yourusername
  MYSQLPASSWORD=your_db_password
  MYSQLDATABASE=yourusername$wellsure
  ```

## 3. Web App Configuration
- [ ] **Add New Web App**: Go to **Web** tab -> **Add a new web app**.
- [ ] **Select Framework**: Manual Configuration -> Python 3.9 (or 3.10).
- [ ] **Code Section**:
  - **Source code**: `/home/yourusername/WellSure`
  - **Working directory**: `/home/yourusername/WellSure`
- [ ] **WSGI Configuration File**:
  - Click the link to edit the WSGI file.
  - Delete everything and paste the content from `pythonanywhere_wsgi_example.py`.
  - **CRITICAL**: Update `path = '/home/yourusername/WellSure'` inside the file.
- [ ] **Static Files**:
  - **URL**: `/static/`
  - **Directory**: `/home/yourusername/WellSure/static`

## 4. Final Verification
- [ ] **Reload Web App**: Click the green "Reload" button throughout the process if things change.
- [ ] **Test Login**: Ensure you can log in with existing users.
- [ ] **Test Prediction**: Run a symptom check to verify CSV loading and Rules Engine.
- [ ] **Test PDF**: Download a diagnosis report (Verifies absolute paths fixes).
- [ ] **Test Maps**: View Doctor's page to ensure map renders (OpenStreetMap).
