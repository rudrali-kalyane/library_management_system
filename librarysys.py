lib_books = {"Physics":{"author":"Albert Einstein","year": 1870,"available":1},
                "Chemistry":{"author":"Marie Curie","year": 1930,"available":1},
                "Mathematics":{"author":"Issac Newton","year": 1850,"available":1},
                "Biology":{"author":"Darwin","year": 1890,"available":1}
                }

c=0
while c!=5:
    print("Menu:")
    print("choice 1 :Add new book")
    print("choice 2 :Borrow or Return book")
    print("choice 3 :Show availability of books")
    print("choice 4 :Search book")
    print("choice 5 :Exit")
    print("\n")

    c = int(input("Enter your choice : "))
    print("\n")

    if c == 1 :
        key = (input("Enter the name of book :"))
        key = key.capitalize()
        author = input("Enter author name : ")
        year = input("Enter published year : ")
        lib_books.update({key:{"author":author,"year":year,"available":1}})

        print("\n")
        


    elif c == 2:
        avail = int(input("Return : 0\nBorrow : 1\nEnter :"))
        key = (input("Enter the name of book :"))
        key = key.capitalize()

        if avail == 1: 
            if lib_books[key]["available"]==1:
                print(f"Book is Available..\n{key} is issued..!!!")
                lib_books.update({key:{"available":0}})

            else :
                print(f"{key} book is not available...\nCheckout other books")

        else:
            lib_books.update({key:{"available":1}})
            print(f"{key} book received.\nThank you!")

        print("\n")

       

    elif c == 3 :
        print("Available Books")
        for i in lib_books.keys():
            
            if lib_books[i]["available"]==1:
                print(i)

        print("\n")

    elif c == 4 :

        key = input("Enter the name of book :")
        key = key.capitalize()

        if key in lib_books.keys():
            print("Book is Available...")
            print(lib_books[key])

        else:
            print("Sorry...No Such book in library")


    else :
        if c!=5:
            print("Enter valid choice\n")

            

    


