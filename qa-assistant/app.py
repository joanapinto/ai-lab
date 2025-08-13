import streamlit as st
import tempfile
import os
import zipfile
from assistant import generate_qa_suggestions
from repo_parser import summarize_project

def extract_repo_description(repo_path):
    """Extract project description from repository path"""
    if repo_path.startswith('http'):
        # GitHub URL - extract basic info
        return f"Project from GitHub repository: {repo_path}"
    else:
        # Local path - use summarize_project
        try:
            # Ensure repo_path is a string and exists
            repo_path = str(repo_path)
            if not os.path.exists(repo_path):
                return f"Error: Path {repo_path} does not exist"
            
            summary = summarize_project(repo_path)
            
            # Convert summary dict to readable text
            project_text = f"Project analysis from {repo_path}:\n\n"
            for file_path, content in summary.items():
                project_text += f"File: {file_path}\nContent: {content}\n\n"
            
            return project_text
        except Exception as e:
            return f"Error analyzing project at {repo_path}: {str(e)}"

st.set_page_config(page_title="AI QA Assistant", layout="centered")

st.title("🧪 AI QA Assistant for Devs & Small Teams")
st.markdown("Generate test strategies and Playwright code based on your project.")

# Step 1 – Choose input method
input_method = st.radio(
    "How would you like to describe your project?",
    ("GitHub/local folder", "Manual description"),
    index=0
)

project_description = ""

# Step 2 – Input form
if input_method == "GitHub/local folder":
    uploaded_zip = st.file_uploader("Upload your zipped project folder", type="zip")
    if uploaded_zip is not None:
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Save uploaded file to temp zip
                tmp_zip_path = os.path.join(tmp_dir, "uploaded.zip")
                with open(tmp_zip_path, "wb") as f:
                    f.write(uploaded_zip.getbuffer())
                
                # Extract zip to temporary directory
                with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(tmp_dir)
                
                # Find the actual project directory (might be nested)
                project_dir = tmp_dir
                for item in os.listdir(tmp_dir):
                    # Skip system folders like __MACOSX
                    if item.startswith('__') or item in ['.DS_Store', 'Thumbs.db']:
                        continue
                    item_path = os.path.join(tmp_dir, item)
                    if os.path.isdir(item_path):
                        project_dir = item_path
                        break
                
                repo_text = extract_repo_description(project_dir)
                response = generate_qa_suggestions(repo_text)
            st.success("Project analyzed!")
            st.markdown(response)
        except Exception as e:
            st.error(f"❌ Error analyzing project: {str(e)}")

elif input_method == "Manual description":
    project_description = st.text_area("📝 Describe your project", placeholder="e.g. I'm building a React app with login and a dashboard.")

# Step 3 – Generate suggestions
if st.button("🚀 Generate QA Suggestions"):
    if not project_description.strip():
        st.warning("Please provide a valid project description first.")
    else:
        with st.spinner("Thinking..."):
            response = generate_qa_suggestions(project_description)
        st.markdown("### ✅ Suggestions")
        st.markdown(response)