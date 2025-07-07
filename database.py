import sqlite3
from task import Task

def load_from_database(task_id, db_path="database.db"):
    """
    Load a task from the SQLite database by its ID.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch the task data
        cursor.execute("SELECT * FROM task WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            task = Task()
            task.analyze.content = row[1]
            task.analyze.why = row[2]
            task.analyze.baseline = row[3]
            task.analyze.time = row[4]
            task.prediction.worst_result = row[5]
            task.prediction.plan_b = row[6] if len(row) > 6 and row[6] else ""
            task.prediction.probability = row[7] if len(row) > 7 else 0.5
            task.result.finished = bool(row[8]) if len(row) > 8 else False
            task.result.quality = row[9] if len(row) > 9 else None
            task.result.task_duration = row[10] if len(row) > 10 else 0
            task.review.affirmation = row[11] if len(row) > 11 else ""
            task.review.areas_for_improvement = row[12] if len(row) > 12 else ""
            if len(row) > 13:
                task.work_notes = row[13] if row[13] else ""
            else:
                task.work_notes = ""
            if len(row) > 14:
                task.actual_time = row[14] if row[14] else "00:00:00"
            else:
                task.actual_time = "00:00:00"
            return task
        else:
            print(f"No task found with ID {task_id}")
            return None
    except Exception as e:
        print(f"An error occurred while loading data from the database: {e}")
        return None


def initialize_database(db_path="database.db"):
    """
    Initialize the SQLite database and create the necessary tables if they don't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the task table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analyze_content TEXT,
        analyze_why TEXT,
        analyze_baseline TEXT,
        analyze_time TEXT,
        prediction_worst_result TEXT,
        prediction_plan_b TEXT,
        prediction_probability REAL,
        result_finished INTEGER,
        result_quality TEXT,
        result_task_duration TEXT,
        review_affirmation TEXT,
        review_areas_for_improvement TEXT,
        work_notes TEXT,
        actual_time TEXT
    )
    """)

    conn.commit()
    conn.close()


