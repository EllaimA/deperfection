import json
import sqlite3
from task import Task

def tabel_task():
    # Define the structure of the task table
    task_template = {
        "task": {
            "analyze": {
                "content": "",
                "why": "",
                # "subgoals": "",
                "baseline": "",
                "time": ""
            },
            "prediction": {
                "worst_result": "",
                "probability": ""
            },
            "result": {
                "finished": False,
                "quality": "",  # A class / B class / C class
                "task_duration": '',
                "gentle_time_based_exposure": ""  # on / off
            },
            "review": {
                "affirmation": "",
                "areas_for_improvement": "",
            }
        }
    }
    return task_template

@staticmethod
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
            task.prediction.probability = row[6]
            task.result.finished = bool(row[7])
            task.result.quality = row[8]
            task.result.task_duration = row[9]
            task.review.affirmation = row[10]
            task.review.areas_for_improvement = row[11]
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
        prediction_probability REAL,
        result_finished INTEGER,
        result_quality TEXT,
        result_task_duration TEXT,
        review_affirmation TEXT,
        review_areas_for_improvement TEXT
    )
    """)

    conn.commit()
    conn.close()


