import streamlit as st

st.set_page_config(page_title="Sample Weekly Plan", page_icon="📋")

def sample_plan_demo():
    st.title("📋 Sample Weekly Plan")
    st.markdown("See how a personalized weekly plan looks")
    
    # Add a back button
    if st.button("← Back to Home"):
        st.switch_page("main.py")
    
    st.markdown("### 🎯 Example Goal")
    st.markdown("*Build 3 AI tools by December*")
    
    st.markdown("### 📋 Sample Weekly Plan")
    
    st.markdown("""
    # Weekly Plan for Building AI Tools
    
    ## 🎯 Main Objective
    Make significant progress on AI tool development with focused daily tasks.
    
    ## 📅 Daily Breakdown
    
    **Monday:** Research and plan the first AI tool
    - Spend 2 hours researching existing solutions
    - Define the core features and requirements
    - Create a basic project structure
    
    **Tuesday:** Start coding the first tool
    - Set up the development environment
    - Implement the basic framework
    - Create the main functionality
    
    **Wednesday:** Continue development and testing
    - Add error handling and validation
    - Write unit tests for core functions
    - Test with sample data
    
    **Thursday:** Polish and document
    - Improve user interface
    - Write documentation
    - Create a demo version
    
    **Friday:** Review and plan next tool
    - Test the complete tool
    - Gather feedback
    - Plan the second AI tool
    
    **Saturday:** Learning and research
    - Study new AI techniques
    - Research tools 2 and 3
    - Update skills as needed
    
    **Sunday:** Rest and reflection
    - Review the week's progress
    - Plan improvements
    - Prepare for next week
    
    ## 💡 Tips for Success
    - Focus on one tool at a time
    - Test frequently as you build
    - Document your progress
    - Stay consistent with daily work
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 Ready to create your own plan?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Start Setup", type="primary", use_container_width=True):
            st.switch_page("pages/1_Setup.py")
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    sample_plan_demo() 