import streamlit as st
import random
from task import Task
import datetime

# Use the Task object from session state
if "task" not in st.session_state:
    st.session_state.task = Task()

task = st.session_state.task

def analyze_page():
    st.title("Analyze")
    task = st.session_state.task # 获取 session 中的 task

    task.analyze.content = st.text_area("Task是什么?", task.analyze.content, key="analyze_content_input")
    task.analyze.why = st.text_area("为什么要做这个task?", task.analyze.why, key="analyze_why_input")
    task.analyze.baseline = st.text_area("这个task至少要做到哪一步?", task.analyze.baseline, key="analyze_baseline_input")

    # --- 时间输入处理 ---
    initial_datetime_obj_for_widget = None
    if task.analyze.time:  # task.analyze.time 是 "HH:MM" 字符串或空串
        try:
            parts = task.analyze.time.split(':')
            if len(parts) == 2:
                hour, minute = int(parts[0]), int(parts[1])
                initial_datetime_obj_for_widget = datetime.time(hour, minute)
        except (ValueError, TypeError): # 解析失败
            initial_datetime_obj_for_widget = None

    selected_time_obj = st.time_input("时间", value=initial_datetime_obj_for_widget, key="analyze_time_input")
    task.analyze.time = selected_time_obj.strftime("%H:%M") if selected_time_obj else ""
    # --- 时间输入处理结束 ---

    if st.button("Update Analyze", key="update_analyze_button"):
        st.success("Analysis data updated successfully!")
        st.session_state.current_page = "Prediction"
        st.rerun()
        

def prediction_page():
    st.title("Prediction")
    task = st.session_state.task # 获取 session 中的 task

    task.prediction.worst_result = st.text_input("Worst Result", task.prediction.worst_result, key="worst_result_input")

    # 确保 probability 是浮点数
    try:
        current_probability_val = float(task.prediction.probability)
    except (ValueError, TypeError): # 如果是空字符串或者None等无法转换的情况
        current_probability_val = 0.5 # 给一个默认值

    task.prediction.probability = st.slider("Probability", min_value=0.0, max_value=1.0, value=current_probability_val, step=0.05)

    if st.button("Update Prediction", key="update_prediction_button"):
        st.success("Prediction data updated successfully!")
        st.session_state.current_page = "Result"
        st.rerun()



def result_page():
    task = st.session_state.task # 获取 session 中的 task
    st.title("Result")
    # Use a key for the selectbox to directly manage its state in st.session_state
    # Initialize if not present
    if "result_finished_selection" not in st.session_state:
        st.session_state.result_finished_selection = 0 if task.result.finished else 1

    finished_selection = st.selectbox("Finished", ["Yes", "No"], index=st.session_state.result_finished_selection, key="result_finished_selection_widget")
    task.result.finished = finished_selection == "Yes"


    display_options = ["A class: 超出期望，有额外优化", "B class: 满足要求，没大问题", "C class: 能交差，不至于失败"]
    value_options = ["A class", "B class", "C class"]

    # Helper to get current index for the selectbox
    try:
        # If task.result.quality is None or not in value_options on a new task, handle it.
        current_quality_index = value_options.index(task.result.quality) if task.result.quality in value_options else 0
    except ValueError:
        current_quality_index = 0 # Default if somehow task.result.quality is invalid

    # The selectbox value will be one of display_options
    selected_display_option = st.selectbox(
        "Quality",
        display_options,
        index=current_quality_index,
        key="quality_selectbox" # Give it a unique key
    )

    # Update task.result.quality based on the selection from the widget
    # This will reflect the user's current choice in the selectbox
    task.result.quality = value_options[display_options.index(selected_display_option)]

    if st.button("Update Result", key="update_result_button"):
        # The task.result.quality is already updated by the selectbox's interaction above
        # and task.result.finished is also updated.
        st.success("Result data updated successfully!")
        st.session_state.current_page = "Review"
        st.rerun()


def review_page():
    # Ensure task is always bound to st.session_state.task
    task = st.session_state.task

    st.title("Review")
    task.review.affirmation = st.text_area("今天我朝目标迈进了吗？迈进了什么？", task.review.affirmation, key="review_affirmation_input")
    task.review.areas_for_improvement = st.text_area("做得不够好的地方（最多写一个）", task.review.areas_for_improvement, key="review_areas_for_improvement_input")
    st.write(f'*它真的必须完美吗？*')

    # Randomly select a cue from the Review.cue list
    random_cue = random.choice(task.review.cue)
    st.write(f'*"{random_cue}"*')
    
    if st.button("Save Task", key="save_task_button"):
        task.save_to_database()
        st.success("Task data saved successfully!")

    if st.button("New Task", key="new_task_button"):
        # Create a new Task object and assign it to session state
        st.session_state.task = Task()
        task = st.session_state.task  # Update the local reference to the new task

        # Clear Streamlit session state for all inputs
        for key in list(st.session_state.keys()):
            if key not in ["task", "current_page"]:  # 保留必要的键
                del st.session_state[key]

        st.session_state.current_page = "Analyze"
        st.rerun()