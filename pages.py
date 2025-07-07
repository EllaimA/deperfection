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

    # 初始化widget状态
    if "analyze_content_input" not in st.session_state:
        st.session_state.analyze_content_input = task.analyze.content
    if "analyze_why_input" not in st.session_state:
        st.session_state.analyze_why_input = task.analyze.why
    if "analyze_baseline_input" not in st.session_state:
        st.session_state.analyze_baseline_input = task.analyze.baseline

    task.analyze.content = st.text_area("Task是什么?", value=st.session_state.analyze_content_input, key="analyze_content_input")
    task.analyze.why = st.text_area("为什么要做这个task?", value=st.session_state.analyze_why_input, key="analyze_why_input")
    task.analyze.baseline = st.text_area("这个task至少要做到哪一步?", value=st.session_state.analyze_baseline_input, key="analyze_baseline_input")

    # --- 时间输入处理 ---
    # 初始化session state中的时间值
    if "analyze_time_widget" not in st.session_state:
        if task.analyze.time:  # task.analyze.time 是 "HH:MM" 字符串或空串
            try:
                parts = task.analyze.time.split(':')
                if len(parts) == 2:
                    hour, minute = int(parts[0]), int(parts[1])
                    st.session_state.analyze_time_widget = datetime.time(hour, minute)
                else:
                    st.session_state.analyze_time_widget = datetime.time(0, 0)
            except (ValueError, TypeError): # 解析失败
                st.session_state.analyze_time_widget = datetime.time(0, 0)
        else:
            st.session_state.analyze_time_widget = datetime.time(0, 0)

    selected_time_obj = st.time_input("时间", value=st.session_state.analyze_time_widget, key="analyze_time_widget", step=60)
    # 更新task中的时间值
    task.analyze.time = selected_time_obj.strftime("%H:%M") if selected_time_obj else ""
    # --- 时间输入处理结束 ---

    # 实时同步所有字段到task对象
    task.analyze.content = st.session_state.analyze_content_input
    task.analyze.why = st.session_state.analyze_why_input
    task.analyze.baseline = st.session_state.analyze_baseline_input

    if st.button("Update Analyze", key="update_analyze_button"):
        st.success("Analysis data updated successfully!")
        st.session_state.current_page = "Prediction"
        st.rerun()
        

def prediction_page():
    st.title("Prediction")
    task = st.session_state.task # 获取 session 中的 task

    # 初始化widget状态
    if "worst_result_input" not in st.session_state:
        st.session_state.worst_result_input = task.prediction.worst_result

    task.prediction.worst_result = st.text_input("Worst Result", value=st.session_state.worst_result_input, key="worst_result_input")

    # 初始化session state中的probability值
    if "prediction_probability_widget" not in st.session_state:
        try:
            st.session_state.prediction_probability_widget = float(task.prediction.probability)
        except (ValueError, TypeError): # 如果是空字符串或者None等无法转换的情况
            st.session_state.prediction_probability_widget = 0.5 # 给一个默认值

    probability_value = st.slider("Probability", min_value=0.0, max_value=1.0, value=st.session_state.prediction_probability_widget, step=0.05, key="prediction_probability_widget")
    # 更新task中的probability值
    task.prediction.probability = probability_value

    # 实时同步所有字段到task对象
    task.prediction.worst_result = st.session_state.worst_result_input

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

    # 实时同步所有字段到task对象
    task.result.finished = st.session_state.result_finished_selection_widget == "Yes"

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
    
    # 初始化widget状态
    if "review_affirmation_input" not in st.session_state:
        st.session_state.review_affirmation_input = task.review.affirmation
    if "review_areas_for_improvement_input" not in st.session_state:
        st.session_state.review_areas_for_improvement_input = task.review.areas_for_improvement
    
    task.review.affirmation = st.text_area("今天我朝目标迈进了吗？迈进了什么？", value=st.session_state.review_affirmation_input, key="review_affirmation_input")
    task.review.areas_for_improvement = st.text_area("做得不够好的地方（最多写一个）", value=st.session_state.review_areas_for_improvement_input, key="review_areas_for_improvement_input")
    
    # 实时同步所有字段到task对象
    task.review.affirmation = st.session_state.review_affirmation_input
    task.review.areas_for_improvement = st.session_state.review_areas_for_improvement_input
    
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
            if key not in ["task", "current_page", "page_selector"]:  # 保留必要的键
                del st.session_state[key]

        # 重新初始化所有widget状态为新task的默认值
        st.session_state.analyze_content_input = task.analyze.content
        st.session_state.analyze_why_input = task.analyze.why
        st.session_state.analyze_baseline_input = task.analyze.baseline
        st.session_state.analyze_time_widget = datetime.time(0, 0)
        st.session_state.worst_result_input = task.prediction.worst_result
        st.session_state.prediction_probability_widget = 0.5
        st.session_state.result_finished_selection = 1  # Default to "No"
        st.session_state.review_affirmation_input = task.review.affirmation
        st.session_state.review_areas_for_improvement_input = task.review.areas_for_improvement
        
        st.session_state.current_page = "Analyze"
        st.rerun()