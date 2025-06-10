import streamlit as st
from pages import analyze_page, prediction_page, result_page, review_page
from task import Task
from database import initialize_database



# Initialize a global Task object in session state
if "task" not in st.session_state:
    st.session_state.task = Task()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Analyze"

def main():
    st.set_page_config(page_title="目标导向 + 去完美主义", page_icon="🎯")
    st.sidebar.title("Navigation")
    
    # Sidebar navigation

    page = st.sidebar.selectbox(
        "Select a page",
        ["Analyze", "Prediction", "Result", "Review"],
        index=["Analyze", "Prediction", "Result", "Review"].index(st.session_state.current_page)
    )

    #Update the current page based on sidebar selection
    st.session_state.current_page = page

    #Render the selected page
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
