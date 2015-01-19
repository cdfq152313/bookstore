import mysql.connector
from mysql.connector import errorcode
import csv

dataPath = 'data/'
orderData = dataPath + 'order.csv'
bookData = dataPath + 'item.csv'

# db config
config = {
  'user': 'root',
  'password': 'imis1000801',
  'host': '127.0.0.1',
  'database': 'bookstore',
  'raise_on_warnings': True,
}

tablesContent  = []
#prevOrder
tablesContent.append( (
       "CREATE TABLE prevOrder ("
        " number INT AUTO_INCREMENT,"
        " buyDate VARCHAR(20) ,"
        " orderNumber VARCHAR(20) NOT NULL,"
        " itemNumber VARCHAR(20) NOT NULL,"
        " itemName VARCHAR(50) NOT NULL,"
        " amount INT NOT NULL,"
        " price INT NOT NULL,"
        " PRIMARY KEY (number) "
        ") ENGINE=InnoDB ;" ) ) 
#member
tablesContent.append(  (
       "CREATE TABLE member ("
        " memberID VARCHAR(20) NOT NULL,"
        " passwd VARCHAR(20) NOT NULL,"
        " name VARCHAR(50) ,"
        " address VARCHAR(50) ,"
        " phone VARCHAR(50) ,"
        " email VARCHAR(50) ,"
        " PRIMARY KEY (memberID) "
        ") ENGINE=InnoDB ;" ) )
#oderlist
tablesContent.append(  (
       "CREATE TABLE orderList ("
        " orderID INT AUTO_INCREMENT,"
        " deliveryStatus INT,"
        " time VARCHAR(20),"
        " totalPrice INT,"
        " payway INT ,"
        " memberID VARCHAR(20) ,"
        " FOREIGN KEY (memberID) REFERENCES member(memberID) ,"
        " PRIMARY KEY (orderID) "
        ") ENGINE=InnoDB ;" ) )
#book
tablesContent.append( (
       "CREATE TABLE book ("
        " itemNumber VARCHAR(20) NOT NULL,"
        " ISBN VARCHAR(20),"
        " title VARCHAR(50) NOT NULL,"
        " author VARCHAR(20) ,"
        " publisher VARCHAR(20),"
        " publishDate VARCHAR(20),"
        " introduction VARCHAR(100),"
        " listPrice INT NOT NULL,"
        " salePrice INT NOT NULL,"
        " amountOfStock INT NOT NULL,"
        " PRIMARY KEY (itemNumber) "
        ") ENGINE=InnoDB ;" ) )
#dispatch
tablesContent.append(  (
       "CREATE TABLE dispatch ("
        " orderID INT NOT NULL,"
        " itemNumber VARCHAR(20) NOT NULL,"
        " amountOfItem INT NOT NULL,"
        " salePrice INT NOT NULL,"
        " FOREIGN KEY (orderID) REFERENCES orderList(orderID),"
        " FOREIGN KEY (itemNumber) REFERENCES book(itemNumber),"
        " PRIMARY KEY (orderID, itemNumber) "
        ") ENGINE=InnoDB ;" ) )

def ConnectSQL(config):
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

def CreateDatabase(DB_NAME):
    dbName = config['database']
    del config['database']

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    instruction = "CREATE DATABASE  {} DEFAULT CHARACTER SET 'utf8'".format(dbName)
    print (instruction)
    cursor.execute(instruction)

    cnx.database = dbName
    return cnx

def CreateTable(cursor, tablesContent):
    for content in tablesContent:
        try:
            print(content)
            cursor.execute(content)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Table already exist.')
            else:
                print(err)
                exit(1)


def InsertOrder(cnx, cursor, infileName):
    with open(infileName, 'r', encoding='utf-8' ) as infile:
        input = csv.reader(infile)
        instruction = ("INSERT INTO  prevOrder (buyDate, orderNumber, itemNumber, itemName, amount, price) "
            "VALUES (%s, %s, %s, %s, %s, %s) ;" )
        print (instruction)
        for data in input:
            data[4] = int(data[4])
            data[5] = int(data[5])
            cursor.execute(instruction, data)
        cnx.commit()

def InsertBook(cnx, cursor, infileName):
    with open(infileName, 'r', encoding='utf-8' ) as infile:
        input = csv.reader(infile)
        instruction = ("INSERT INTO  book (itemNumber, ISBN, title, author, publisher, publishDate, introduction, listPrice, salePrice, amountOfStock)"
            "VALUES (%s, NULL, %s, NULL, NULL, NULL, NULL, %s, %s,10) ;" )
        print (instruction)
        for data in input:
            data[2] = int(data[2])
            data.append( data[2] )
            cursor.execute(instruction, data)
        cnx.commit()

if __name__ == '__main__':
    cnx = ConnectSQL(config)
    cursor = cnx.cursor()
    CreateTable(cursor, tablesContent)
    InsertOrder(cnx, cursor, orderData)
    InsertBook(cnx, cursor, bookData)
    cursor.close()
    cnx.close()
