import streamlit as st
from pages import analyze_page, prediction_page, result_page, review_page
from task import Task
from database import initialize_database

def sync_widget_states_to_task():
    """在页面切换前同步所有widget状态到task对象"""
    task = st.session_state.task
    
    # 同步analyze页面的输入
    if "analyze_content_input" in st.session_state:
        task.analyze.content = st.session_state.analyze_content_input
    if "analyze_why_input" in st.session_state:
        task.analyze.why = st.session_state.analyze_why_input
    if "analyze_baseline_input" in st.session_state:
        task.analyze.baseline = st.session_state.analyze_baseline_input
    if "analyze_time_widget" in st.session_state:
        task.analyze.time = st.session_state.analyze_time_widget.strftime("%H:%M")
    
    # 同步prediction页面的输入
    if "worst_result_input" in st.session_state:
        task.prediction.worst_result = st.session_state.worst_result_input
    if "prediction_probability_widget" in st.session_state:
        task.prediction.probability = st.session_state.prediction_probability_widget
    
    # 同步result页面的输入
    if "result_finished_selection_widget" in st.session_state:
        task.result.finished = st.session_state.result_finished_selection_widget == "Yes"
    if "quality_selectbox" in st.session_state:
        display_options = ["A class: 超出期望，有额外优化", "B class: 满足要求，没大问题", "C class: 能交差，不至于失败"]
        value_options = ["A class", "B class", "C class"]
        if st.session_state.quality_selectbox in display_options:
            task.result.quality = value_options[display_options.index(st.session_state.quality_selectbox)]
    
    # 同步review页面的输入
    if "review_affirmation_input" in st.session_state:
        task.review.affirmation = st.session_state.review_affirmation_input
    if "review_areas_for_improvement_input" in st.session_state:
        task.review.areas_for_improvement = st.session_state.review_areas_for_improvement_input

# Initialize a global Task object in session state
if "task" not in st.session_state:
    st.session_state.task = Task()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Analyze"

def main():
    st.set_page_config(page_title="目标导向 + 去完美主义")
    
    # 在每次运行时都同步状态
    sync_widget_states_to_task()
    
    # 使用不同的按钮样式显示当前页面
    st.sidebar.markdown("**Navigation**")
    
    # 创建导航按钮，当前页面使用不同的显示方式
    pages = [
        ("📊 Analyze", "Analyze"),
        ("🔮 Prediction", "Prediction"), 
        ("✅ Result", "Result"),
        ("📝 Review", "Review")
    ]
    
    for icon_text, page_name in pages:
        is_current = st.session_state.current_page == page_name
        
        if is_current:
            # 当前页面使用主要按钮样式并添加标记
            button_text = f"{icon_text}"
            button_type = "primary"
        else:
            # 其他页面使用次要按钮样式
            button_text = icon_text
            button_type = "secondary"
        
        if st.sidebar.button(button_text, key=f"nav_{page_name.lower()}", 
                           use_container_width=True, type=button_type):
            if not is_current:  # 只有当不是当前页面时才切换
                st.session_state.current_page = page_name
                st.rerun()
    
    
    # Render the selected page
    if st.session_state.current_page == "Analyze":
        analyze_page()

    elif st.session_state.current_page == "Prediction":
        prediction_page()

    elif st.session_state.current_page == "Result":
        result_page()

    elif st.session_state.current_page == "Review":
        review_page()



if __name__ == "__main__":
    # Call this function before the main function
    initialize_database()
    main()
