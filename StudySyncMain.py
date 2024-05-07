import json
from datetime import datetime, timedelta

# Path to the JSON file where data will be stored
users_file = 'study_sync_data.json'

def load_data():
    """Load data from a JSON file."""
    try:
        with open(users_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    """Save data to a JSON file."""
    with open(users_file, 'w') as file:
        json.dump(data, file, indent=4)

def register_user(users):
    """Register a new user and return the username with additional info on privacy."""
    username = input("Enter your username to register: ")
    if username in users:
        print("Username already exists. Try logging in.")
    else:
        users[username] = {'sessions': []}
        save_data(users)
        print("Registration successful. Your data is stored locally and is not shared with any third parties.")
    return username

def log_study_session(users, username):
    """Log a new study session with time cost information."""
    subject = input("Enter the subject you studied: ")
    duration = input("Enter the duration (in hours): ")
    session = {'date': str(datetime.now()), 'subject': subject, 'duration': duration}
    users[username]['sessions'].append(session)
    save_data(users)
    print("Study session logged successfully. Logging each session helps build your personal study database for better planning.")

def view_study_sessions(users, username):
    """Display all study sessions for the user with indices."""
    sessions = users.get(username, {}).get('sessions', [])
    if not sessions:
        print("No study sessions found.")
        return False  # Indicates no sessions to edit or delete
    print("Here are your logged study sessions:")
    for index, session in enumerate(sessions, start=1):
        print(f"{index}. {session}")
    return True

def calculate_weekly_totals(users, username):
    """Calculate and display total study time for the current week."""
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)
    total_hours = sum(float(session['duration']) for session in users.get(username, {}).get('sessions', [])
                      if week_start <= datetime.fromisoformat(session['date'][:10]) <= week_end)
    print(f"Total study hours this week: {total_hours} hours")

def display_motivational_quote():
    """Display a motivational quote."""
    quotes = [
        "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
        "Learning is not attained by chance, it must be sought for with ardor and attended to with diligence. – Abigail Adams",
        "The beautiful thing about learning is that nobody can take it away from you. – B.B. King"
    ]
    import random
    print(random.choice(quotes))

def edit_or_delete_session(users, username):
    """Allow users to edit or delete study sessions with confirmation prompts."""
    if not view_study_sessions(users, username):  # Display sessions if any
        return  # Exit if no sessions to edit/delete

    action = input("Do you want to edit or delete a session? (edit/delete/no): ").lower()
    if action in ['edit', 'delete']:
        session_index = int(input(f"Enter the session number to {action}: ")) - 1
        if session_index < 0 or session_index >= len(users[username]['sessions']):
            print("Invalid session number. Returning to main menu.")
            return

        if action == 'edit':
            new_subject = input("Enter new subject: ")
            new_duration = input("Enter new duration (in hours): ")
            if input(f"Are you sure you want to update this session? (yes/no): ").lower() == 'yes':
                users[username]['sessions'][session_index] = {
                    'date': str(datetime.now()),
                    'subject': new_subject,
                    'duration': new_duration
                }
                print("Session updated successfully.")
        elif action == 'delete':
            if input("Are you sure you want to delete this session? (yes/no): ").lower() == 'yes':
                del users[username]['sessions'][session_index]
                print("Session deleted successfully.")

        save_data(users)
    elif action == 'no':
        print("No changes made.")
    else:
        print("Invalid option.")

def main_menu():
    """Main menu for the Study Sync application with mindful exit prompts."""
    ascii_art ="""
   _____ _             _        _____                  
  / ____| |           | |      / ____|                 
 | (___ | |_ _   _  __| |_   _| (___  _   _ _ __   ___ 
  \___ \| __| | | |/ _` | | | |\___ \| | | | '_ \ / __|
  ____) | |_| |_| | (_| | |_| |____) | |_| | | | | (__ 
 |_____/ \__|\__,_|\__,_|\__, |_____/ \__, |_| |_|\___|
                          __/ |        __/ |           
                         |___/        |___/            

    """

    print(ascii_art)
    users = load_data()
    print("Welcome to Study Sync, your companion for effective study management.")
    username = input("Please enter your username or type 'new' to register: ")
    if username == 'new':
        username = register_user(users)
    elif username not in users:
        print("Username not found. Please register.")
        return

    while True:
        print("""
        Main Menu:
        1. Log New Study Session
        2. View My Study Sessions
        3. Edit or Delete Study Session
        4. Study Time Averages 
        5. Motivational Quote
        6. Help
        7. Exit
        """)
        choice = input("Enter your choice: ")
        if choice == '1':
            log_study_session(users, username)
        elif choice == '2':
            view_study_sessions(users, username)
        elif choice == '3':
            edit_or_delete_session(users, username)
        elif choice == '4':
            calculate_weekly_totals(users, username)
        elif choice == '5':
            display_motivational_quote()
        elif choice == '6':
            print("Help Information: Use the menu to track your study sessions or get inspired with a quote! You may also view weekly totals or weekly/daily/monthly study time average metrics.")
        elif choice == '7':
            if input("Are you sure you want to exit? (yes/no): ").lower() == 'yes':
                print("Thank you for using Study Sync. Goodbye!")
                break
            else:
                continue
        else:
            print("Invalid choice. Please select a valid option from the menu.")

if __name__ == "__main__":
    main_menu()
