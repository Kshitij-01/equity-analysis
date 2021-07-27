import json
import mysql.connector

mydb = mysql.connector.connect(
    user="root",
    host="localhost",
    password="4618", database="equity_management"
)
mycursor = mydb.cursor()
sym = "BAJAJ_AUTO"
mycursor.execute("SELECT * FROM equity_balance_sheet_ticker where symbol = '{}'".format(sym))
rows = mycursor.fetchall()
mycursor.execute("SHOW columns FROM  equity_income_ticker;")
rows1 = mycursor.fetchall()


mydict = {}
for x in rows:
    mydict[x[2]] = x[3:]

rname = list(x[0] for x in rows1)[3:]
years = list(p for p, v in mydict.items())
rows = list(v for p, v in mydict.items())
thedict = {}
for r in range(len(rname)):
    for a, s in mydict.items():
        if not rname[r] in thedict:
            thedict[rname[r]] = [s[r]]
            # print("jo")
        else:
            thedict[rname[r]].append(s[r])
        #     print('c')
        # print(thedict)
username = "merken"
password = "iamawesome"
sql = "INSERT INTO {} (symbol,{}) VALUES (%s{})"
sql_company = "INSERT INTO company (symbol,company_name,logo,description,description_wiki) VALUES (%s,%s,%s,%s,%s)"
vals_company = []
ace = ',%s'
file = (open(r"C:\Users\Shrutika\Downloads\djangoProject\sidebuiness\edge.txt", 'r').read().split('\n'))
file.pop(-1)
print(len(file))
file = [file[3]]
# vals = []
# for f in file:
#     jj = json.loads(str(f))
#     vals.append(jj[0])
#     # for j in jj:
#     #     print(j)
#     for j in jj[-1]:
#         vals = [jj[0]]
#         if isinstance(j, dict):
#             X, Y, count = [], [], 0
#             e = '_ticker'
#             for x, y in j.items():
#                 print(x, y)
