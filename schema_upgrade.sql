
-- Upgrade Schema for MediMind Telemedicine Platform

USE medimind;

-- 1. Upgrade Users (Patients)
-- Add location and medical history
ALTER TABLE users 
ADD COLUMN city VARCHAR(100),
ADD COLUMN address TEXT,
ADD COLUMN pincode VARCHAR(20),
ADD COLUMN medical_history TEXT,
ADD COLUMN lat DECIMAL(10, 8),
ADD COLUMN lng DECIMAL(11, 8);

-- 2. Upgrade Doctors
-- Add location and ratings
ALTER TABLE doctors 
ADD COLUMN city VARCHAR(100),
ADD COLUMN address TEXT,
ADD COLUMN pincode VARCHAR(20),
ADD COLUMN lat DECIMAL(10, 8),
ADD COLUMN lng DECIMAL(11, 8),
ADD COLUMN rating_average DECIMAL(3, 2) DEFAULT 0.00,
ADD COLUMN rating_count INT DEFAULT 0;

-- 3. Upgrade Appointments
-- Add link to prediction log, prescription, notes
ALTER TABLE appointments 
ADD COLUMN symptom_log_id INT,
ADD COLUMN prescription_path VARCHAR(255),
ADD COLUMN visit_notes TEXT;

-- 4. Upgrade Symptoms Logs
-- Add more details from prediction and PDF path
ALTER TABLE symptoms_logs 
ADD COLUMN pdf_path VARCHAR(255),
ADD COLUMN description TEXT,
ADD COLUMN medications TEXT,
ADD COLUMN precautions TEXT,
ADD COLUMN diets TEXT,
ADD COLUMN workouts TEXT;

-- 5. New Table: Doctor Feedback
CREATE TABLE IF NOT EXISTS doctor_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

-- 6. New Table: Activity Logs
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, -- Can be NULL for system events or if user deleted
    role VARCHAR(50), -- 'patient', 'doctor', 'admin'
    action VARCHAR(255),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
