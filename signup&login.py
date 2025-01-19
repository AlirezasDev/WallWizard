import re
import json
import hashlib

def signup_or_login(entry):
    def check_mail(mail):
        valid_email_pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        return bool(re.match(valid_email_pattern, mail))

    def check_password(password):
        valid_password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!_]).{8,}$"
        return bool(re.match(valid_password_pattern, password))

    def check_username(username):
        valid_username_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$'
        return bool(re.match(valid_username_pattern, username))

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_accounts():
        with open('account.json', 'r') as data:
            return json.load(data)

    def save_accounts(accounts):
        with open('account.json', 'w') as data:
            json.dump(accounts, data, indent=4)

    def signup(accounts):
        while True:
            email = input("Enter your email: ")
            if any(member["email"] == email for member in accounts):
                print("This email already exists!")
            elif check_mail(email):
                break
            else:
                print("Please enter a valid email.")

        while True:
            username = input("Enter your username: ")
            if any(member["username"] == username for member in accounts):
                print("This username already exists! Try another one.")
            elif check_username(username):
                break
            else:
                print("Username must be at least 4 characters long, which can include letters, numbers and underline.")

        while True:
            password = input("Enter your password: ")
            if check_password(password):
                hashed_password = hash_password(password)
                break
            else:
                print("Invalid password. Password must contain at least 8 characters,"
                      " including an uppercase letter, a lowercase letter, a digit, and a special character.")

        accounts.append({"username": username, "email": email, "password": hashed_password, "user_ID": len(accounts)})
        save_accounts(accounts)
        print("Signup successful!")

    def login(accounts):
        members = {member["username"]: member for member in accounts}
        members.update({member["email"]: member for member in accounts})

        while True:
            email_or_username = input("Enter your email or username: ")
            if email_or_username in members:
                member = members[email_or_username]
                break
            else:
                print("Email or username not found!")

        while True:
            password = input("Enter your password: ")
            hashed_password = hash_password(password)

            if member["password"] == hashed_password:
                print(f"Welcome back, {member['username']}!")
                break
            else:
                print("Incorrect password. Please try again.")

    accounts = load_accounts()
    if entry == "signup":
        signup(accounts)
    elif entry == "login":
        login(accounts)

signup_or_login(input("Enter 'signup' or 'login': "))
