import sqlite3

class Analyze:
    def __init__(self):
        self.content = ""
        self.why = ""
        # self.subgoals = ""
        self.baseline = ""
        self.time = ""
class Prediction:
    def __init__(self):
        self.worst_result = ""
        self.probability = 0.5  
class Result:
    def __init__(self):
        self.finished = False
        # quality should be one of these: "A class", "B class", "C class"
        self.quality = None  # Default is None, to be set later
        self.task_duration = 0
        # self.gentle_time_based_exposure = False

# class GentleTimeBasedExposure:
#     def __init__(self):
#         self.affirmations = [""]

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
                    # "subgoals": self.analyze.subgoals,
                    "baseline": self.analyze.baseline,
                    "time": self.analyze.time
                },
                "prediction": {
                    "worst_result": self.prediction.worst_result,
                    "probability": self.prediction.probability
                },
                "result": {
                    "finished": self.result.finished,
                    "quality": self.result.quality,
                    "task_duration": self.result.task_duration,
                    # "gentle_time_based_exposure": self.result.gentle_time_based_exposure
                },
                "review": {
                    "affirmation": self.review.affirmation,
                    "areas_for_improvement": self.review.areas_for_improvement,
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
                prediction_worst_result, prediction_probability,
                result_finished, result_quality, result_task_duration,
                review_affirmation, review_areas_for_improvement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.analyze.content,
                self.analyze.why,
                self.analyze.baseline,
                self.analyze.time,
                self.prediction.worst_result,
                self.prediction.probability,
                int(self.result.finished),  # Convert boolean to integer
                self.result.quality,
                self.result.task_duration,
                self.review.affirmation,
                self.review.areas_for_improvement
            ))

            conn.commit()
            conn.close()
            print("Task data successfully saved to the database.")
        except Exception as e:
            print(f"An error occurred while saving data to the database: {e}")


