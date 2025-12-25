-- Database Schema for MediMind AI
-- Run this script to initialize the database tables

CREATE DATABASE IF NOT EXISTS medimind;
USE medimind;

-- 1. Users (Patients) Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Hashed
    phone VARCHAR(20),
    age INT,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    experience_years INT,
    fees DECIMAL(10, 2),
    description TEXT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    available_start_time TIME,
    available_end_time TIME,
    profile_pic VARCHAR(255), -- Path to image
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    disease_predicted VARCHAR(100),
    doctor_specialization VARCHAR(100),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending', -- Pending, Confirmed, Completed, Cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- 4. Feedback Table
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- 5. Symptoms Logs Table
CREATE TABLE IF NOT EXISTS symptoms_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    symptoms_text TEXT,
    disease_predicted VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

-- Insert Dummy Admin (handled in code or here if needed, but Prompt says hard-coded or DB)
-- We will stick to Roles within logic or a separate admins table if preferred, 
-- but strictly following prompt: "Admin (hard-coded or DB)". We'll use DB is better.
-- Let's add an 'role' column to users or a separate table? 
-- The prompt splits Dashboards clearly. Let's create an 'admins' table for clarity or just hardcode as requested "Admin (hard-coded or DB)".
-- I'll create a simple admins table for robustness.
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT IGNORE INTO admins (email, password) VALUES ('admin@medimind.ai', 'scrypt:32768:8:1$hardcodedhash$placeholder'); 
-- Note: Password handling will be done via Werkzeug security in Python.
