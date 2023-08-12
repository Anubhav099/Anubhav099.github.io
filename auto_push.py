import os
import subprocess
from datetime import datetime, timedelta

def git_status():

    print("\nRunning 'git status' command...")
    try:
        subprocess.run("git status", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: 'git status' command failed.")
        return False
    return True

def get_previous_date():
    current_date = datetime.now()
    if current_date.hour < 6:  # If current time is before 6 AM, set the date to previous day
        current_date -= timedelta(days=1)
    return current_date.strftime("%d:%m:%Y").replace(" ", "0")

def git_add_commit_n_push(optional_message = None):
    choice = input("\nDo you want to push?: ")
    if choice.lower() in ['y','yes','ok','hmm','hmmph','yup','yo']:
        try:
            subprocess.run("git add *", shell=True, check=True)

            msg = get_previous_date()
            if optional_message:
                msg += f" - {optional_message}"
            
            commit_message = f'git commit -m "{msg}"'
            subprocess.run(commit_message, shell=True, check=True)
            print("Commit successful!\n")
            return True

        except subprocess.CalledProcessError:
            print("Error: Commit failed.")
            return False
    else:
        print("Aborted.")
        return False

def git_push():
    try:
        subprocess.run("git push", shell=True, check=True)
        print("Push successful!\n")
        return True
    except subprocess.CalledProcessError:
        print("Error: Push failed.")
        return False

if __name__ == "__main__":
    optional_message = input("Optional message: ")
    status_successful = git_status()
    if status_successful:
        commit_successful = git_add_commit_n_push(optional_message)
        if commit_successful:
            git_push()