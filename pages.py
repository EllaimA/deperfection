import streamlit as st
import random
from task import Task
import datetime
from streamlit_autorefresh import st_autorefresh

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

    # 显示分析页面的信息
    st.subheader("📋 分析回顾")
    
    # 创建一个展开的区域显示分析信息
    with st.expander("查看分析详情", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Task内容:**")
            if task.analyze.content:
                st.info(task.analyze.content)
            else:
                st.write("*未填写*")
            
            st.write("**基线要求:**")
            if task.analyze.baseline:
                st.info(task.analyze.baseline)
            else:
                st.write("*未填写*")
        
        with col2:
            st.write("**目标原因:**")
            if task.analyze.why:
                st.info(task.analyze.why)
            else:
                st.write("*未填写*")
            
            st.write("**计划时间:**")
            if task.analyze.time:
                st.info(f"⏰ {task.analyze.time}")
            else:
                st.write("*未设置*")
    
    st.divider()
    
    # 预测部分
    st.subheader("🔮 预测分析")
    
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

    if st.button("Begin Task", key="begin_task_button"):
        st.success("Task started! Good luck! 🚀")
        st.session_state.current_page = "Work"
        st.rerun()



def work_page():
    st.title("🚀 Work in Progress")
    task = st.session_state.task # 获取 session 中的 task
    
    # 自动刷新（每 1 秒）- 只在计时器运行时启用
    if st.session_state.get("timer_running", False):
        st_autorefresh(interval=1000, key="timer_refresh")
    
    # 显示任务概要
    st.subheader("📝 当前任务")
    if task.analyze.content:
        st.info(f"**任务内容**: {task.analyze.content}")
    else:
        st.warning("任务内容未填写")
    
    
    # 解析目标时间
    if task.analyze.time:
        try:
            parts = task.analyze.time.split(':')
            if len(parts) == 2:
                target_hours = int(parts[0])
                target_minutes = int(parts[1])
                total_target_seconds = target_hours * 3600 + target_minutes * 60
                
                # 初始化计时器状态
                if "timer_start_time" not in st.session_state:
                    st.session_state.timer_start_time = None
                if "timer_running" not in st.session_state:
                    st.session_state.timer_running = False
                
                # 启动计时按钮 - 只能按一次
                if not st.session_state.timer_running and st.session_state.timer_start_time is None:
                    if st.button("▶️ 开始计时", key="start_timer"):
                        import time
                        st.session_state.timer_start_time = time.time()
                        st.session_state.timer_running = True
                        st.rerun()

                
                # 显示倒计时
                if st.session_state.timer_running and st.session_state.timer_start_time:
                    import time
                    elapsed_seconds = int(time.time() - st.session_state.timer_start_time)
                    remaining_seconds = max(0, total_target_seconds - elapsed_seconds)
                    
                    if remaining_seconds > 0:
                        hours = remaining_seconds // 3600
                        minutes = (remaining_seconds % 3600) // 60
                        seconds = remaining_seconds % 60
                        
                        # 大号显示剩余时间
                        st.markdown(f"### {hours:02d}:{minutes:02d}:{seconds:02d}")
                        
                        # 进度条
                        progress = (total_target_seconds - remaining_seconds) / total_target_seconds
                        st.progress(progress)
                        
                        # 显示状态信息
                        st.success(f"工作中...")
                    else:
                        st.success("🎉 时间到！任务完成！")
                        st.balloons()
                        st.session_state.timer_running = False
                elif st.session_state.timer_start_time:
                    import time
                    elapsed_seconds = int(time.time() - st.session_state.timer_start_time)
                    remaining_seconds = max(0, total_target_seconds - elapsed_seconds)
                    hours = remaining_seconds // 3600
                    minutes = (remaining_seconds % 3600) // 60
                    seconds = remaining_seconds % 60
                    st.markdown(f"### ⏸️ 暂停中: {hours:02d}:{minutes:02d}:{seconds:02d}")
                else:
                    hours = target_hours
                    minutes = target_minutes
                    st.markdown(f"### {hours:02d}:{minutes:02d}:00")
                    
        except (ValueError, TypeError):
            st.error("时间格式错误")
    else:
        st.warning("未设置目标时间")
    
    st.divider()
    
    # 工作笔记
    st.subheader("📝 工作笔记")
    
    # 初始化笔记状态
    if "work_notes_input" not in st.session_state:
        if hasattr(task, 'work_notes'):
            st.session_state.work_notes_input = task.work_notes
        else:
            st.session_state.work_notes_input = ""
    
    work_notes = st.text_area(
        "记录工作过程、想法、遇到的问题等...",
        value=st.session_state.work_notes_input,
        key="work_notes_input",
        height=200,
        placeholder="在这里记录你的工作进展、遇到的问题、灵感想法等...",
        help="💡 提示：计时过程中可以正常输入笔记，倒计时会自动更新显示"
    )
    
    # 实时保存笔记到task对象
    task.work_notes = st.session_state.work_notes_input
    
    st.divider()
    
    # 完成任务按钮
    if st.button("✅ 完成任务", key="finish_work_button"):
        # 计算实际花费时间
        if st.session_state.timer_start_time:
            import time
            actual_time_seconds = int(time.time() - st.session_state.timer_start_time)
            actual_hours = actual_time_seconds // 3600
            actual_minutes = (actual_time_seconds % 3600) // 60
            actual_seconds = actual_time_seconds % 60
            task.actual_time = f"{actual_hours:02d}:{actual_minutes:02d}:{actual_seconds:02d}"
        else:
            task.actual_time = "00:00:00"
        
        # 停止计时器
        st.session_state.timer_running = False
        
        st.success("任务执行完成！现在去记录结果吧 📊")
        st.session_state.current_page = "Result"
        st.rerun()


def result_page():
    task = st.session_state.task # 获取 session 中的 task
    st.title("Result")
    
    # 显示分析和预测页面的信息
    st.subheader("📋 任务回顾")
    
    # 创建一个展开的区域显示所有之前的信息
    with st.expander("查看完整任务信息", expanded=True):
        # 分析信息
        st.write("### 📊 分析阶段")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Task内容:**")
            if task.analyze.content:
                st.info(task.analyze.content)
            else:
                st.write("*未填写*")
            
            st.write("**基线要求:**")
            if task.analyze.baseline:
                st.info(task.analyze.baseline)
            else:
                st.write("*未填写*")
        
        with col2:
            st.write("**目标原因:**")
            if task.analyze.why:
                st.info(task.analyze.why)
            else:
                st.write("*未填写*")
        
        st.divider()
        
        # 预测信息
        st.write("### 🔮 预测阶段")
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("**最坏结果:**")
            if task.prediction.worst_result:
                st.warning(task.prediction.worst_result)
            else:
                st.write("*未填写*")
        
        with col4:
            st.write("**发生概率:**")
            if task.prediction.probability is not None:
                prob_percent = task.prediction.probability * 100
                st.metric("概率", f"{prob_percent:.1f}%")
            else:
                st.write("*未设置*")
        
        st.divider()
        
        # 工作阶段信息
        st.write("### 🚀 工作阶段")
        col5, col6 = st.columns(2)
        
        with col5:
            st.write("**计划时间:**")
            if task.analyze.time:
                st.info(f"⏰ {task.analyze.time}")
            else:
                st.write("*未设置*")
        
        with col6:
            st.write("**实际用时:**")
            if hasattr(task, 'actual_time') and task.actual_time:
                st.success(f"⏱️ {task.actual_time}")
            else:
                st.write("*未记录*")
    
    st.divider()
    
    # 结果部分
    st.subheader("✅ 结果记录")
    
    # Use a key for the selectbox to directly manage its state in st.session_state
    # Initialize if not present
    if "result_finished_selection" not in st.session_state:
        st.session_state.result_finished_selection = 0 if task.result.finished else 1

    finished_selection = st.selectbox("Finished", ["Yes", "No"], index=st.session_state.result_finished_selection, key="result_finished_selection_widget")
    task.result.finished = finished_selection == "Yes"

    # 如果选择了"No"，则Quality显示为"未完成"且不可修改
    if finished_selection == "No":
        st.text_input("Quality", value="未完成", disabled=True, key="quality_disabled")
        task.result.quality = "未完成"
    else:
        # 如果选择了"Yes"，则显示正常的Quality选择框
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
        st.session_state.work_notes_input = ""  # 初始化工作笔记
        st.session_state.result_finished_selection = 1  # Default to "No"
        st.session_state.review_affirmation_input = task.review.affirmation
        st.session_state.review_areas_for_improvement_input = task.review.areas_for_improvement
        
        st.session_state.current_page = "Analyze"
        st.rerun()