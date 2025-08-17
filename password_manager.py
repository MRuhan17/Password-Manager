from cryptography.fernet import Fernet
import os

# Generate or load key
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
fernet = Fernet(key)

# File to store passwords
PASSWORD_FILE = "passwords.txt"

def add_password():
    website = input("Enter website/app name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    encrypted_password = fernet.encrypt(password.encode()).decode()

    with open(PASSWORD_FILE, "a") as f:
        f.write(f"{website}|{username}|{encrypted_password}\n")

    print("✅ Password saved securely!")

def view_passwords():
    if not os.path.exists(PASSWORD_FILE):
        print("⚠️ No saved passwords.")
        return

    with open(PASSWORD_FILE, "r") as f:
        for line in f.readlines():
            website, username, encrypted_password = line.strip().split("|")
            decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
            print(f"🌐 {website} | 👤 {username} | 🔑 {decrypted_password}")

def main():
    while True:
        print("\n=== Password Manager ===")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
