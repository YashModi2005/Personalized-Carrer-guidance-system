from database import init_db

if __name__ == "__main__":
    print("Applying Advanced SQL Upgrades...")
    init_db()
    print("Success: All SQL Triggers, Views, and Procedures are live!")
