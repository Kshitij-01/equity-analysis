import json
import mysql.connector

mydb = mysql.connector.connect(
    user="root",
    host="localhost",
    password="4618", database="equity_management"
)
mycursor = mydb.cursor()
username = "merken"
password = "iamawesome"
sql = "INSERT INTO equity_{} (symbol,{}) VALUES (%s{})"
sql_company = "INSERT INTO equity_company (symbol,company_name,logo,description,description_wiki,financial_report) VALUES (%s,%s,%s,%s,%s,%s)"
vals_company = []
ace = ',%s'
file = (open(r"edge.txt", 'r').read().split('\n'))
file.pop(-1)
# print(len(file))
mycursor.execute('select symbol from equity_company')
cpany = mycursor.fetchall()
vals = []
print(len(cpany))
for f in file[len(cpany):]:
    vals = []
    vals_company = []

    jj = json.loads(str(f))
    vals.append(jj[0])
    comp = jj[0]

    try:
        vals_company.append(jj[0])
    except:
        vals_company.append('not found')
    try:
        vals_company.append(jj[1])
    except:
        vals_company.append('not found')
    try:
        if jj[-2].startswith('data:image'):
            vals_company.append(jj[-2])
        else:
            vals_company.append('not found')
    except:
        vals_company.append('not found')
    try:
        if jj[4].startswith('<ion-label '):
            vals_company.append(jj[4])
        else:
            vals_company.append('not found')
    except:
        vals_company.append('not found')
    try:
        if isinstance(jj[-1][-1], str):
            vals_company.append(jj[-1][-1])
        else:
            vals_company.append('not found')
    except:
        vals_company.append('not found')
    try:
        if isinstance(jj[-1][0], dict):
            vals_company.append(str(jj[-1][0]))
        else:
            vals_company.append('not found')
    except:
        vals_company.append('not found')

    # print(sql_company, vals_company, len(sql_company), len(vals_company), sep='\n')
    mycursor.execute(sql_company, vals_company)

    #   # print(*vals_company,sep='\n')
    # print(sql_company)
    for j in jj[:-3]:
        count = 0
        if isinstance(j, dict):
            X, Y = [], []
            count = 0
            e = '_stockedge'
            for x, y in j.items():
                #  # print(type(y))
                if count == 0:
                    e = y.replace('/', '').replace(' ', '_').strip().strip('_') + e
                X.append(x.strip().replace('&', 'and').replace('.', '').replace(' ', '_').replace('/',
                                                                                                  '').replace(
                    '(', '').replace(')', '').replace('-', '_').replace("'", "").replace('%', '').replace('9_',
                                                                                                          '').strip(
                    '_').replace('__', '_'))
                if isinstance(y, list):
                    Y.append(
                        " ".join(y).strip())
                elif count == len(j.items()) - 1:
                    Y.append(y.strip())
                else:
                    Y.append(y.strip().replace('/', ''))

                count += 1
            #  # print(X, Y, sep="\n")
            # print(sql.format(e, str(','.join(X)), (ace * len(Y))))

            for v in Y:
                vals.append(v)

            print(len(Y), len(vals))
            print(sql.format(e, str(','.join(X)), (ace * len(Y))))
            # print(vals)
            for i in range(len(X)):
                print(X[i], vals[i])
            try:
                mycursor.execute(sql.format(e, str(','.join(X)), (ace * len(Y))), vals)
            except:
                pass
            vals = [jj[0]]
            #  # print(Y)
            e = '_stockedge'
    sql = "INSERT INTO equity_{} ({}) VALUES (%s{})"
    for j in jj[-1]:
        vals = [jj[0]]
        if isinstance(j, dict):
            X, Y, count = [], [], 0
            e = '_ticker'
            for x, y in j.items():
                # print(x,y)
                if x.startswith('r') or x.startswith('p'):
                    e = x.replace('row headers', '').strip().replace(' ', '_') + e
                    X = ['symbol',
                         *list(p.replace('row headers ', '').strip().replace('&', 'and').replace('.', '').replace(' ',
                                                                                                                  '_').strip(
                             '_').replace('/', '').replace('(', '').replace(')', '').replace('-', '_').replace('%',
                                                                                                               '').replace(
                             "'", "").replace('9_', '').strip('_').replace('__', '_') for p in y)]

                    continue

                if not isinstance(y, bool):
                    # print(sql.format(e, str(','.join(X)), (ace * len(X))))
                    vals.append(x)
                    for v in y:
                        vals.append(v)
                    # print(len(y), len(vals), len(X))
                    # print(y)
                    # print(X)
                    # print(vals)

                    # for i in range(len(vals)):
                    # print(X[i], vals[i])
                    try:
                        mycursor.execute(sql.format(e, str(','.join(X)), (ace * (len(X) - 1))), vals)
                    except:
                        pass
                    vals = [jj[0]]

                else:
                    break

    print(
        '---------------------------------------------------------------------------------------------------------------')
    mydb.commit()
# break
