import pymongo
import json

import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["company_details"]

mycol = mydb["company"]

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
    print("The database exists.")

df = pd.read_csv(r'C:\Users\Shrutika\Downloads\djangoProject\equity\static\excels\bse_ticker.csv')
dictt = {}
for index, row in df.iterrows():
    dictt[str(row['name'].split("EOD")[0].replace('-$', '').replace('.', '').strip().upper())] = str(row['code'])

file = (open(r"edge.txt", 'r').read().split('\n'))
file.pop(-1)
print(len(file))
count = 0
for f in file:

    company = json.loads(str(f))
    # print(*company[-1], sep='\n')
    try:
        k = company[-1].copy()
        company.remove(company[-1])
        for c in k:
            if isinstance(c, dict):
                d = {k.replace('.', '')+' ticker': v for k, v in c.items()}
                # print(d)
                company.append(d)

        for c in company:

            if isinstance(c, dict):
                d = {k.replace('.', ''): v for k, v in c.items()}
                company.append(d)
                company.remove(c)

        mongo = {'company_name': company[1].upper(), 'code': dictt[company[1].upper().replace('.', '')],
                 'details': company}
        print(*company, sep='\n')
        mycol.insert_one(mongo)
        print(company[1].upper().replace('.', ''), dictt[company[1].upper().replace('.', '')])
        count += 1
    except:
        # mongo = {'company_name': company[1].upper(), 'code': dictt[company[1].upper().replace('.', '')],
        #          'details': company}
        # mycol.insert_one(mongo)
        pass
        # print(company[1].upper().replace('.', ''))
print(count)
