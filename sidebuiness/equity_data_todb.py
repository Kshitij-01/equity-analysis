f = open(r"C:\Users\kshit\Desktop\logos.txt")
import pandas as pd
import mysql.connector
import re

df = pd.read_excel(r"C:\Users\Shrutika\Downloads\djangoProject\equity\static\excels\MCAP31122020.xlsx")
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


def convert(list):
    return tuple(list)


mycursor = mydb.cursor()

sql = "INSERT INTO equity_company (symbol, company_name , Market_capitalization_in_lakhs , logo) VALUES (%s, %s,%s ,%s)"
val = []
for x in f:
    t = x.split()
    if t[0].startswith("data"):
        if x.split()[1].startswith("<Cell"):
            dfa = df[df["Company Name"] == re.sub("_", " ", t[-2])].drop(df.columns[4], axis=1)
            val.append((dfa['Symbol'].values[0], re.sub("_", " ", t[-2]), float(t[-1]), t[0]))
        elif t[-1] == "2020":
            val.append((t[1], re.sub("_", " ", t[-2]), 0.0, t[0]))
        else:
            val.append((t[1], re.sub("_", " ", t[-2]), float(t[-1]), t[0]))
mycursor.executemany(sql, val)
mydb.commit()
