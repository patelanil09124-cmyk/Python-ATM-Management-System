# 🏦 Python ATM Management System

A professional ATM Management System developed using **Python**,
**Object-Oriented Programming (OOP)**, and **PostgreSQL**. 
The project simulates real-world ATM operations with secure user management,
transaction handling, and an admin panel.

---

# 🚀 Features

## User Features
- Create User Account
- Secure User Login
- Deposit Money
- Withdraw Money
- Money Transfer
- Transaction History
- Change PIN

## Admin Features
- Show All Users
- Search User
- Delete User
- Reset User PIN
- System Statistics
- Database Backup
- Database Restore
- System Shutdown

---

# 🛠 Technologies Used

- Python 3
- PostgreSQL
- Psycopg
- Object-Oriented Programming (OOP)
- Git
- GitHub

---

# 📂 Project Structure

```
SBIATM/
│
├── admin.py
├── atm.py
├── database.py
├── storage.py
├── transaction.py
├── user.py
├── validator.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── backups/
```

---

# 🗄 Database Schema

## Users Table

| Column | Type |
|---------|------|
| id | SERIAL |
| user_id | VARCHAR(25) |
| pin | VARCHAR(4) |
| balance | DECIMAL(12,2) |
| created_at | TIMESTAMP |

---

## Transactions Table

| Column | Type |
|---------|------|
| id | SERIAL |
| user_id | VARCHAR(25) |
| transaction_type | VARCHAR(20) |
| amount | DECIMAL(12,2) |
| sender_id | VARCHAR(25) |
| receiver_id | VARCHAR(25) |
| transaction_date | TIMESTAMP |

---

# 🏗 System Architecture

```
User
   │
   ▼
ATM
   │
   ▼
Admin / User
   │
   ▼
Storage Layer
   │
   ▼
PostgreSQL Database
```

---

# ⚙ Installation

## 1. Clone Repository

```bash
git clone https://github.com/patelanil09124-cmyk/Python-ATM-Management-System.git
```

## 2. Open Project

```bash
cd Python-ATM-Management-System
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Create PostgreSQL Database

```sql
CREATE DATABASE atm_db;
```

## 5. Configure Environment Variables

Create a `.env` file in the project root.

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=atm_db
DB_USER=postgres
DB_PASSWORD=your_password
```

## 6. Create Database Tables

Run

```bash
python database.py
```

## 7. Start Application

```bash
python main.py
```

---

# 💾 Backup & Restore

The Admin Panel supports:

- Database Backup (.backup)
- Database Restore
- Automatic Backup File Management

All backup files are stored inside:

```
backups/
```

---

# 📈 System Statistics

The application displays:

- Total Users
- Total Balance
- Total Transactions

---

# 🔮 Future Improvements

- Bcrypt PIN Encryption
- Block / Unblock Users
- Admin Activity Logs
- Repository Pattern
- Logging Module
- Unit Testing
- Email Notifications
- Account Lock After Multiple Failed Login Attempts

---

# 📸 Screenshots

You can add screenshots of:

- Main Menu
- User Menu
- Admin Menu
- Transaction History
- PostgreSQL Tables
- Backup & Restore

---

# 👨‍💻 Author

**Anil Kumar Patel**

- GitHub: https://github.com/patelanil09124-cmyk
- LinkedIn: https://www.linkedin.com/in/anil-patel-0b314b425

---

# ⭐ If you like this project, don't forget to give it a Star.

