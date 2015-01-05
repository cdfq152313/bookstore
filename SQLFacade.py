import mysql.connector
from mysql.connector import errorcode

class SQLFacade():
    __single = None
    config = {
      'user': 'bookmanager',
      'password': '0000',
      'host': '127.0.0.1',
      'database': 'bookstore',
      'raise_on_warnings': True,
    }

    def __init__(self):
        if SQLFacade.__single:
            raise Singleton.__single
        SQLFacade.__single = self

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

    @classmethod
    def get_singleton(Class):
        if not SQLFacade.__single:
            SQLFacade.__single = SQLFacade()
        return SQLFacade.__single

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
        
    def create_order(self, data):
        instruction =( "INSERT INTO orderList (orderID, memberID, deliveryStatus, time, totalPrice, payway)"
            "VALUES (%(orderID)s, %(memberID)s, %(deliveryStatus)s, %(time)s, %(totalPrice)s, %(payway)s) ;")
        print (instruction)
        self.cursor.execute()