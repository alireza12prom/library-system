from DataManager import JsonManager
from user import User
import datetime
jsLib = JsonManager()

class GoldenCredit(User):
    # with golden credit, we can rent a book for 20 days and can only rent 10 books
    # if we return book next 21 days or more, our account will block for 2 days
    _rentLimit = 10  # books
    _blockTime = 2   # days  
    _returnTime = 20 # days
    def __init__(self, Id, name, password):
        super().__init__(Id, name, password, "Golden")

    @classmethod
    def feature(cls):
        return {"RentLimit":cls._rentLimit, "BlockTime":cls._blockTime, "ReturnTime":cls._returnTime}

    @property  
    def libraryBooks(self):
        books = jsLib.pullData()["Books"]
        return books

    @property
    def rentedBooks(self):
        userInfo = self._getUserById(self._id)
        return userInfo["RentedBooks"]
    
    @property
    def history(self):
        userInfo = self._getUserById(self._id)
        return userInfo["History"]



    @staticmethod
    def _getUserById(userId:str):
        users = jsLib.pullData()["Users"]
        return users[userId] if userId in users else None

    @staticmethod
    def _getBookById(bookId:str):
        books = jsLib.pullData()["Books"]
        return books[bookId] if bookId in books else None
    
    @staticmethod
    def _calculateInterval(date1:str, date2:str):
        """ date: day/month/year """
        monthMap = {
            1:31,
            2:28,
            3:31,
            4:30,
            5:31,
            6:30,
            7:31,
            8:31,
            9:30,
            10:31,
            11:30,
            12:31
        }

        day1, month1, year1 = date1.split("/")
        day1, month1, year1 = int(day1), int(month1), int(year1)

        day2, month2, year2 = date2.split("/")
        day2, month2, year2 = int(day2), int(month2), int(year2)

        days = 0
        while day1 != day2:
            if day1 == monthMap[month1]:
                if month1 == 12:
                    year1 += 1
                    month1 = 1
                else:
                    month1 += 1
                day1 = 0
            day1 += 1
            days += 1
            
        
        while month1 != month2:
            if month1 == 13:
                year1 += 1
                month1 = 1
            else:
                days += monthMap[month1]
                month1 += 1
        
        while year1 != year2:
            year1 += 1
            days += 361
        
        return days

    @staticmethod
    def _date():
        now = datetime.datetime.now()
        date = "{}/{}/{}".format(now.day, now.month, now.year)
        return date


    def rentABook(self, bookId:str):
        # check user status
        userInfo = self._getUserById(self._id)
        if userInfo["BlockedStatus"] != []:
            print("You account was blocked,\n for more information refer to the 'Account\Support'.")
            return -1

        elif len(userInfo["RentedBooks"]) >= self._rentLimit:
            print("Every member with {} credit can rent {} books in total.".format(
               self._creditType, 
               self._rentLimit
            ))
            return -1

        # check book status
        bookInfo = self._getBookById(bookId)
        if bookInfo == None:
            print("There is no book with this id")
            return -1
        
        elif bookInfo["Rented"]:
            print("Sorry, This book already rented")
            return -1

        
        # add book to rented books!
        jsLib.updateData("Books", bookId, "Rented", True)
        
        userInfo["RentedBooks"].update({bookId:self._date()})
        jsLib.updateData("Users", self._id, "RentedBooks", userInfo["RentedBooks"])
        
        print("{} - {}; rented successfully at {}".format(bookId, bookInfo["Name"], self._date()))
        print("You must return this book next {} days. overwise your account will block for {} day(s)".format(self._returnTime, self._blockTime))
    
    def returnABook(self, bookId:str):
        
        userInfo = self._getUserById(self._id)
        if bookId not in userInfo["RentedBooks"]:
            print("You didn't rent this book")
            return -1
        
        # remove book from rented books
        jsLib.updateData("Books", bookId, "Rented", False) 

        rentedDate= userInfo["RentedBooks"].pop(bookId)
        jsLib.updateData("Users", self._id, "RentedBooks", userInfo["RentedBooks"])

        # update history (bookId, rent date, return date)
        userInfo["History"].append((bookId, rentedDate, self._date()))
        jsLib.updateData("Users", self._id, "History", userInfo["History"])

        # calculating how many days user rent the book
        delta = self._calculateInterval(rentedDate, self._date())
        
        bookInfo = self._getBookById(bookId)
        print("{}-(Name: {}, Autor: {}); Rented {} for {} day(s).".format(
            bookId, 
            bookInfo["Name"], 
            bookInfo["Autor"], 
            rentedDate, 
            delta))

        if delta > self._returnTime:

            if userInfo["BlockedStatus"] == []:
                userInfo["BlockedStatus"] = [self._date(), self._blockTime]
                print("Your account for this delay will block for {} day(s).".format(self._blockTime))
            
            else:
                date, days = userInfo["BlockedStatus"]
                if self._calculateInterval(date, self._date()) > days:
                    userInfo["BlockedStatus"] = [self._date(), 0]
            
                userInfo["BlockedStatus"][1] += self._blockTime
                print("Your account blocked time increased by {} day(s)".format(self._blockTime))
            
            jsLib.updateData("Users", self._id, "BlockedStatus", userInfo["BlockedStatus"])
        else:
            print("Thanks for timely return")

    def support(self):
        userInfo = self._getUserById(self._id)
        if userInfo["BlockedStatus"] == []:
            print("Your account is not block")
            return -1
        else:
            date, days = userInfo["BlockedStatus"]
            if self._calculateInterval(date, self._date()) >= days:
                jsLib.updateData("Users", self._id, "BlockedStatus", [])
                print("Your account was block for {} day(s) at {},".format(days, date))
                print("So it is free now(^,^).")
            else:
                print("Sorry, your account was blocked at {} for {} days!".format(date, days))

    def deletAccount(self, password):
        userInfo = self._getUserById(self._id)
        if len(userInfo["RentedBooks"]) != 0:
            print("You rented {} book(s), first return those to library!".format(len(userInfo["RentedBooks"])))
            return -1
        jsLib.removeDataFromCategory("Users", self._id)
        print("Your account deleted successfully(^_^)")


class SilverCredit(GoldenCredit):
    # with silver credit, we can rent a book for 10 days and can only rent 5 books
    # if we return book next 11 days or more, our account will block for 3 days
    _rentLimit = 5   # books
    _blockTime = 3   # days 
    _returnTime = 10 # days
    def __init__(self, Id, name, password):
        User.__init__(self, Id, name, password, "Silver")

