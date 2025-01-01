import os
import re
import time
import json
import hashlib
import keyboard
from printy import printy


def clear_terminal(): #clear the terminal for better UI
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(options: list): #menu interface
    def fancy_menu(options, current_selection: int): #graphical text for a better view
        clear_terminal()
        printy("-use the 'arrow keys' to navigate.", "g")
        printy("-use the 'space bar' to confirm your selection.", "g")
        printy("-use the 'q button' to quit the application.", "g")
        print("\n")

        for line in range(len(options)):
            if line == current_selection:
                printy("\t->" + f"[mBHI]{options[line]}@")
                print("\n")
            else:
                printy("\t" + options[line], "B")
                print("\n")
        print("\n")

    j = 0  #a while loop for switching between menu options
    fancy_menu(options, j)
    while True:
        if keyboard.is_pressed('up'):
            j -= 1
            fancy_menu(options, j % len(options))
            time.sleep(0.2) #giving the app a delay time to prevent multiple actions
        elif keyboard.is_pressed('down'):
            j += 1
            fancy_menu(options, j % len(options))
            time.sleep(0.2)
        elif keyboard.is_pressed('space'):
            break

    if options[j] == "Login":
        return signup_or_login("login")
    elif options[j] == "Signup":
        return signup_or_login("signup")
    # elif options[j] == "Leaderboard":
    #     return leaderboard()

def signup_or_login(entry):

    def check_mail(mail): #check the email format
        valid_email_pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        return bool(re.match(valid_email_pattern, mail))

    def check_password(password): #check the password format
        valid_password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!_]).{8,}$"
        return bool(re.match(valid_password_pattern, password))

    def check_username(username): #check the username format
        valid_username_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$'
        return bool(re.match(valid_username_pattern, username))

    def hash_password(password): #hash the password
        return hashlib.sha256(password.encode()).hexdigest()

    def load_accounts(): #loading json file content which has users data
        with open('account.json', 'r') as data:
            return json.load(data)

    def save_accounts(accounts): #save the changes made to users data on the jason file
        with open('account.json', 'w') as data:
            json.dump(accounts, data, indent=4)

    def retry_on_failure():
        for count in range(3, -1, -1):
            print("Retry in ", count)
            time.sleep(1)

    def signup(accounts): #enter email,username and password to signup
        while True:
            clear_terminal()
            email = input("Enter your email: ").strip()
            if any(member["email"] == email for member in accounts):
                print("This email already exists!")
                retry_on_failure()
            elif check_mail(email):
                break
            else:
                print("Please enter a valid email.")
                retry_on_failure()

        while True:
            clear_terminal()
            username = input("Enter your username: ")
            if any(member["username"] == username for member in accounts):
                print("This username already exists! Try another one.")
                retry_on_failure()
            elif check_username(username):
                break
            else:
                print("Username must be at least 4 characters long (and less than 20), which can include letters, numbers and underline.")
                retry_on_failure()

        while True:
            clear_terminal()
            password = input("Enter your password: ")
            if check_password(password):
                hashed_password = hash_password(password)
                break
            else:
                print("Invalid password. Password must contain at least 8 characters,"
                      " including an uppercase letter, a lowercase letter, a digit, and a special character.")
                retry_on_failure()

        accounts.append({"username": username, "email": email, "password": hashed_password,
                         "points": 0, "play_time": 0, "user_ID": len(accounts)}) #adding the new user info to our list
        save_accounts(accounts) #writing changes on json

        for count in range(3,-1, -1):
            clear_terminal()
            print("Signup successful!")
            print("Entering in ", count)
            time.sleep(1)
        return

    def login(accounts): #enter an existing email or username to login
        members = {member["username"]: member for member in accounts}
        members.update({member["email"]: member for member in accounts})
        while True:
            clear_terminal()
            email_or_username = input("Enter your email or username: ").strip()
            if email_or_username in members:
                member = members[email_or_username]
                break
            else:
                print("Email or username not found!")
                retry_on_failure()

        while True:
            clear_terminal()
            password = input("Enter your password: ")
            hashed_password = hash_password(password)

            if member["password"] == hashed_password:
                print(f"Welcome back, {member['username']}!")
                break
            else:
                print("Incorrect password. Please try again.")
                retry_on_failure()

        for count in range(3,-1, -1):
            clear_terminal()
            print("login successful!")
            print("Entering in ", count)
            time.sleep(1)
        return

    accounts = load_accounts() #load json file data
    if entry == "signup":
        signup(accounts)
    elif entry == "login":
        login(accounts)


menu(["Login", "Signup", "Leaderboard"])
