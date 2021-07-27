import re
from time import sleep

import json
import pandas as pd
import wikipediaapi
from bs4 import BeautifulSoup
from selenium import webdriver

wiki_wiki = wikipediaapi.Wikipedia('en')


class data:
    def clickit(self, *paths):
        p = 0
        while True:
            for path in paths:
                try:
                    return self.driver.find_element_by_xpath(path).click()
                except Exception as e:
                    if p < 10:
                        print("not found trying again in 0.5 secs total time since start =", p, 'secs',
                              path)
                    else:
                        print(e)
                        self.driver.find_element_by_xpath(path)
                    p += 0.2
                    sleep(0.2)

    def findit(self, *paths):
        p = 0
        while True:
            for path in paths:
                try:
                    return self.driver.find_element_by_xpath(path)
                except Exception as e:
                    if p < 10:
                        print("not found trying again in 0.5 secs total time since start =", p, 'secs',
                              path)
                    else:
                        print(e)
                        self.driver.find_element_by_xpath(path)
                    p += 0.2
                    sleep(0.2)

    def __init__(self):
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page('Reliance Industries')
        # print("hello", page_py.summary[0:])

        wiki_html = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.HTML
        )

        df = pd.read_excel(r"C:\Users\Shrutika\Downloads\djangoProject\equity\static\excels\MCAP31122020.xlsx")
        cn = df['Company Name'].to_numpy()
        f = open(r"C:\Users\kshit\Desktop\cdata.txt", 'a')
        options = webdriver.ChromeOptions()
        # options.add_argument(r"user-data-dir=C:\Users\kshit\AppData\Local\Google\Chrome\User Data\Default")
        options.add_argument("--start-maximized")
        download_dir = r"C:\Users\kshit\Desktop\project_company_pdfs"  # for linux/*nix, download_dir="/usr/Public"

        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                   # Disable Chrome's PDF Viewer
                   "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        self.driver = webdriver.Chrome(
            executable_path=r'C:\Users\kshit\.wdm\drivers\chromedriver\win32\86.0.4240.22\chromedriver.exe',
            options=options)
        self.driver.get("https://www.tickertape.in/")
        print('hello i hope you are having a great day')
        try:
            cname, flag = json.loads(open(r"C:\Users\kshit\Desktop\cdata.txt", 'r').read().split('\n')[-2])[0], True
        except:
            print("new file")
            cname = 'nope'
            flag = False

        for x in cn:
            if x == 'ABHISHEK': break
            f = open(r"C:\Users\kshit\Desktop\cdata.txt", 'a')
            if flag and cname == x:
                flag = False
                continue
            elif flag:
                continue
            else:
                print(x)

            mainlist = [x]
            self.driver.find_element_by_xpath("/html/body/div/div[2]/header/div/div[1]/div[2]/div/div[1]").click()
            sleep(0.8)
            self.driver.find_element_by_xpath(
                "/html/body/div/div[2]/header/div/div[1]/div[2]/div/div[1]/input").send_keys(x)
            sleep(0.5)
            self.clickit("/html/body/div/div[2]/header/div/div[1]/div[2]/div/div[2]/div/div/ul/li[1]/div/a",
                         '//*[@id="react-autowhatever-1-section-0-item-0"]/a')
            sleep(0.6)
            soup = BeautifulSoup(
                self.findit('//*[@id="app-container"]/div/div/div[2]/div[1]').get_attribute('innerHTML'),
                features="html.parser")
            if not len(soup.findAll('a')) > 5:
                print("financials does not exist")
                self.clickit('//*[@id="app-container"]/div/div/div[2]/div[1]/div[1]/a[2]')
                tb = [
                    '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div']
                tbal = [
                    '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div']

                for q in range(len(tb)):

                    soup = BeautifulSoup(
                        self.findit(tb[q], tbal[q]).get_attribute('innerHTML'),
                        features="html.parser")
                    divx = soup.findAll("div")
                    a = 'peers'
                    list = []
                    dict = {}
                    for div in divx:
                        # print(div.get_text())
                        if len(div.get_text()) < 40:
                            if (div.get_text().strip().startswith("P") or div.get_text().strip().startswith(
                                    "D")) and not div.get_text().strip().startswith("Pr "):
                                dict[a] = list
                                print(div.get_text().strip())
                                break
                            elif div.get_text().strip() != '':
                                list.append(div.get_text().strip())

                    mainlist.append(dict)
                self.driver.execute_script(
                    'window.open("https://www.google.com/search?q=' + x + "+wiki" + "&start=" + str(0) + '","_blank");')
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.findit(
                    '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/a/h3',
                    '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/h3').click()
                cpany = self.findit('/html/body/div[3]/h1').text
                self.driver.execute_script(
                    'window.close();')
                p_html = wiki_html.page(cpany)
                mainlist.append(p_html.text[:p_html.text.find('See also') - 4])
                self.driver.switch_to.window(self.driver.window_handles[0])

                f.write(json.dumps(mainlist))
                f.write('\n')
                continue

            self.driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[2]/div[1]/div[1]/a[3]").click()
            sleep(0.4)
            reports = BeautifulSoup(
                self.findit('//*[@id="app-container"]/div/div/div[2]/div[2]/div[4]').get_attribute("innerHTML"),
                features="html.parser")

            reports.find_all("div", class_='jsx-1680410907')
            reportsdict = {"financial_reports": True}
            for report in reports:
                for r in report.find_all("div", class_='jsx-1680410907'):
                    try:
                        reportsdict[r.find_all("span")[0].text] = re.findall(r'href=[\'"]?([^\'" >]+)', str(r))[0]
                    except:
                        continue
            mainlist.append(reportsdict)

            tbname = ['income', 'balance sheet', 'cashflow']
            tb = ['/html/body/div/div[3]/div/div/div[2]/div[2]/div[3]/div[4]/div[2]/div',
                  '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[4]/div[2]',
                  '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[3]/div[2]/div',
                  '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div']
            tbal = ['/html/body/div/div[3]/div/div/div[2]/div[2]/div[3]/div[4]/div[2]/div',
                    '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[4]/div[2]',
                    '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[4]/div[2]/div',
                    '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div']
            col = ['//*[@id="app-container"]/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/input',
                   '//*[@id="app-container"]/div/div/div[2]/div[2]/div[2]/div[1]/div[2]/input',
                   '//*[@id="app-container"]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/input',
                   '//*[@id="app-container"]/div/div/div[2]/div[1]/div[1]/a[4]'
                   ]
            dict = {}

            for q in range(3):
                print(tbname[q], q)
                self.clickit(col[q])
                soup = BeautifulSoup(
                    self.findit(tb[q], tbal[q]).get_attribute('innerHTML'),
                    features="html.parser")
                divx = soup.findAll("div")
                a = 'row headers ' + tbname[q]
                print(a)
                list = []
                dict = {}
                for div in divx:
                    if len(div.get_text()) < 50:
                        if div.get_text().strip().startswith("FY"):
                            dict[a] = list
                            list = []
                            # print(div.get_text().strip())
                            a = div.get_text().strip()
                        elif div.get_text().strip().startswith(
                                tuple(str(x) for x in range(11))) and '%' not in div.get_text().strip():
                            list.append(float(div.get_text().strip().replace(",", "")))
                        elif div.get_text().strip() != '':
                            list.append(div.get_text().strip())
                dict[a] = list
                mainlist.append(dict)

            self.clickit('//*[@id="app-container"]/div/div/div[2]/div[1]/div[1]/a[4]')
            tb = [
                '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div']
            tbal = [
                '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[2]/div/div']
            col = [
                '//*[@id="app-container"]/div/div/div[2]/div[2]/div[2]/div/div/div[1]/input'
            ]

            for q in range(len(tb)):
                self.clickit(col[q])
                soup = BeautifulSoup(
                    self.findit(tb[q], tbal[q]).get_attribute('innerHTML'),
                    features="html.parser")
                divx = soup.findAll("div")
                a = 'peers'
                list = []
                dict = {}
                for div in divx:
                    # print(div.get_text())
                    if len(div.get_text()) < 40:
                        if (div.get_text().strip().startswith("P") or div.get_text().strip().startswith(
                                "D")) and not div.get_text().strip().startswith("Pr "):
                            dict[a] = list
                            print(div.get_text().strip())
                            break
                        elif div.get_text().strip() != '':
                            list.append(div.get_text().strip())

                mainlist.append(dict)
            print("https://www.google.com/search?q=" + x.replace("&", "and") + "+wiki" + "&start=" + str(
                0) + "," + "_blank")
            self.driver.execute_script(
                'window.open("https://www.google.com/search?q=' + x.replace("&", "and") + "+wiki" + "&start=" + str(
                    0) + '","_blank");')
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.findit(
                '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/a/h3',
                '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/h3',
                '//*[@id="rso"]/div[1]/div/div/div/div/div[1]/a/h3',
                '//*[@id="rso"]/div[1]/div/div[1]/a/h3').click()
            cpany = self.findit('/html/body/div[3]/h1').text
            self.driver.execute_script(
                'window.close();')
            p_html = wiki_html.page(cpany)
            print(p_html.text)
            mainlist.append(p_html.text[:p_html.text.find('See also') - 4])
            self.driver.switch_to.window(self.driver.window_handles[0])


            f.write(json.dumps(mainlist))
            f.write('\n')
            f.close()

        sleep(10)

data()
