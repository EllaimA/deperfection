import sqlite3

def migrate_database(db_path="database.db"):
    """
    Migrate the existing database to add new columns for work_notes and actual_time
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the new columns already exist
        cursor.execute("PRAGMA table_info(task)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add plan_b column if it doesn't exist
        if 'prediction_plan_b' not in columns:
            cursor.execute("ALTER TABLE task ADD COLUMN prediction_plan_b TEXT DEFAULT ''")
            print("Added prediction_plan_b column to task table")
        
        # Add work_notes column if it doesn't exist
        if 'work_notes' not in columns:
            cursor.execute("ALTER TABLE task ADD COLUMN work_notes TEXT DEFAULT ''")
            print("Added work_notes column to task table")
        
        # Add actual_time column if it doesn't exist
        if 'actual_time' not in columns:
            cursor.execute("ALTER TABLE task ADD COLUMN actual_time TEXT DEFAULT '00:00:00'")
            print("Added actual_time column to task table")
        
        conn.commit()
        conn.close()
        print("Database migration completed successfully")
        
    except Exception as e:
        print(f"An error occurred during database migration: {e}")

if __name__ == "__main__":
    migrate_database()
