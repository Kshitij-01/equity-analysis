import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["company_details"]

mycol = mydb["company"]

myquery = {"company_name": "AARTI INDUSTRIES LTD."}

x = mycol.find(myquery)

for k, v in x[0].items():
    if isinstance(v, list):
        for l in v:
            print(l)
    else:
        print(k, v)
