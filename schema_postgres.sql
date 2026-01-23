-- Database Schema for WellSure (PostgreSQL/Supabase)
-- Run this script in Supabase SQL Editor to initialize tables

-- 1. Users (Patients) Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    age INT,
    gender VARCHAR(10),
    city VARCHAR(100),
    address TEXT,
    pincode VARCHAR(10),
    medical_history TEXT,
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
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
    profile_pic VARCHAR(255),
    city VARCHAR(100),
    address TEXT,
    pincode VARCHAR(10),
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    rating_average DECIMAL(3,2) DEFAULT 0,
    rating_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) DEFAULT 'Admin',
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Specializations Table
CREATE TABLE IF NOT EXISTS specializations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 5. Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES users(id),
    doctor_id INT NOT NULL REFERENCES doctors(id),
    symptom_log_id INT,
    disease_predicted VARCHAR(100),
    doctor_specialization VARCHAR(100),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    payment_mode VARCHAR(20) DEFAULT 'at_clinic',
    meeting_link TEXT,
    visit_notes TEXT,
    prescription_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Symptoms Logs Table
CREATE TABLE IF NOT EXISTS symptoms_logs (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES users(id),
    symptoms_text TEXT,
    disease_predicted VARCHAR(100),
    description TEXT,
    medications TEXT,
    precautions TEXT,
    diets TEXT,
    workouts TEXT,
    pdf_path VARCHAR(255),
    confidence_level VARCHAR(20),
    recommended_specialist VARCHAR(100),
    patient_age INT,
    patient_gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Doctor Feedback Table
CREATE TABLE IF NOT EXISTS doctor_feedback (
    id SERIAL PRIMARY KEY,
    appointment_id INT REFERENCES appointments(id),
    doctor_id INT NOT NULL REFERENCES doctors(id),
    patient_id INT NOT NULL REFERENCES users(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Activity Logs Table
CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    user_type VARCHAR(20),
    action VARCHAR(50),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Default Specializations
INSERT INTO specializations (name) VALUES 
    ('Cardiologist'),
    ('Dermatologist'),
    ('Gastroenterologist'),
    ('General Physician'),
    ('Neurologist'),
    ('Ophthalmologist'),
    ('Orthopedic'),
    ('Pediatrician'),
    ('Psychiatrist'),
    ('Pulmonologist'),
    ('ENT Specialist'),
    ('Endocrinologist'),
    ('Rheumatologist'),
    ('Allergist'),
    ('Infectious Disease Specialist')
ON CONFLICT (name) DO NOTHING;
