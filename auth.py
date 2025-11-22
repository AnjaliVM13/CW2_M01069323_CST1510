# ---------------------- IMPORTS ----------------------
import bcrypt  # Library for hashing passwords securely
import os      # For file operations
import secrets # For session tokens
import json    # For storing sessions
import time    # For timestamps

# ---------------------- FILE PATHS & SETTINGS ----------------------
USER_DATA_FILE = "users.txt"
FAILED_ATTEMPTS_FILE = "failed_attempts.txt"
SESSION_FILE = "sessions.json"
LOCK_DURATION = 300  # 5 minutes lockout

# ---------------------- PASSWORD HASHING ----------------------
def hash_password(plain_text_password):
    """Hashes a password with bcrypt."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """Checks if plaintext password matches stored hash."""
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# ---------------------- PASSWORD VALIDATION ----------------------
def validate_password(password):
    """Checks password rules: length, digits, upper/lower, special."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*()-_=+[]{};:,<.>/?\\|~" for char in password):
        return False, "Password must contain at least one special character."
    return True, ""

def check_password_strength(password):
    """Evaluates password as Weak, Medium, or Strong."""
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()-_=+[]{};:,<.>/?\\|~" for c in password)

    # Count character types present
    score = sum([has_lower, has_upper, has_digit, has_symbol])

    # Determine strength
    if len(password) < 8 or score <= 1:
        return "Weak"
    elif score == 2 or score == 3:
        return "Medium"
    else:
        return "Strong"

# ---------------------- USERNAME VALIDATION ----------------------
def validate_username(username):
    """Ensures username is valid: >=3 chars, no spaces, alphanumeric."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if " " in username:
        return False, "Username cannot contain spaces."
    if not username.isalnum():
        return False, "Username must be alphanumeric (letters and numbers only)."
    return True, ""

# ---------------------- ACCOUNT LOCKOUT ----------------------
def record_failed_attempt(username):
    """Records a failed login attempt and returns current count."""
    attempts = {}
    if os.path.exists(FAILED_ATTEMPTS_FILE):
        with open(FAILED_ATTEMPTS_FILE, 'r') as f:
            for line in f:
                try:
                    user, count, ts = line.strip().split(',')
                    attempts[user] = [int(count), float(ts)]
                except ValueError:
                    continue

    count, ts = attempts.get(username, [0, 0])
    if time.time() - ts > LOCK_DURATION:
        count = 1
    else:
        count += 1

    attempts[username] = [count, time.time()]

    with open(FAILED_ATTEMPTS_FILE, 'w') as f:
        for user, (cnt, t) in attempts.items():
            f.write(f"{user},{cnt},{t}\n")

    return count

def reset_failed_attempts(username):
    """Resets failed attempts after successful login."""
    if not os.path.exists(FAILED_ATTEMPTS_FILE):
        return
    attempts = {}
    with open(FAILED_ATTEMPTS_FILE, 'r') as f:
        for line in f:
            try:
                user, count, ts = line.strip().split(',')
                attempts[user] = [int(count), float(ts)]
            except ValueError:
                continue

    if username in attempts:
        del attempts[username]

    with open(FAILED_ATTEMPTS_FILE, 'w') as f:
        for user, (cnt, t) in attempts.items():
            f.write(f"{user},{cnt},{t}\n")

def is_account_locked(username):
    """Checks if account is locked due to 3 failed attempts."""
    if not os.path.exists(FAILED_ATTEMPTS_FILE):
        return False
    with open(FAILED_ATTEMPTS_FILE, 'r') as f:
        for line in f:
            try:
                user, count, ts = line.strip().split(',')
                if user != username:
                    continue
                count, ts = int(count), float(ts)
                if count >= 3 and time.time() - ts < LOCK_DURATION:
                    return True
            except ValueError:
                continue
    return False

# ---------------------- SESSION MANAGEMENT ----------------------
def create_session(username):
    """Generates a session token and saves in JSON."""
    token = secrets.token_hex(16)
    session_data = {}
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            session_data = json.load(f)
    session_data[username] = {"token": token, "timestamp": time.time()}
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f)
    return token

# ---------------------- USER MANAGEMENT ----------------------
def user_exists(username):
    """Check if user already exists."""
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.strip().split(',')[0] == username:
                return True
    return False

def register_user(username, password, role="user"):
    """Registers a new user with role."""
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password},{role}\n")

    print(f"Success: User '{username}' registered as '{role}'!")
    return True

def login_user(username, password):
    """Logs in user if credentials correct and account not locked."""
    if is_account_locked(username):
        print(f"Error: Account '{username}' is locked. Try again later.")
        return False

    if not os.path.exists(USER_DATA_FILE):
        print("Error: Username not found.")
        return False

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue
            existing_username, stored_hashed_password, role = parts

            if existing_username == username:
                if verify_password(password, stored_hashed_password):
                    reset_failed_attempts(username)
                    session_token = create_session(username)
                    print(f"Success: Welcome, {username}! Role: {role}")
                    print(f"Session Token: {session_token}")
                    return True
                else:
                    print("Error: Invalid password.")
                    attempts = record_failed_attempt(username)
                    if attempts >= 3:
                        print(f"Account '{username}' is now locked for {LOCK_DURATION} seconds.")
                    return False

    print("Error: Username not found.")
    return False

# ---------------------- MENU DISPLAY ----------------------
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

# ---------------------- MAIN LOOP ----------------------
def main():
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            strength = check_password_strength(password)
            print(f"Password Strength: {strength}")

            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            role = input("Enter role (user/admin/analyst) [default: user]: ").strip().lower()
            if role not in ["user", "admin", "analyst"]:
                role = "user"

            register_user(username, password, role)

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            if login_user(username, password):
                print("\nYou are now logged in.")
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system. Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

# ---------------------- ENTRY POINT ----------------------
if __name__ == "__main__":
    main()





