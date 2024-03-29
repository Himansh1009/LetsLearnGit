import os
import sys
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to your Git repository
repo_path = '/home/himanshu1009/Desktop/everything_in_here/GITDEMO/githarkat'

# Check if the repository directory exists
if not os.path.exists(repo_path):
    print(f"Repository directory '{repo_path}' does not exist. Creating it...")
    try:
        os.makedirs(repo_path)
        print("Directory created successfully.")
    except Exception as e:
        print(f"Error occurred while creating directory: {str(e)}")
        sys.exit(1)

# Initialize Git repository object or create a new one if it doesn't exist
try:
    repo = Repo(repo_path)
except Exception as e:
    print(f"Error occurred while initializing Git repository: {str(e)}")
    sys.exit(1)

# Define a custom event handler for monitoring file system changes
class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.change_count = 0

    def on_modified(self, event):
        # Increment change count when a file is modified
        self.change_count += 1
        print("Change detected.")

        # If 50 changes are tracked, commit and push changes to GitHub
        if self.change_count >= 50:
            print("50 changes tracked. Pushing to GitHub...")
            self.commit_and_push_changes()
            self.change_count = 0

    def commit_and_push_changes(self):
        try:
            # Stage all changes
            repo.git.add('--all')

            # Commit changes
            repo.git.commit('-m', 'Automatic commit')

            # Push changes to GitHub
            origin = repo.remote(name='origin')
            origin.push()
            print("Changes pushed to GitHub.")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Initialize watchdog observer
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=repo_path, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
