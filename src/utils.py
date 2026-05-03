from pathlib import Path

def confirm_overwrite(path: Path) -> bool:
    if not path.exists():
        return True
    
    while True:
        choice = input(f"{path.name} already exists, do you want to overwrite this file? y/n ")

        if choice == "y":
            return True  
        elif choice == "n":
            print("Skipping file.")
            return False
        else:
            print("Please enter 'y' or 'n'.")
            
def get_survey_summary(st):
    profile = st.session_state.get("user_profile", {})
    survey_summary = "\n".join(f"{k}: {v}" for k, v in profile.items())

    return survey_summary