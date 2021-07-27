import pandas as pd
import mysql.connector
import re

df = pd.read_csv(r"C:\Users\kshit\Desktop\XNSE_tickers.csv")
# file1 = open(r"C:\Users\kshit\Desktop\logos1.txt","w")
u = 0
mydb = mysql.connector.connect(
    user="root",
    host="localhost",
    password="4618", database="equity_management"
)
if mydb:
    print("connection sucess")
else:
    print("nope")

mycursor = mydb.cursor()

mycursor.execute("SELECT company_name FROM equity_company ORDER BY Market_capitalization_in_lakhs DESC")
myresult = mycursor.fetchall()
clist = []
for x in myresult:
    if x[0] != '31,':
        clist.append(x[0])
print(df['issuer_name'].to_numpy())
print(df['ticker'].to_numpy())
for x in clist:
    x = x.replace('Limited', 'LTD')
    if "Finance Holdings" in x:
        print(x)
