import mysql.connector
from mysql.connector import errorcode

from datetime import datetime

class SQLFacade():
    config = {
      'user': 'root',
      'password': 'imis1000801',
      'host': '127.0.0.1',
      'database': 'bookstore',
      'raise_on_warnings': True,
    }

    def __init__(self):
        self.cnx = self.connect_SQL(self.config)
        self.cursor = self.cnx.cursor()

    def connect_SQL(self, config):
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists, create it.")
                return CreateDatabase(config)
            else:
                print(err)
                exit(1)
        else:
            return cnx

    def create_member(self, data):
        instruction =( "INSERT INTO  member (memberID, passwd, name, address, phone)"
            "VALUES (%(memberID)s, %(passwd)s, %(name)s, %(address)s, %(phone)s) ;")
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def find_member(self, data):
        instruction = "SELECT passwd FROM member WHERE memberID = %(memberID)s ;"
        print (instruction)
        self.cursor.execute(instruction, data)
        for passwd in self.cursor:
            print(passwd[0])
            if passwd[0] == data['passwd']:
                return True
        return False

    def add_item2shopping_cart(self, memberID, itemNumber, amountOfItem):
        orderID = self.get_shopping_cart_ID(memberID)
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber
        data['amountOfItem'] = amountOfItem

        instruction = ("INSERT INTO dispatch (orderID, itemNumber, amountOfItem )"
                        "VALUES (%(orderID)s, %(itemNumber)s, %(amountOfItem)s ) ;" )
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def remove_item_from_shopping_cart(self, memberID, itemNumber):
        orderID = self.get_shopping_cart_ID(memberID)
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber

        instruction = "DELETE FROM dispatch WHERE orderID=%(orderID)s AND itemNumber=%(itemNumber)s ; "
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def update_item_from_shopping_cart(self, memberID, itemNumber, amountOfItem):
        orderID = self.get_shopping_cart_ID(memberID)
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber
        data['amountOfItem'] = amountOfItem

        instruction = "UPDATE dispatch SET amountOfItem=%(amountOfItem)s WHERE orderID=%(orderID)s AND itemNumber=%(itemNumber)s ; "
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()
    
    def commit_shopping_cart(self, memberID, payway):
        orderID = self.get_shopping_cart_ID(memberID)
        data = dict()
        data['orderID'] = orderID
        data['payway'] = payway



       
    def create_shopping_cart(self,memberID):
        data = dict()
        data['memberID'] = memberID
        instruction =( "INSERT INTO  orderList (deliveryStatus, memberID)"
                        "VALUES (0,%(memberID)s) ;")
        print (instruction)
        self.cursor.execute(instruction, data )
        self.cnx.commit()
        # self.cursor.execute("SELECT LAST_INSERT_ID")
        # print(self.cursor)
        return self.get_shopping_cart_ID(memberID)

    def get_shopping_cart_ID(self, memberID):
        data = dict()
        data['memberID'] = memberID
        instruction = "SELECT orderID, deliveryStatus FROM orderList WHERE memberID=%(memberID)s"
        print (instruction)
        self.cursor.execute(instruction, data)
        for result in self.cursor:
            # this is shopping box
            if result[1] == 0:
                print (result)
                return result[0]
        print ('cant find order ID, create one')
        return self.create_shopping_cart(memberID) 

    def get_itemName(self, itemNumber):
        data = dict()
        data['itemNumber'] = itemNumber
        instruction = "SELECT title FROM book WHERE itemNumber=%(itemNumber)s ;"
        print (instruction)
        self.cursor.execute(instruction, data)
        
        for itemName in self.cursor:
            return itemName[0] 

    def get_shopping_cart(self, memberID):
        orderID = self.get_shopping_cart_ID(memberID)
        data = dict()
        data['orderID'] = orderID
        instruction =( "SELECT dispatch.itemNumber, book.title, dispatch.amountOfItem, book.listPrice, book.salePrice "
                       "FROM dispatch, book "
                       "WHERE orderID=%(orderID)s AND dispatch.itemNumber=book.itemNumber ;")
        print(instruction)
        self.cursor.execute(instruction, data)

        result = []
        for i in self.cursor:
            result.append(i)
            print (i)
        return result

    def find_book(self, keyword):
        keyword = '%' + keyword + '%'
        data = dict()
        data['keyword'] = keyword
        instruction = "SELECT * FROM book WHERE title LIKE %(keyword)s ;"
        print (instruction)
        self.cursor.execute(instruction, data)
        for i in self.cursor:
            print (i)
