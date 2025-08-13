from pathlib import Path
import os

def summarize_project(project_dir):
    """Summarize the project structure and key files"""
    summary = {}
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.js', '.jsx', '.ts', '.tsx', '.py', '.html', '.css')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        summary[rel_path] = content[:500] + "..." if len(content) > 500 else content
                except:
                    summary[rel_path] = "[File could not be read]"
    return summary