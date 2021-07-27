import bcrypt
import mysql.connector

mydb = mysql.connector.connect(
    user="root",
    host="localhost",
    password="4618", database="equity_management"
)
mycursor = mydb.cursor()
username = "merken"
password = "iamawesome"
sql = "INSERT INTO customers "+str()+" VALUES (%s, %s)"
myresult = mycursor.fetchone()


