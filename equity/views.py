import datetime

import bcrypt
import mysql.connector
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import quandl
import pandas as pd
import json
from .models import User
from .forms import userform, loginform
import pymongo
from more_itertools import sliced
import locale

locale.setlocale(locale.LC_ALL, locale.getlocale())

usernamee = 'Merken'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mymg = myclient["company_details"]

mycol = mymg["company"]

API = 'miDVwhVxgsPKPrDt-jyh'
quandl.ApiConfig.api_key = API
fd = pd.read_csv("equity/static/excels/^NSEI.csv")
df = quandl.get("BSE/SENSEX")  # pd.read_csv('equity/static/excels/^BSESN.csv')

x = fd['Date'].values.tolist()

y = fd['Close'].values.tolist()
xs, ys = df.index.to_numpy(), df['Close'].values.tolist()
mydb = mysql.connector.connect(
    user="root",
    host="localhost",
    password="4618", database="equity_management"
)
mycursor = mydb.cursor(buffered=True)
# print(xs)
f = []
for d in x:
    d = str(d)
    d = d.split("T")[0]
    t = list(map(int, d.split("-")))
    f.append([t[0], t[1], t[2]])
f = json.dumps(f)
ff = []
for d in xs:
    d = str(d)
    d = d.split("T")[0]
    t = list(map(int, d.split("-")))
    ff.append([t[0], t[1], t[2]])
print("first")
ff = json.dumps(ff)
dic = {'x': f, 'y': y, 'xs': ff, 'ys': ys}
start = pd.to_datetime(datetime.datetime.today() - datetime.timedelta(days=2000))
end = pd.to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))
mycursor.execute("SELECT company_name FROM equity_company ")
myresult = mycursor.fetchall()
c = list(my[0] for my in myresult)
c = json.dumps(c)

x = mycol.find({}, {'company_name': 1, '_id': 0})
comps2 = list(l['company_name'] for l in x)
print(comps2)


def explorer(request):
    return render(request, 'equity explorer.html', {'x': f, 'y': y, 'xs': ff, 'ys': ys, 'comps': comps2})


def loginhandel(request):
    if request.method == "POST":
        username = request.POST['Username']
        mycursor.execute("SELECT password FROM equity_user where username ='" + str(username) + "'")
        myresult = mycursor.fetchone()
        if myresult is None:
            return render(request, 'Equity home.html',
                          {"login": "true", "signup": "false", "loginerr": "invalid username or password"})
        flag = False
        password = request.POST['password']
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(myresult[0], 'utf-8')):
            user = loginform(request.POST.copy())
            flag = True
            print("It Matches!")
            return redirect('explorer')
        else:
            print("It Does not Match :(")
            messages.info(request, 'username or password not correct')
            return render(request, 'Equity home.html',
                          {"login": "true", "signup": "false", "loginerr": "ERROR: invalid username or password"})
    else:
        return render(request, 'Equity home.html',
                      {"login": "true", "signup": "false"})


def signup(request):
    if request.method == "POST":
        usernamee = request.POST["Username"]
        form = userform(request.POST or None)
        formcopy = userform(request.POST.copy())
        print(request.POST['password'])
        if form.is_valid():
            print(form.cleaned_data.get('password'))
            formcopy.data['password'] = bcrypt.hashpw(bytes(request.POST['password'], 'utf-8'),
                                                      bcrypt.gensalt(14))
            user = formcopy.save()
            # login(request, user)
            return redirect('explorer')
        else:
            messages.error(request, "incorrect username or password")
            return render(request, 'Equity home.html',
                          {"signup": "true", "login": "false",
                           "sigunuperr": "The username " + request.POST["Username"] + " is already taken"})

    else:
        return render(request, 'Equity home.html',
                      {"signup": "true", "login": "false",
                       "sigunuperr": "The username " + request.POST["Username"] + " is already taken"})


def about(request):
    return render(request, 'ABOUT.html', {'comps': comps2})


def search(request):
    if request.method == "POST":

        print(request.POST)
        cname = request.POST["tags"]
        myquery = {"company_name": cname}
        z = mycol.find(myquery)[0]
        zz = z
        # for k, v in zz.items():
        #     if isinstance(v, list):
        #         for l in v:
        #             print(l)
        #     else:
        #         print(k, v)
        # print(zz['details'][2][' Sector '][0])
        try:
            try:
                overview = {'sector': zz['details'][2][' Sector '][0], 'industry': zz['details'][2][' Industry '][0],
                            'website': zz['details'][9][' Website ']}
            except:
                overview = {'sector': zz['details'][2][' Sector '][0], 'industry': zz['details'][2][' Industry '][0]}
                pass
        except:
            overview = {}
        indi = z['details'][9]
        try:
            fi = {'Market Cap': indi[' Market Cap '][0],
                  ' Earnings per share (EPS) ': indi[' Earnings per share (EPS) '][0],
                  'Price-Earning Ratio (PE)': indi[' Price-Earning Ratio (PE) '][0]}
        except:
            fi = {}
        try:
            fi1 = {'Industry PE': indi[' Industry PE '][0], 'Book Value / Share': indi[' Book Value / Share '][0],
                   'Price to Book Value': indi[' Price to Book Value '][0]}
        except:
            fi1 = {}
        try:
            fi2 = {'Dividend Yield': ' '.join(indi[' Dividend Yield ']),
                   'No of Shares Subscribed': ' with '.join(indi[' No of Shares Subscribed ']),
                   'FaceValue': indi[' FaceValue '][0]}
        except:
            fi2 = {}
        print(overview)

        # for k, v in zz[0].items():
        #     if isinstance(v, list):
        #         for l in v:
        #             print(l)
        #     else:
        #         print(k, v)
        mycursor.execute("SELECT * FROM equity_company where company_name = '{}'".format(cname))
        ticker = mycursor.fetchone()
        sym = ticker[0]
        logo = ticker[2]
        description = json.dumps(ticker[3])
        mycursor.execute("SELECT * FROM equity_balance_sheet_ticker where symbol = '{}'".format(sym))
        rows = mycursor.fetchall()
        mycursor.execute(
            "SELECT financial_year,total_revenue,net_income FROM equity_income_ticker where symbol = '{}'".format(sym))
        incomee = mycursor.fetchall()
        dat, rev, income = [], [], []
        for q in incomee:
            income.append(float(q[2].replace(',', '')))
            dat.append(q[0])
            rev.append(float(q[1]))

        # print(*incomee, sep='\n')
        mydict = {}
        for x in rows:
            mydict[x[2]] = x[3:]
        mycursor.execute("SHOW columns FROM  equity_balance_sheet_ticker;")
        rows1 = mycursor.fetchall()
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
        print(thedict)
        # print(rows)

        #    print(ticker, cname)

        try:
            df = quandl.get('BSE/{}'.format(zz['code']), start_date=start, end_date=end)
            open = json.dumps(df['Open'].values.tolist())
            close = json.dumps(df['Close'].values.tolist())
            high = json.dumps(df['High'].values.tolist())
            low = json.dumps(df['Low'].values.tolist())
            market_cap = json.dumps(df['Total Turnover'].map(lambda p: p / 10000000).values.tolist())
            print(open, high, low, close, list(str(t).split(' ')[0] for t in df.index.tolist()), sep="\n")
            date = list(str(t).split(' ')[0] for t in df.index.tolist())
            return render(request, 'SEARCH.html',
                          {"comps": comps2, "open": open, "close": close, "high": high, "low": low, "date": date,
                           'name': cname,
                           'logo': logo, 'desc': description, 'rows': rows, "rname": rname, "mydict": mydict,
                           "years": years, "thedict": thedict, "income": json.dumps(income), "dat": json.dumps(dat),
                           "rev": json.dumps(rev), 'overview': overview, 'fi': fi, 'fi1': fi1, 'fi2': fi2,
                           'market_cap': market_cap})
        except:
            return render(request, 'SEARCH.html', {"comps": comps2, 'name': cname,
                                                   'logo': logo, 'desc': description, 'rows': rows, "rname": rname,
                                                   "mydict": mydict, "years": years, "thedict": thedict,
                                                   "income": json.dumps(income), "dat": json.dumps(dat),
                                                   "rev": json.dumps(rev), 'overview': overview, 'fi': fi, 'fi1': fi1,
                                                   'fi2': fi2})

    return render(request, 'SEARCH.html', {"comps": comps2})


# noinspection PyDeprecation
def portfolio(request):
    start = pd.to_datetime(datetime.datetime.today() - datetime.timedelta(days=1))
    profit = 0
    networth = 0
    amount = 0
    if request.method == "POST":
        mycoll = mymg["customer"]
        myquery = {"username": usernamee}
        try:
            ust = mycoll.find(myquery)[0]
            trans = ['date', 'quantity', 'price']
            for io in range(1, 4):
                flag = False

                for t in ust['investments']:
                    if t['company'] == request.POST['sn' + str(io)]:
                        print('this exe')
                        t['transactions'].append(
                            {
                                trans[0]: request.POST['dop' + str(io)],
                                trans[1]: int(request.POST['q' + str(io)]),
                                trans[2]: int(request.POST['p' + str(io)])
                            })
                        flag = True
                        break
                if not flag:
                    print('line2')
                    tt = {'company': request.POST['sn' + str(io)], 'transactions': [
                        {
                            trans[0]: request.POST['dop' + str(io)],
                            trans[1]: int(request.POST['q' + str(io)]),
                            trans[2]: int(request.POST['p' + str(io)])
                        }
                    ]}

                    ust['investments'].append(tt.copy())
                # print(ust)
            for x in ust['investments']:
                print(x['company'])
                tquantity = 0
                scale = 0
                avgprice = 0
                for t in x['transactions']:
                    tquantity += t['quantity']
                    scale += t['quantity'] * t['price']
                x['avgprice'] = scale / tquantity
                x['tquantity'] = tquantity

            print(ust)
            myquery = {"username": usernamee}
            newvalues = {"$set": ust}

            mycoll.update_one(myquery, newvalues)

            for u in ust['investments']:
                mq = {"company_name": u['company']}
                z = mycol.find(mq)[0]['code']
                amount += u['tquantity'] * u['avgprice']
                c = quandl.get('BSE/{}'.format(z), start_date=start, end_date=end)['Close'][-1]
                networth += u['tquantity'] * c
            stat1 = [networth, amount, networth - amount]
            stat = []
            for s in stat1:
                stat.append(locale.format_string("%d", s, grouping=True))
            return render(request, 'PORTFOLIO.html', {'comps': comps2, 'n': stat[0], 'a': stat[1], 'p': stat[2]})


        except:
            model = {'company': request.POST['sn1'], 'transactions': []}
            ust = {'username': usernamee, 'investments': [model.copy()]}

            ops = ['q', 'p', 'dop']
            trans = ['date', 'quantity', 'price']
            for io in range(1, 4):
                flag = False

                for t in ust['investments']:
                    if t['company'] == request.POST['sn' + str(io)]:
                        print('this exe')
                        t['transactions'].append(
                            {
                                trans[0]: request.POST['dop' + str(io)],
                                trans[1]: int(request.POST['q' + str(io)]),
                                trans[2]: int(request.POST['p' + str(io)])
                            })
                        flag = True
                        break
                if not flag:
                    print('line2')
                    tt = {'company': request.POST['sn' + str(io)], 'transactions': [
                        {
                            trans[0]: request.POST['dop' + str(io)],
                            trans[1]: int(request.POST['q' + str(io)]),
                            trans[2]: int(request.POST['p' + str(io)])
                        }
                    ]}

                    ust['investments'].append(tt.copy())
                # print(ust)
            for x in ust['investments']:
                print(x['company'])
                tquantity = 0
                scale = 0
                avgprice = 0
                for t in x['transactions']:
                    tquantity += t['quantity']
                    scale += t['quantity'] * t['price']
                x['avgprice'] = scale / tquantity
                x['tquantity'] = tquantity
            print(ust)
            mycoll.insert_one(ust)

            for u in ust['investments']:
                mq = {"company_name": u['company']}
                z = mycol.find(mq)[0]['code']
                amount += u['tquantity'] * u['avgprice']
                c = quandl.get('BSE/{}'.format(z), start_date=start, end_date=end)['Close'][-1]
                networth += u['tquantity'] * c
            stat1 = [networth, amount, networth - amount]
            stat = []
            for s in stat1:
                stat.append(locale.format_string("%d", s, grouping=True))

            return render(request, 'PORTFOLIO.html', {'comps': comps2, 'n': stat[0], 'a': stat[1], 'p': stat[2]})

    else:
        try:
            mycoll = mymg["customer"]
            myquery = {"username": usernamee}
            ust = mycoll.find(myquery)[0]
            for u in ust['investments']:
                mq = {"company_name": u['company']}
                z = mycol.find(mq)[0]['code']
                amount += u['tquantity'] * u['avgprice']
                c = quandl.get('BSE/{}'.format(z), start_date=start, end_date=end)['Close'][-1]
                networth += u['tquantity'] * c
            stat1 = [networth, amount, networth - amount]
            stat = []
            print(stat1)
            for s in stat1:
                stat.append(locale.format_string("%d", s, grouping=True))
        except:
            stat = [0, 0, 0]

        return render(request, 'PORTFOLIO.html', {'comps': comps2, 'n': stat[0], 'a': stat[1], 'p': stat[2]})
