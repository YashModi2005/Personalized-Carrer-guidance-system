import mysql.connector
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the same directory as this file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# MySQL Configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'career_pilot_db')
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    try:
        # Base initialization connection
        conn_config = {
            'host': DB_CONFIG['host'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password'],
            'auth_plugin': 'mysql_native_password' # Ensure compatibility with various MySQL versions
        }
        conn = mysql.connector.connect(**conn_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.close()

        # Connect to the target database
        conn = get_connection()
        cursor = conn.cursor()
        
        # Career Recommendations Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                name VARCHAR(255) NOT NULL,
                academic_percentage FLOAT,
                interests TEXT,
                tech_skills TEXT,
                soft_skills TEXT,
                extracurriculars TEXT,
                predicted_career VARCHAR(255),
                match_score FLOAT,
                full_json LONGTEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chats history table with Full-Text Search and Soft Delete support
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                session_id VARCHAR(255),
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                is_deleted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FULLTEXT(message, response)
            ) ENGINE=InnoDB
        ''')

        # System Auditing Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_type VARCHAR(100) NOT NULL,
                event_description TEXT,
                user_id INT,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Migration: Add session_id if it doesn't exist
        try:
            cursor.execute("ALTER TABLE chats ADD COLUMN session_id VARCHAR(255) AFTER user_id")
        except:
            pass # Already exists
        
        # System Metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                metric_name VARCHAR(255) NOT NULL,
                metric_value FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                role ENUM('student', 'counselor') NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 1. SOFT DELETE MIGRATION: Add is_deleted to recommendations
        try:
            cursor.execute("ALTER TABLE recommendations ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE")
        except:
            pass

        # 2. ANALYTICAL VIEW: Student Progress Summary
        cursor.execute("DROP VIEW IF EXISTS student_progress_view")
        cursor.execute('''
            CREATE VIEW student_progress_view AS
            SELECT 
                u.id as user_id,
                u.username,
                COUNT(r.id) as assessment_count,
                MAX(r.match_score) as highest_match_score,
                AVG(r.match_score) as avg_match_score,
                MAX(r.created_at) as last_assessment_date
            FROM users u
            LEFT JOIN recommendations r ON u.id = r.user_id
            WHERE r.is_deleted = FALSE OR r.is_deleted IS NULL
            GROUP BY u.id, u.username
        ''')

        # 3. STORED PROCEDURE: Get Detailed Career Profile
        cursor.execute("DROP PROCEDURE IF EXISTS GetCareerProfile")
        cursor.execute('''
            CREATE PROCEDURE GetCareerProfile(IN p_user_id INT)
            BEGIN
                SELECT * FROM recommendations 
                WHERE user_id = p_user_id AND is_deleted = FALSE 
                ORDER BY created_at DESC;
            END
        ''')

        # 4. TRIGGER: Auto-Welcome Chat on Registration
        # Note: Delimiters are handled by mysql-connector internally if sent as one block or properly handled
        cursor.execute("DROP TRIGGER IF EXISTS after_user_registration")
        cursor.execute('''
            CREATE TRIGGER after_user_registration
            AFTER INSERT ON users
            FOR EACH ROW
            BEGIN
                INSERT INTO chats (user_id, session_id, message, response)
                VALUES (NEW.id, 'SYSTEM_INIT', 'User Registered', 'Welcome to CareerPilot! I am your AI coach. How can I help you today?');
            END
        ''')
        
        conn.commit()
        conn.close()
        print(f"MySQL Database '{DB_CONFIG['database']}' initialized.")
    except Exception as e:
        print(f"Error initializing MySQL database: {e}")

def save_recommendation(data, prediction, score, user_id=None, full_json=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recommendations 
        (user_id, name, academic_percentage, interests, tech_skills, soft_skills, extracurriculars, predicted_career, match_score, full_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        user_id,
        data.name,
        data.academic_percentage,
        data.interests,
        ",".join(data.tech_skills) if isinstance(data.tech_skills, list) else data.tech_skills,
        ",".join(data.soft_skills) if isinstance(data.soft_skills, list) else data.soft_skills,
        data.extracurriculars,
        prediction,
        score,
        full_json
    ))
    conn.commit()
    conn.close()

def get_user_recommendations(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM recommendations WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_chat(user_id, message, response, session_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    # Log the event (Auditing)
    cursor.execute('''
        INSERT INTO system_logs (event_type, event_description, user_id)
        VALUES (%s, %s, %s)
    ''', ('CHAT_MESSAGE', f'User sent: {message[:50]}...', user_id))
    
    cursor.execute('''
        INSERT INTO chats (user_id, session_id, message, response)
        VALUES (%s, %s, %s, %s)
    ''', (user_id, session_id, message, response))
    conn.commit()
    conn.close()

def search_chats(user_id, query):
    """5. FULL-TEXT SEARCH Implementation"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT *, MATCH(message, response) AGAINST(%s IN NATURAL LANGUAGE MODE) as score
        FROM chats 
        WHERE user_id = %s AND is_deleted = FALSE
        AND MATCH(message, response) AGAINST(%s IN NATURAL LANGUAGE MODE)
        ORDER BY score DESC
    ''', (query, user_id, query))
    rows = cursor.fetchall()
    conn.close()
    return rows

def soft_delete_chat(chat_id):
    """6. SOFT DELETE Implementation"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE chats SET is_deleted = TRUE WHERE id = %s', (chat_id,))
    conn.commit()
    conn.close()

def get_user_chats(user_id, limit=5, session_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if session_id:
        cursor.execute('SELECT * FROM chats WHERE user_id = %s AND session_id = %s AND is_deleted = FALSE ORDER BY created_at DESC LIMIT %s', (user_id, session_id, limit))
    else:
        cursor.execute('SELECT * FROM chats WHERE user_id = %s AND is_deleted = FALSE ORDER BY created_at DESC LIMIT %s', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    # Return in chronological order for the agent to build context
    return rows[::-1]

def get_latest_recommendation(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM recommendations WHERE user_id = %s ORDER BY created_at DESC LIMIT 1', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_recommendations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Get all recommendations with a count of total assessments for that voyager
    # We use a subquery to pre-calculate counts to ensure performance
    query = '''
        SELECT r.*, counts.total as assessment_count
        FROM recommendations r
        LEFT JOIN (
            SELECT 
                name, user_id, 
                COUNT(*) as total
            FROM recommendations
            GROUP BY name, user_id
        ) counts ON r.name = counts.name AND (r.user_id = counts.user_id OR (r.user_id IS NULL AND counts.user_id IS NULL))
        ORDER BY r.created_at DESC
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Debug print to verify data structure
    if rows:
        print(f"DEBUG: First row keys: {list(rows[0].keys())}")
        print(f"DEBUG: First row assessment_count: {rows[0].get('assessment_count')}")
    
    conn.close()
    return rows

def get_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Use the Analytical View for more advanced stats
    cursor.execute('SELECT COUNT(*) as total_users, AVG(avg_match_score) as overall_avg FROM student_progress_view')
    view_stats = cursor.fetchone()
    
    cursor.execute('SELECT COUNT(*) as total_sessions FROM recommendations WHERE is_deleted = FALSE')
    total_sessions = cursor.fetchone()['total_sessions']
    
    cursor.execute('SELECT predicted_career, COUNT(*) as count FROM recommendations WHERE is_deleted = FALSE GROUP BY predicted_career ORDER BY count DESC')
    top_careers = [{"career": row['predicted_career'], "count": row['count']} for row in cursor.fetchall()]
    
    conn.close()
    return {
        "total_sessions": total_sessions,
        "total_users": view_stats['total_users'],
        "average_match_score": round(float(view_stats['overall_avg'] or 0) * 100, 2),
        "top_career_trends": top_careers,
        "model_version": "1.1.0-Neural-v2-SQL-Pro"
    }

def create_user(username, hashed_password, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, hashed_password, role)
            VALUES (%s, %s, %s)
        ''', (username, hashed_password, role))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating user: {err}")
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    row = cursor.fetchone()
    conn.close()
    return row
