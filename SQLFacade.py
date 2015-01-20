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
        instruction =( "INSERT INTO  member (memberID, passwd, name, address, phone,email)"
            "VALUES (%(memberID)s, %(passwd)s, %(name)s, %(address)s, %(phone)s, %(email)s) ;")
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

    def __item_exist_in_cart(self, orderID, itemNumber):
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber
        instruction = "SELECT COUNT(*) FROM dispatch WHERE orderID=%(orderID)s AND itemNumber=%(itemNumber)s;"
        self.cursor.execute(instruction, data)
        for count in self.cursor:
            print(count[0])
            if count[0] == 0:
                return False
            else:
                return True

    def add_item2shopping_cart(self, orderID, itemNumber, amountOfItem):
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber
        data['amountOfItem'] = amountOfItem

        instruction = ("INSERT INTO dispatch (orderID, itemNumber, amountOfItem )"
                        "VALUES (%(orderID)s, %(itemNumber)s, %(amountOfItem)s ) ;" )
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def update_item_from_shopping_cart(self, orderID, itemNumber, amountOfItem):
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber
        data['amountOfItem'] = amountOfItem

        instruction = "UPDATE dispatch SET amountOfItem=%(amountOfItem)s WHERE orderID=%(orderID)s AND itemNumber=%(itemNumber)s ; "
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def add_or_update_item2shopping_cart(self, memberID, itemNumber, amountOfItem):
        orderID = self.get_shopping_cart_ID(memberID)
        exist = self.__item_exist_in_cart(orderID, itemNumber)
        if exist:
            self.update_item_from_shopping_cart(orderID, itemNumber, amountOfItem)
        else:
            self.add_item2shopping_cart(orderID, itemNumber, amountOfItem)

    def remove_item_from_shopping_cart(self, memberID, itemNumber):
        orderID = self.get_shopping_cart_ID(memberID)
        data = dict()
        data['orderID'] = orderID
        data['itemNumber'] = itemNumber

        instruction = "DELETE FROM dispatch WHERE orderID=%(orderID)s AND itemNumber=%(itemNumber)s ; "
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    

    def test_time(self):
        from datetime import datetime
        data = dict()
        # data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(data['time'])
        instruction= "INSERT INTO hello VALUES( %(time)s )"
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def __check_book_from_stock(self, cartList):
        data = dict()

        instruction = "SELECT amountOfStcok FROM book WHERE itemNumber=%(itemNumber)s"
        print (instruction)
        amountOfStocks = []
        for acart in cartList:
            data['itemNumber']= acart[0]
            takeAmount = acart[2]
            self.cursor.execute(instruction, data)

            for amountOfStock in self.cursor:
                # run out of stock
                if amountOfStock < takeAmount:
                    return None
                else:
                    amountOfStocks.append(amountOfStock)
        return amountOfStocks

    def __take_book_from_stock(self, itemNumber, remainAmount):
        data = dict()
        data['itemNumber'] = itemNumber
        data['remainAmount'] = remainAmount
        instruction = "UPDATE book SET amountOfStock=%(remainAmount)s WHERE itemNumber=%(itemNumber)s"
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def __commit_shopping_cart(self, memberID, payway, totalPrice):
        from datetime import datetime
        orderID = self.get_shopping_cart_ID(memberID)
        print(orderID)
        data = dict()
        data['orderID'] = orderID
        data['payway'] = payway
        data['totalPrice'] = totalPrice
        data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        instruction= ("UPDATE orderList SET  "
                      " deliveryStatus=1, time=%(time)s, payway=%(payway)s , totalPrice=%(totalPrice)s "
                      " WHERE orderID=%(orderID)s " )
        print (instruction)
        self.cursor.execute(instruction, data)
        self.cnx.commit()

    def buy_shopping_cart(self, memberID, payway):
        items = self.get_shopping_cart(memberID)
        totalPrice = 0
        for acart in items:
            # run out of stock
            if acart[2] > acart[5]:
                return False
            # still has stock
            else:
                totalPrice += (acart[2] * acart[4])

        for acart in items:
            self.__take_book_from_stock(acart[0], acart[5] - acart[2])

        self.__commit_shopping_cart(memberID, payway, totalPrice)

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
        instruction =( "SELECT dispatch.itemNumber, book.title, dispatch.amountOfItem, book.listPrice, book.salePrice, book.amountOfStock "
                       "FROM dispatch, book "
                       "WHERE orderID=%(orderID)s AND dispatch.itemNumber=book.itemNumber ;")
        print(instruction)
        self.cursor.execute(instruction, data)

        result = []
        for i in self.cursor:
            result.append(i)
        return result

    def get_all_orderList(self, memberID):
        data = dict()
        data['memberID'] = memberID
        data['shopping_cart_status'] = 0
        instruction =( "SELECT * FROM orderList WHERE memberID=%(memberID)s AND deliveryStatus!=%(shopping_cart_status)s;")
        print(instruction)
        self.cursor.execute(instruction, data)

        result = []
        for i in self.cursor:
            print(i)
            result.append(i)
        return result

    def get_orderList(self, orderID):
        data = dict()
        data['orderID'] = orderID
        instruction =( "SELECT dispatch.itemNumber, book.title, dispatch.amountOfItem, book.listPrice, book.salePrice, book.amountOfStock "
                       "FROM dispatch, book "
                       "WHERE orderID=%(orderID)s AND dispatch.itemNumber=book.itemNumber ;")
        print(instruction)
        self.cursor.execute(instruction, data)

        result = []
        for i in self.cursor:
            result.append(i)
        return result

    def find_book(self, keyword):
        keyword = '%' + keyword + '%'
        data = dict()
        data['keyword'] = keyword
        instruction = "SELECT * FROM book WHERE title LIKE %(keyword)s ;"
        print (instruction)
        self.cursor.execute(instruction, data)
        result = []
        for i in self.cursor:
            result.append(i)
            print (i)
        return result
