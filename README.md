Library Management System



A Python-based Library Management System that manages students, books, and book transactions like issuance, returns, and penalties, backed by a MySQL database.

✨ Features
Student Management: Add, update, delete, and view students.
Book Management: Add, update, delete, and view books.
Book Issuance: Issue books with due dates, avoid duplicate issuance.
Returns & Penalties: Handle returns, calculate late fees, and manage lost books.
🛠️ Prerequisites
Python 3.7+, MySQL 5.7+
Install mysql-connector-python:
bash
Copy code
pip install mysql-connector-python
⚙️ Setup
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
Create the database:
sql
Copy code
CREATE DATABASE library;
USE library;
Run the script:
bash
Copy code
python library_management_system.py
📋 Database Tables
student: Manages student records.
book: Stores book details.
issued_books: Tracks issued and returned books.
penalty: Maintains penalty records.
💰 Penalties
Late Returns: ₹5/day after the due date.
Lost Books: ₹500/book.
📜 License
This project is licensed under the MIT License.

Feel free to expand sections based on your project’s specifics!



