from member import GoldenCredit, SilverCredit
from library import Library
from DataManager import JsonManager
import os
library = Library("Univers")

def intro():
    while True:
        print(
        """
        ~~~~~~~~~~~< Welcome >~~~~~~~~~~~
        a. Register for Golden credit
        b. Register for Silver credit
        c. Login 
        d. Exit
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """)
        chose = input(">>> ").lower()

        # clear console
        os.system("cls")

        if chose == "a":
            feature = GoldenCredit.feature()
            print("~~~~~~~~~~~~~~~~~< Description >~~~~~~~~~~~~~~~~~")
            print("Note: With golden credit, you can rent {} books.".format(feature["RentLimit"]))
            print("Rent time for every book: {} days".format(feature["ReturnTime"]))
            print("For delay in return book: you will block {} days".format(feature["BlockTime"]))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            input("Click Enter....")
            print("\n\n")

            print("~~~~~~~~~~~< Register >~~~~~~~~~~~")
            userName = input("Name:").strip()
            userId =   input("Id:").strip()
            userPass = input("Password:").strip()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            # clear console
            os.system("cls")

            creditType = "Golden"
            library.register(userId, userName, userPass, creditType)

        elif chose == "b":
            feature = SilverCredit.feature()
            print("~~~~~~~~~~~~~~~~~~~< Description >~~~~~~~~~~~~~~~~~~")
            print("Note: With golden credit, you can rent {} books.".format(feature["RentLimit"]))
            print("Rent time for every book: {} days".format(feature["ReturnTime"]))
            print("For delay in return book: you will block for {} days".format(feature["BlockTime"]))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            input("Click Enter....")
            print("\n\n")

            print("~~~~~~~~~~~< Register >~~~~~~~~~~~")
            userName = input("Name:").strip()
            userId =   input("Id:").strip()
            userPass = input("Password:").strip()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # clear console
            os.system("cls")

            creditType = "Silver"
            library.register(userId, userName, userPass, creditType)

        elif chose == "c":
            print("~~~~~~~~~~~< Login >~~~~~~~~~~~")
            userId =   input("Your id:").strip()
            userPass = input("Your password:").strip()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            # clear console
            os.system("cls")

            respons = library.login(userId, userPass)
            if isinstance(respons, GoldenCredit) or isinstance(respons, SilverCredit):
                main(respons)

        elif chose == "d":
            print("exit...")
            exit()
       
        else:
            print("please select the options with a, b or c")

def accountSection(user):
    while True:
        print(
        """
        ~~~~~~~~~~~~< Account >~~~~~~~~~~~~
        a. Info
        b. Change my id
        c. Change my name
        d. Change my password
        e. Support(Is Your account blocked?)
        f. history
        g. Delet account
        h. Back
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """)
        chose = input(">> ").lower()

        # clear console
        os.system("cls")

        if chose == "a":
            print("~~~~~~~~~~~~< Info >~~~~~~~~~~~~")
            print("Your Name: {}".format(user.name))
            print("Your Id: {}".format(user.Id))
            print("Credit Type: {}".format(user.creditType))
            print("Rented Books: {}".format(len(user.rentedBooks)))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            input("Click Enter...")

            # clear console
            os.system("cls")
        
        elif chose == "b":
            print("~~~~~~~~~~~< Change Id >~~~~~~~~~~~")
            newUserId = input("New Id:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # clear console
            os.system("cls")

            user.changeId(newUserId)
        
        elif chose == "c":
            print("~~~~~~~~~~~< Change Name >~~~~~~~~~~~")
            newUserName = input("New Name:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # clear console
            os.system("cls")

            user.changeName(newUserName)

        elif chose == "d":
            print("~~~~~~~~~~~< Change Password >~~~~~~~~~~~")
            oldUserPass = input("Old password:")
            newUserPass = input("New Password:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # clear console
            os.system("cls")

            user.changePassword(oldUserPass, newUserPass)
        
        elif chose == "e":
            user.support()

        elif chose == "f":
            
            if len(user.history) == 0:
                print("Your history is empty.")
            
            else:
                books = user.libraryBooks
                print("~~~~~~~~~~~~~~~< History >~~~~~~~~~~~~~~~")
                for data in user.history:
                    bookId, rentTime, returnTime = data
                    print("ID: {} -- {} - rent in {}: Return At: {}".format(
                        bookId, 
                        books[bookId]["Name"], 
                        rentTime, 
                        returnTime))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                input("Click Enter...")

                # clear console
                os.system("cls")

        
        elif chose == "g":
            print("Note: When you delet your account, your information cleared forever")
            answer = input("Are you sure(n/y)?").lower()
            if answer == "y":
                print("~~~~~~~~~~~~< Delet Account >~~~~~~~~~~~~")
                userPass = input("Password: ")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                # clear console
                os.system("cls")

                user.deletAccount(userPass)
                exit()
            else:
                # clear console
                os.system("cls")

                print("Cancel...")
                
        elif chose == "h":
            # clear console
            os.system("cls")

            print("Back...")
            break
        
        else:
            print("Please select options with (a, b, c, d, e, f, g)")
    
def main(user):
    """ user: an object of GoldenCredit or SilverCredit classes """

    while True:
        print("""
        ~~~~~~~~~~~~< Menu >~~~~~~~~~~~~
        a. Account
        b. Library
        c. Books list
        d. Rent a book
        e. Return a book
        f. My rented book
        g. Log out
        h. Exit
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """)
        chose = input(">> ").lower()
        
        # clear console
        os.system("cls")
        
        if chose == "a":
            accountSection(user)
        
        elif chose == "b":
            print(library)
        
        elif chose == "c":
            books = user.libraryBooks
            print("~~~~~~~~~~~~~~~< Books >~~~~~~~~~~~~~~~")
            for bookId, info in books.items():
                print("{} :: {} - {}; Rented: {}".format(
                    bookId,
                    info["Name"],
                    info["Autor"],
                    "Yes" if info["Rented"] else "No"
                ))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            input("Click Enter...")

            # clear console
            os.system("cls")



        elif chose == "d":
            print("Note: For find your book's id, first go to 'Book list'.")
            print("~~~~~~~~~~~~< Rent A Book >~~~~~~~~~~~~")
            bookId = input("Book id: ").strip()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # clear console
            os.system("cls")
            
            user.rentABook(bookId)
        
        elif chose == "e":
            print("Note: For find the book's id, first go to 'My rented book'")
            print("~~~~~~~~~~~~< Return A Book >~~~~~~~~~~~~")
            bookId = input("Book Id: ").strip()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # clear console
            os.system("cls")

            user.returnABook(bookId)
        
        elif chose == "f":
            
            rentedBooks = user.rentedBooks
            if rentedBooks == {}:
                print("You don't rent any book.")
            
            else:
                bookslist = user.libraryBooks
                print("~~~~~~~~~~~~~~~~< Your Rented Books >~~~~~~~~~~~~~~~~")
                for bookId, rentedDate in rentedBooks.items():
                    print("ID: {} -- Name: {}; Rented At: {}".format(
                        bookId,
                        bookslist[bookId]["Name"],
                        rentedDate
                    ))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                input("Click Enter...")
                
                # clear console
                os.system("cls")

        elif chose == "g":
            print("log out...")
            break

        elif chose == "h":
            print("Exit...")
            exit()
            
        else:
            print("Please select options with (a, b, c, d, e, f, g)")


if __name__ == "__main__":
    intro()