# Week 7: Secure Authentication System

**Student Name:** Anjali Marimootoo  
**Student ID:** M01069323  
**Course:** CST1510 - CW2 - Multi-Domain Intelligence Platform – Secure User Authentication  

---

## Project Description
A command-line authentication system that implements secure password hashing and user management for the Multi-Domain Intelligence Platform.  
This system allows users to register accounts, log in with verified credentials, and manage sessions safely using modern security practices.

---

## Features
- Secure password hashing using bcrypt with automatic salt generation  
- User registration with duplicate username prevention  
- User login with password verification  
- Input validation for usernames and passwords  
- Password strength indicator (Weak / Medium / Strong)  
- Role-based account creation (user / admin / analyst)  
- Account lockout after 3 failed login attempts (5 minutes)  
- Session management via secure token (`sessions.json`)  
- File-based user data persistence  

---

## Technical Implementation

- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`, `sessions.json`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters), must include upper/lower/digit/special char

---

## Testing
Run the program and perform these verification tests:

- Register New User: Displays success message after valid registration.

- Duplicate Registration: Prevents duplicate usernames with error message.

- Successful Login: Grants access and shows “Welcome, username!”.

- Wrong Password: Denies access and displays “Error: Invalid password.”

- Non-existent User: Displays “Error: Username not found.”

---

## Installation and Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run the authentication system
python auth.py

