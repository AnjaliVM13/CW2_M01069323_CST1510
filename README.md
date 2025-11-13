# Week 7: Secure Authentication System

**Student Name:** Anjali Marimootoo 
**Student ID:** M01069323
**Course:** CST1510 - CW2 - Multi-Domain Intelligence Platform  

---

##  Project Description
This project is a command-line authentication system that demonstrates **secure password handling** using the `bcrypt` hashing algorithm.  
It allows users to **register** and **log in** with strong validation and encrypted password storage.

---

##  Features
- Secure password hashing using **bcrypt** with automatic salt generation  
- **User registration** with duplicate username prevention  
- **User login** with password verification  
- Input validation for usernames and passwords  
- File-based user data persistence (`users.txt`)  

---

##  Technical Implementation
- **Hashing Algorithm:** bcrypt (automatic salt per password)  
- **Data Storage:** Plain text file (`users.txt`) with comma-separated values  
- **Password Security:** One-way hashing — no plaintext passwords are stored  
- **Validation Rules:**  
  - Username: 3–20 alphanumeric characters  
  - Password: At least 8 characters, must include uppercase, lowercase, number, and special character  