-- AI Career Pilot - Data Viewer Script
-- Open this file in MySQL Workbench and press the 'Execute' (Lightning Bolt) icon

USE career_pilot_db;

-- 1. View all Registered Users
SELECT * FROM users;

-- 2. View all Career Assessments & Recommendations
SELECT * FROM registrations;

-- 3. View all AI Coach Chat History
SELECT * FROM chats;

-- 4. View System Metrics (Global Stats)
SELECT * FROM metrics;
