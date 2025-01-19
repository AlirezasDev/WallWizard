import os
import re
import time
import json
import hashlib
from enum import member

import keyboard
from printy import printy

player1_id = ""
player2_id = ""
player1_username = ""
player2_username = ""

def load_accounts():  # loading json file content which has users data
    with open('account.json', 'r') as data:
        return json.load(data)

def save_accounts(accounts): #save the changes made to users data on the jason file
    with open('account.json', 'w') as data:
        json.dump(accounts, data, indent=4)

def clear_terminal(): #clear the terminal for better UI
    os.system('cls' if os.name == 'nt' else 'clear')


def menu(options: list): #menu interface
    global player1_username, player2_username
    time.sleep(0.2)
    clear_terminal()
    def fancy_menu(options1, current_selection: int): #graphical text for a better view
        clear_terminal()
        printy("-use the 'arrow keys' to navigate.", "g")
        printy("-use the 'space bar' to confirm your selection.", "g")
        print("\n")
        if len(player1_username) != 0:
            printy(f"player1 = {player1_username}", "gB")
        if len(player2_username) != 0:
            printy(f"player1 = {player2_username}", "gB")
        print("\n")
        for line in range(len(options1)):
            if line == current_selection:
                printy("\t->" + f"[mBHI]{options1[line]}@")
                print("\n")
            else:
                printy("\t" + options1[line], "B")
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
            time.sleep(0.2)
            break


    if options[j] == "Login":
        return signup_or_login("login")
    elif options[j] == "Signup":
        return signup_or_login("signup")
    elif options[j] == "Quit":
        while True:
            clear_terminal()
            yorn = input("Are you sure you want to quit?(y/n)")
            if yorn.strip().lower() == "y":
                for count in range(3):
                    for i in range(4):
                        print("\rExiting the app" + "." * i + " " * (3 - i), end="")
                        time.sleep(0.45)
                clear_terminal()
                print("\rBye!", end="")
                time.sleep(1)
                exit()
            elif yorn.strip().strip() == "n":
                menu(options)
    elif options[j] == "Leaderboard":
        return leaderboard()
    elif options[j] == "Main Menu":
        player1_id = ""
        player1_username = ""
        player2_id = ""
        player2_username = ""
        return menu(["Login", "Signup", "Leaderboard", "Quit"])
    elif options[j] == "New Game":
        return menu(["Login", "Signup", "Quit"])
    # elif options[j] == "Continue":

def signup_or_login(entry):
    time.sleep(0.1)
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

    def retry_on_failure():
        for count in range(3, -1, -1):
            print("\rRetry in ", count, end="")
            time.sleep(1)

    def signup(accounts): #enter email,username and password to signup
        global player1_username, player2_username, player1_id, player2_id
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
                         "points": 0, "wins": 0, "losses": 0,
                         "play_time": [0,0,0], "user_ID": len(accounts)}) #adding the new user info to our list
        save_accounts(accounts) #writing changes on json

        for count in range(3, -1, -1):
            print("\rSignup successful! Entering in ", count, end="")
            time.sleep(1)
        if len(player1_username) == 0:
            player1_id = len(accounts)
            player1_username = username
            return menu(["New Game", "Main Menu", "Quit"])
        elif len(player2_username) == 0:
            player2_id = len(accounts)
            player2_username = username
            return
            # return start_game()

    def login(accounts): #enter an existing email or username to login
        global player1_username, player2_username, player1_id, player2_id
        members = {member["username"]: member for member in accounts}
        members.update({member["email"]: member for member in accounts})
        while True:
            clear_terminal()
            email_or_username = input("Enter your email or username: ").strip()
            if len(player1_username) > 0:
                if email_or_username == player1_username or email_or_username == members[player1_username]["email"]:
                    print("This player has already logged in.")
                    retry_on_failure()
                    continue
                else:
                    if email_or_username in members:
                        member = members[email_or_username]
                        break
                    else:
                        print("Email or username not found!")
                        retry_on_failure()
                        continue
            elif email_or_username in members:
                member = members[email_or_username]
                break
            else:
                print("Email or username not found!")
                retry_on_failure()
                continue
        while True:
            clear_terminal()
            password = input("Enter your password: ")
            hashed_password = hash_password(password)

            if member["password"] == hashed_password:
                print(f"Welcome back, \033[33m{member['username']}\033[39m!")
                break
            else:
                print("Incorrect password. Please try again.")
                retry_on_failure()

        for count in range(3, -1, -1):
            print("\rLogin successful! Entering in ", count, end="")
            time.sleep(1)
        if len(player1_username) == 0:
            player1_id = member['user_ID']
            player1_username = member['username']
            return menu(["New Game", "Main Menu", "Quit"])
        elif len(player2_username) == 0:
            player2_id = member['user_ID']
            player2_username = member['username']
            return
            # return start_game()

    accounts = load_accounts() #load json file data
    if entry == "signup":
        signup(accounts)
    elif entry == "login":
        login(accounts)

def leaderboard():
    clear_terminal()
    users = load_accounts()
    sorted_users = sorted(users, key=lambda x: x["points"], reverse=True)

    printy("="*44+"TOP 3 PLAYERS"+"="*44, "BHw")
    printy(" {:30}{:<20}{:<15}{:<20}{:<15}".format("Username", "Points", "Wins", "Losses", "Play Time"), "BH")

    try:
        printy("  {:30}{:<+20}{:<15}{:<20}{:<14}".format(sorted_users[0]['username'], sorted_users[0]['points'],
                                             sorted_users[0]['wins'], sorted_users[0]['losses'],
                                                         f"{sorted_users[0]['play_time'][0]}h"
                                                         f"{sorted_users[0]['play_time'][1]}m"
                                                         f"{sorted_users[0]['play_time'][2]}s"), "BHy")
    except:
        pass
    try:
        printy("  {:30}{:<+20}{:<15}{:<20}{:<14}".format(sorted_users[1]['username'], sorted_users[1]['points'],
                                             sorted_users[1]['wins'], sorted_users[1]['losses'],
                                                         f"{sorted_users[1]['play_time'][0]}h"
                                                         f"{sorted_users[1]['play_time'][1]}m"
                                                         f"{sorted_users[1]['play_time'][2]}s"), "BHc")
    except:
        pass
    try:
        printy("  {:30}{:<+20}{:<15}{:<20}{:<14}".format(sorted_users[2]['username'], sorted_users[2]['points'],
                                             sorted_users[2]['wins'], sorted_users[2]['losses'],
                                                         f"{sorted_users[2]['play_time'][0]}h"
                                                         f"{sorted_users[2]['play_time'][1]}m"
                                                         f"{sorted_users[2]['play_time'][2]}s"), "BHm")
    except:
        pass

    printy("press 'q' to quit","D")
    printy("press 'm' to go back to the main menu","D")

    while True:
        if keyboard.is_pressed('q'):
            for count in range(3):
                for i in range(4):
                    print("\rExiting the app" + "." * i + " " * (3 - i), end="")
                    time.sleep(0.45)
            clear_terminal()
            print("\rBye!", end="")
            time.sleep(1)
            exit()

        if keyboard.is_pressed('m'):
            menu(["Login", "Signup", "Leaderboard", "Quit"])



menu(["Login", "Signup", "Leaderboard", "Quit"])
