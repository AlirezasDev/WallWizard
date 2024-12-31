import re
import json
import hashlib
def signup_or_login(entry):
    user = {}

    def check_mail(mail):
        valid_email_pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        if re.match(valid_email_pattern, mail):
            return True
        print("Please enter a valid email.")
        return False

    def check_password(password):
        valid_password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if re.match(valid_password_pattern, password):
            return True
        print("Invalid password. Password must contain at least 8 characters,"
              " including an uppercase letter, a lowercase letter, a digit, and a special character.")
        return False

    def check_username(username):
        valid_username_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$'
        if re.match(valid_username_pattern, username):
            return True
        print("Username must be at least 4 characters long, which can include letters, numbers and underline.")
        return False

    def hash_password(password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def signup():
        with open('account.json', 'r') as data:
            accounts = json.load(data)

        while True:
            email = input("Enter your email: ")
            if email in [members["email"] for members in accounts]:
                print("This email already exists!")
            elif check_mail(email):
                break

        while True:
            username = input("Enter your username: ")
            if username in [members["username"] for members in accounts]:
                print("This username already exists! Try another one.")
            elif check_username(username):
                break

        while True:
            password = input("Enter your password: ")
            if check_password(password):
                hashed_password = hash_password(password)
                break

        accounts.append({"username": username, "email": email, "password": hashed_password, "user_ID": len(accounts)})

        with open('account.json', 'w') as data:
            json.dump(accounts, data, indent= 4)

    def login():
        with open('account.json', 'r') as data:
            accounts = json.load(data)

        members_username = [members["username"] for members in accounts]
        members_email = [members["email"] for members in accounts]

        while True:
            email_or_username = input("Enter your email or username: ")
            if email_or_username in members_username:
                member_id =  members_username.index(email_or_username)
                break
            elif email_or_username in members_email:
                member_id = members_email.index(email_or_username)
                break
            else:
                print("Email or username not found!")

        while True:
            password = input("Enter your password: ")
            hashed_password = hash_password(password)

            if accounts[member_id]["password"] == hashed_password:
                print(f"Welcome back, {accounts[member_id]['username']}!")
                break
            else:
                print("Incorrect password. Please try again.")

    if entry == "signup":
        signup()
    elif entry == "login":
        login()

