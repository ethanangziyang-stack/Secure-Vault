import hashlib
import random
import string
import os
from cryptography.fernet import Fernet

# KEY MANAGEMENT (PERSISTENT)
KEY_FILE = "secret.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = load_or_create_key()
fernet = Fernet(key)

# DATABASE (IN MEMORY)
users = {}
secure_notes = {}  # username -> list of encrypted notes

# HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CREATE ACCOUNT
def create_account():
    username = input("Enter username: ")

    if username in users:
        print("Account already exists.\n")
        return

    password = input("Enter password: ")
    users[username] = hash_password(password)
    secure_notes[username] = []

    print("Account created successfully!\n")

# LOGIN
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == hash_password(password):
        print("Login successful!\n")
        user_menu(username)
    else:
        print("Invalid username or password.\n")

# PASSWORD GENERATOR
def generate_password():
    length = 14
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f"Generated Password: {password}\n")

# ENCRYPT / DECRYPT NOTES
def add_note(username):
    note = input("Enter your note: ")
    encrypted = fernet.encrypt(note.encode())
    secure_notes[username].append(encrypted)
    print("Note saved securely!\n")

def view_notes(username):
    print("\nYour Notes:")
    for i, note in enumerate(secure_notes[username], 1):
        decrypted = fernet.decrypt(note).decode()
        print(f"{i}. {decrypted}")
    print()

# USER MENU
def user_menu(username):
    while True:
        print("1. Add Secure Note")
        print("2. View Notes")
        print("3. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            add_note(username)
        elif choice == "2":
            view_notes(username)
        elif choice == "3":
            print("Logged out.\n")
            break
        else:
            print("Invalid choice.\n")

# START PROGRAM
def start_app():
    while True:
        print("Secure Password Manager")
        print("1. Create Account")
        print("2. Login")
        print("3. Generate Password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            generate_password()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

start_app()
