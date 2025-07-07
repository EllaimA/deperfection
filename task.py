import sqlite3

class Analyze:
    def __init__(self):
        self.content = ""
        self.why = ""
        self.baseline = ""
        self.time = ""

class Prediction:
    def __init__(self):
        self.worst_result = ""
        self.plan_b = ""
        self.probability = 0.5  

class Result:
    def __init__(self):
        self.finished = False
        self.quality = None
        self.task_duration = 0

class Review:
    def __init__(self):
        self.affirmation = ""
        self.areas_for_improvement = ""
        self.cue = [
            "我不是来表现得完美的，我是来完成任务的。",
            "80%的完成，比0%的完美要有价值得多。",
            "拖延不会让事情更好，只会让我更累。"
        ]

class Task:
    def __init__(self):
        self.analyze = Analyze()
        self.prediction = Prediction()
        self.result = Result()
        self.review = Review()
        self.work_notes = ""
        self.actual_time = "00:00:00"

    def to_dict(self):
        """
        Convert the Task object to a dictionary.
        :return: A dictionary representation of the Task object.
        """
        return {
            "task": {
                "analyze": {
                    "content": self.analyze.content,
                    "why": self.analyze.why,
                    "baseline": self.analyze.baseline,
                    "time": self.analyze.time
                },
                "prediction": {
                    "worst_result": self.prediction.worst_result,
                    "plan_b": self.prediction.plan_b,
                    "probability": self.prediction.probability
                },
                "result": {
                    "finished": self.result.finished,
                    "quality": self.result.quality,
                    "task_duration": self.result.task_duration
                },
                "review": {
                    "affirmation": self.review.affirmation,
                    "areas_for_improvement": self.review.areas_for_improvement
                }
            }
        }
    

    def save_to_database(self, db_path="database.db"):
        """
        Save the task data to the SQLite database.
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Insert task data into the database
            cursor.execute("""
            INSERT INTO task (
                analyze_content, analyze_why, analyze_baseline, analyze_time,
                prediction_worst_result, prediction_plan_b, prediction_probability,
                result_finished, result_quality, result_task_duration,
                review_affirmation, review_areas_for_improvement,
                work_notes, actual_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.analyze.content,
                self.analyze.why,
                self.analyze.baseline,
                self.analyze.time,
                self.prediction.worst_result,
                self.prediction.plan_b,
                self.prediction.probability,
                int(self.result.finished),
                self.result.quality,
                self.result.task_duration,
                self.review.affirmation,
                self.review.areas_for_improvement,
                getattr(self, 'work_notes', ''),
                getattr(self, 'actual_time', '00:00:00')
            ))

            conn.commit()
            conn.close()
            print("Task data successfully saved to the database.")
        except Exception as e:
            print(f"An error occurred while saving data to the database: {e}")


