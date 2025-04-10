
import subprocess
import os

def save_to_feature_file(content, story_key, directory="features"):
    os.makedirs(directory, exist_ok=True)
    filename = f"{directory}/{story_key}.feature"
    with open(filename, "w") as f:
        f.write(content)
    return filename

def git_commit_and_push(repo_path, file_path, commit_msg, branch_name="main"):
    subprocess.run(["git", "-C", repo_path, "add", file_path])
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_msg])
    subprocess.run(["git", "-C", repo_path, "push", "origin", branch_name])
