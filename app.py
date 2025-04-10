
import streamlit as st
from gherkin_generator import save_to_feature_file, git_commit_and_push
from langchain_agent import generate_gherkin_langchain
from jira import JIRA

st.title("Gherkin Test Case Generator")
st.markdown("Fetch user stories from Jira, convert to Gherkin using LangChain + Ollama, and push to GitHub.")

# Jira Configuration
with st.expander("1. Jira Configuration"):
    jira_url = st.text_input("Jira Base URL", "https://your-domain.atlassian.net")
    email = st.text_input("Email")
    token = st.text_input("API Token", type="password")
    project_key = st.text_input("Jira Project Key")

    if st.button("Fetch User Stories"):
        try:
            jira = JIRA(server=jira_url, basic_auth=(email, token))
            issues = jira.search_issues(f'project={project_key}')
            st.session_state["stories"] = [{"key": i.key, "summary": i.fields.summary, "description": i.fields.description} for i in issues]
            st.success(f"Fetched {len(issues)} stories.")
        except Exception as e:
            st.error(f"Error fetching stories: {e}")

# User Story Selection
if "stories" in st.session_state:
    story = st.selectbox("2. Select a User Story", st.session_state["stories"],
                         format_func=lambda x: f"{x['key']}: {x['summary']}")

    if st.button("3. Generate Gherkin"):
        with st.spinner("Generating using LangChain + Ollama..."):
            gherkin_output = generate_gherkin_langchain(story["description"])
            st.session_state["gherkin_output"] = gherkin_output
            st.text_area("Generated Gherkin", value=gherkin_output, height=300)

# GitHub Integration
with st.expander("4. GitHub Configuration & Push"):
    repo_path = st.text_input("Local Git Repository Path")
    branch_name = st.text_input("Branch Name", "main")

    if st.button("Save & Push to GitHub"):
        try:
            filename = save_to_feature_file(st.session_state["gherkin_output"], story["key"])
            git_commit_and_push(repo_path, filename, f"Add Gherkin for {story['key']}", branch_name)
            st.success(f"Feature file saved and pushed to GitHub: {filename}")
        except Exception as e:
            st.error(f"Failed to push to GitHub: {e}")
