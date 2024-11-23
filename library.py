import mysql.connector
import datetime


mydb=mysql.connector.connect(host="localhost",user="root",passwd="1234")
mycursor=mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS library")
mycursor.execute("USE library")


def student_table():
    query = """
    CREATE TABLE IF NOT EXISTS student (
        student_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(25)
    )
    """
    mycursor.execute(query)
    mydb.commit()


def book_table():
    query = """
    CREATE TABLE IF NOT EXISTS book (
        book_id INT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        quantity INT
    )
    """
    mycursor.execute(query)
    mydb.commit()


def issued_books_table():
    query = """
    CREATE TABLE IF NOT EXISTS issued_books (
        issue_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50),
        book_id INT,
        issue_date DATE,
        due_date DATE,
        return_date DATE,
        status VARCHAR(25),
        FOREIGN KEY (student_id) REFERENCES student(student_id),
        FOREIGN KEY (book_id) REFERENCES book(book_id)
    )
    """
    mycursor.execute(query)
    mydb.commit()


def penalty_table():
    query = """
    CREATE TABLE IF NOT EXISTS penalty (
        student_id VARCHAR(50),
        total_penalty INT,
        PRIMARY KEY (student_id),
        FOREIGN KEY (student_id) REFERENCES student(student_id)
    )
    """
    mycursor.execute(query)
    mydb.commit()




def insert_student():
    while True :
        data=()
        print()
        student_id = input("Enter Student ID: ")
        student_name = input("Enter Student Name: ")
        email = input("Enter Student Email: ")
        phone = input("Enter Student Phone number: ")
        data=(student_id,student_name,email,phone)
        query="INSERT INTO student VALUES (%s, %s, %s,%s)"
        mycursor.execute(query,data)
        mydb.commit()
        print()
        ch=input("Do you wish to do add more Students?[Y/N] : ")
        if ch == "n" or ch == "N":
            break
    return   


def delete_student():
    while True:
        print()
        student_id=input(" Enter Student Id whose details to be deleted : ")  

        query = (f"DELETE FROM student WHERE student_id = '{student_id}' ")
        mycursor.execute(query)
        mydb.commit()
        ch=input("Do you wish to do delete more Students?[Y/N] : ")
        if ch == "n" or ch == "N":
            break
    return

def update_student():
    while True:
        print()
        data=()
        student_id = input(" Enter student Id for whose details need to be updated : ")
        student_name = input(" Enter Updated Student Name : ")
        student_phone = input(" Enter updated student phone no.: ")
        student_email = input("Enter updated student Email: ")

        query="UPDATE student SET  name = %s, email = %s, phone = %s WHERE student_id=%s"
        data=(student_name,student_email,student_phone,student_id)
        mycursor.execute(query,data)
        mydb.commit()

        print("Updated succesfully")
        ch=input("Do you wish to do update more Students?[Y/N] : ")
        if ch == "n" or ch == "N":
            break

    return   
    


def insert_book():
    while True :
        data=()
        print()
        Book_id = input(" Enter Book ID: ")
        Book_title =input(" Enter Book Name: ")
        author = input(" Enter Author Name: ")
        quantity = int(input(" Enter Book quantity: "))

        data=(Book_id, Book_title, author, quantity)

        query="INSERT INTO book VALUES (%s, %s, %s, %s)"
        mycursor.execute(query,data)
        mydb.commit()
        print()

        ch=input("Do you wish to do add more books?[Y/N] : ")
        if ch == "n" or ch == "N":
            break

    return


def delete_book():
    while True:
        print()
        Book_id = input(" Enter Book Id whose details to be deleted : ")
        mycursor.execute(f"DELETE FROM book WHERE book_id = '{Book_id}' ")
        mydb.commit()

        ch=input("Do you wish to do delete more book?[Y/N] : ")
        if ch == "n" or ch == "N":
            break

    return


def update_book():
    while True:
        print()
        data=()
        old_book_title = input(" Enter Book title for whose details need to be updated : ")

        new_book_title = input(" Enter updated Book Name : ")
        author = input(" Enter updated Author Name : ")
        qauntity = input(" Enter the updated Quantity : ")

        query="UPDATE book SET title = %s, author = %s, quantity = %s WHERE title = %s" 

        data=(new_book_title,author,qauntity,old_book_title)
        mycursor.execute(query,data)
        mydb.commit()

        print("Updated succesfully")

        ch=input("Do you wish to do update more Students?[Y/N] : ")
        if ch == "n" or ch == "N":
            break

    return


def issue_book():
    student_id = input("Enter your Student ID: ")
    
   
    mycursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
    student = mycursor.fetchone()
    
    if not student:
        print("Invalid Student ID. Please try again.")
        return
    
   
    book_id = input("Enter the Book ID you want to issue: ")
    
    mycursor.execute("SELECT * FROM issued_books WHERE student_id = %s AND book_id = %s AND status ='Issued'", (student_id, book_id))
    issued_book = mycursor.fetchone()
    
    if issued_book:
        print("You have already issued this book. You cannot issue the same book twice.")
        return
    
    
    mycursor.execute("SELECT * FROM book WHERE book_id = %s AND quantity > 0 ", (book_id,))
    book = mycursor.fetchone()
    
    if not book:
        print("This book is not available for issuing.")
        return
    
   
    issue_date = datetime.date.today()
    due_date = issue_date + datetime.timedelta(days=14) 
    
    query = """
    INSERT INTO issued_books (student_id, book_id, issue_date, due_date, status) 
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (student_id, book_id, issue_date, due_date, 'Issued')
    
    mycursor.execute(query, data)
    mydb.commit()
    
    
    mycursor.execute("UPDATE book SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
    mydb.commit()
    
    print("Book successfully issued!")
    input("Press any key to return to the User Menu")



def return_book():

    student_id = input("Enter your Student ID: ")

    mycursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
    student = mycursor.fetchone()
    
    if not student:
        print("Invalid Student ID. Please try again.")
        return
    
    mycursor.execute("SELECT * FROM issued_books WHERE student_id = %s AND status = 'Issued'", (student_id,))
    issued_books = mycursor.fetchall()

    if not issued_books:
        print("No books are currently issued to this student.")
        return


    print("\nBooks issued to you:")
    for book in issued_books:
        print(f"Book ID: {book[2]}, Issue Date: {book[3]}, Due Date: {book[4]}")


    book_id = input("\nEnter the Book ID of the book you want to return or report lost: ")

    mycursor.execute("SELECT * FROM issued_books WHERE student_id = %s AND book_id = %s AND status = 'Issued'", (student_id, book_id))
    issued_book = mycursor.fetchone()

    if not issued_book:
        print("This book was not issued to you or has already been returned.")
        return

    lost = input("Is the book lost? (Y/N): ").strip().lower()

    if lost == 'y':
        replacement_cost = 500 
        print(f"A penalty of {replacement_cost} will be added for the lost book.")

        query = "UPDATE issued_books SET status = 'Lost' WHERE student_id = %s AND book_id = %s"
        mycursor.execute(query, (student_id, book_id))
        mydb.commit()


        mycursor.execute("SELECT * FROM penalty WHERE student_id = %s", (student_id,))
        existing_penalty = mycursor.fetchone()

        if existing_penalty:
            new_total_penalty = existing_penalty[1] + replacement_cost
            mycursor.execute("UPDATE penalty SET total_penalty = %s WHERE student_id = %s", (new_total_penalty, student_id))
        else:
            mycursor.execute("INSERT INTO penalty (student_id, total_penalty) VALUES (%s, %s)", (student_id, replacement_cost))

        mydb.commit()

        print(f"Book reported as lost. A penalty of {replacement_cost} has been added to your account.")


    else:
       
        return_date = datetime.date.today()
        due_date = issued_book[4] 
        penalty_per_day = 5  
        penalty = 0

        if return_date > due_date:
            days_late = (return_date - due_date).days
            penalty = days_late * penalty_per_day
            print(f"You are {days_late} days late. The penalty is {penalty}.")


        query = "UPDATE issued_books SET return_date = %s, status = 'Returned' WHERE student_id = %s AND book_id = %s"
        data = (return_date, student_id, book_id)
        mycursor.execute(query, data)
        mydb.commit()

        mycursor.execute("UPDATE book SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
        mydb.commit()


        if penalty > 0:
            mycursor.execute("SELECT * FROM penalty WHERE student_id = %s", (student_id,))
            existing_penalty = mycursor.fetchone()

            if existing_penalty:
                new_total_penalty = existing_penalty[1] + penalty
                mycursor.execute("UPDATE penalty SET total_penalty = %s WHERE student_id = %s", (new_total_penalty, student_id))
            else:
                mycursor.execute("INSERT INTO penalty (student_id, total_penalty) VALUES (%s, %s)", (student_id, penalty))

            mydb.commit()


        print("Book returned successfully!")
        if penalty > 0:
            print(f"A penalty of {penalty} has been added to your account.")

    input("Press any key to return to the User Menu")


def show_student():
    mycursor.execute("SELECT * FROM student")
    rows = mycursor.fetchall()

    for x in rows:
        print(x)

def show_book():
    mycursor.execute("SELECT * FROM book")
    rows = mycursor.fetchall()

    for x in rows:
        print(x)
   

def show_issued_book():
    mycursor.execute("SELECT * FROM issued_books")
    rows = mycursor.fetchall()

    for x in rows:
        print(x)

def show_penalty():
    mycursor.execute("SELECT * FROM penalty")
    rows = mycursor.fetchall()

    for x in rows:
        print(x)


student_table()
book_table()
issued_books_table()
penalty_table()



while True:
        print("\n*****LIBRARY MANAGEMENT SYSTEM*****")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Add Book")
        print("5. Update Book")
        print("6. Delete Book")
        print("7. Issue Book")
        print("8. Return Book")
        print("9. Show Student Table")
        print("10. Show Book Table")
        print("11. Show Issued book Table")
        print("12. Show Penalty Table")
        print("13. Exit\n")

        c = input("Enter your choice: ")

        if c == '1':
            insert_student()
        elif c == '2':
            update_student()
        elif c == '3':
            delete_student()
        elif c == '4':
            insert_book()
        elif c == '5':
            update_book()
        elif c == '6':
            delete_book()
        elif c == '7':
            issue_book()
        elif c == '8':
            return_book()
        elif c == '9':
            show_student()
        elif c == '10':
            show_book()
        elif c == '11':
            show_issued_book()
        elif c == '12':
            show_penalty()
        elif c == '13':
            break
        else:
            print("Invalid value . Please try again.")



