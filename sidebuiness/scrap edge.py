import base64
import json
import re

import wikipediaapi
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from time import sleep
import wikipediaapi
from bs4 import BeautifulSoup
import urllib.request
import requests


class edgescrapper:
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia('en')
        self.page_py = self.wiki_wiki.page('Reliance Industries')
        # print("hello", page_py.summary[0:])

        self.wiki_html = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.HTML
        )

        df = pd.read_csv(r"C:\Users\Shrutika\Downloads\djangoProject\equity\static\excels\XNSE_tickers.csv")
        cn = df['issuer_name'].map(lambda p: ' '.join(p.split()[:-1])).to_numpy()
        # f = open(r'C:\Users\kshit\PycharmProjects\djangoProject1\equity\static\excels\XNSE_tickers.csv')
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--user-data-dir=" + r"C:\Users\kshit\AppData\Local\Google\Chrome\User Data\Default")
        download_dir = r"C:\Users\kshit\Desktop\logos"  # for linux/*nix, download_dir="/usr/Public"

        # profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
        #            # Disable Chrome's PDF Viewer
        #            "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"}
        # options.add_experimental_option("prefs", profile)
        self.driver = webdriver.Chrome(
            executable_path=r'C:\Users\kshit\.wdm\drivers\chromedriver\win32\86.0.4240.22\chromedriver.exe',
            options=options)
        counter = 1
        self.driver.execute_script(
            'window.open("https://www.tickertape.in/")')
        self.driver.switch_to.window(self.driver.window_handles[0])
        with open(r"C:\Users\Shrutika\Downloads\djangoProject\sidebuiness\edge.txt", 'r') as f:
            try:
                load = json.loads(f.read().split('\n')[-2])
                cp = load[0]
                for x in df['ticker'].to_numpy():
                    if x == cp:
                        break
                    else:
                        print(x)
                        counter += 1
            except:
                counter -= 1
                pass
        f.close()
        print(counter)
        self.fetch(cn[counter:], df['ticker'].to_numpy()[counter:])

    def getit(self, *link, timeout=30, type='xpath'):
        for _ in range(abs(timeout - len(link) * 3)) if abs(timeout - len(link) * 3) != 0 else range(2):
            for x in link:
                try:
                    if type == 'xpath':
                        return self.driver.find_element_by_xpath(x)
                    elif type == 'class':
                        return self.driver.find_elements_by_name(x)
                except:
                    # print('sleeping')
                    sleep(0.2)
        return False

    def data_table(self, table, type, detailed_type, overview=False):
        ddict = {}
        soup = BeautifulSoup(table, 'html.parser')
        soup = soup.find_all('ion-item')
        ddict[type] = detailed_type
        for sou in soup:
            data = []
            so = sou.find_all('ion-text')
            # print(so[0].text)
            if so[0].text.strip() in ['Balance Sheet', 'Profit and Loss', 'Cash Flow']:
                print('continue')
                continue
            if overview == 'pattern':
                so.insert(0, sou.find_all('ion-col')[1])
            for s in so[1:]:
                # print(s.text.strip())
                if s.text.strip() in ['Rs. Cr.']:
                    continue
                data.append(s.text.strip())
            ddict[so[0].text] = data
        if overview == False:
            ddict[' Website '] = self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[5]/div[2]/app-fundamental-overview/se-content/ion-content/div/ion-list[1]/ion-item[3]/ion-grid/ion-row/ion-col[2]/span').text
        # print('--------------------------------------------------------------------------')
        return ddict

    def fetch(self, companies_list, tickers):

        first = [
            '//*[@id="rso"]/div[1]/div/div/div[1]/a/h3',
            '//*[@id="rso"]/div[1]/div/div/div/div[1]/a/h3',
            '//*[@id="rso"]/div[1]/div/div/div/div/div[1]/a/h3',
            '//*[@id="rso"]/div[1]/div/div/div/div/div/div[1]/a/h3',
            '//*[@id="rso"]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div[1]/a/h3',
            '//*[@id="rso"]/div[2]/div/div/div[1]/a/h3'
        ]
        for c, t in tuple(zip(companies_list, tickers)):
            local_list = [t, c]
            self.driver.get("https://www.google.com/search?q={}".format((c.replace("&", "and") + " stockedge")))
            print(self.getit(*first).text.lower())
            if 'StockEdge'.lower() not in self.getit(*first).text.lower() or 'blog' in self.getit(
                    *first).text.lower() or 'mutual fund' in self.getit(*first).text.lower():
                # print(self.getit(*first).text)
                continue
            self.getit(*first).click()
            sleep(1.3)
            try:
                self.getit(
                    '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/div/div/div[5]').click()
                table = self.getit(
                    '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[5]/div[2]/app-fundamental-overview/se-content/ion-content/div/ion-list[2]').get_attribute(
                    'innerHTML')
                local_list.append(self.data_table(table, 'Fundamental', 'Financial Indicators'))
            except:
                pass

            # print(local_list, table)
            # print('-------------------------------------------------------------------------------')
            sleep(0.2)
            try:
                table = self.getit(
                    '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[5]/div[2]/app-fundamental-overview/se-content/ion-content/div/ion-list[1]').get_attribute(
                    'innerHTML')
                local_list.append(self.data_table(table, 'Fundamental', 'Overview', overview=True))
            except:
                continue
            # print(local_list)
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[5]/div[2]/app-fundamental-overview/se-content/ion-content/div/ion-item-divider[1]/ion-grid/ion-row/ion-col[2]/ion-button').click()
            try:
                paras = self.getit(
                    '//*[@id="ion-overlay-1"]/div/app-company-profile-modal/ion-content/se-content/ion-content/div/ion-list/ion-item').get_attribute(
                    'innerHTML')
                soup = BeautifulSoup(paras, 'html.parser').prettify()
                local_list.append(soup)
            except:
                local_list.append("NO COMPANY PROFILE FOUND")

            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/div/div/div[6]').click()
            sleep(0.4)
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[6]/div[1]/div[2]').click()
            sleep(0.3)
            table = self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[6]/div[3]/app-balance-sheet/se-content/ion-content/div/ion-list').get_attribute(
                'innerHTML')
            #    print(table)
            local_list.append(self.data_table(table, 'Financials', 'Balance sheet'))
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[6]/div[1]/div[3]').click()
            sleep(0.5)
            table = self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[6]/div[4]/app-profit-and-loss/se-content/ion-content/div').get_attribute(
                'innerHTML')
            local_list.append(self.data_table(table, 'Financials', 'Profit and Loss'))

            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[6]/div[1]/div[4]').click()
            sleep(0.3)
            table = self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[6]/div[5]/app-cash-flow/se-content/ion-content/div').get_attribute(
                'innerHTML')
            local_list.append(self.data_table(table, 'Financials', 'Cash Flow'))
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/div/div/div[7]').click()
            sleep(0.1)
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/div/div/div[7]').click()
            sleep(0.2)
            table = self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[7]/div[2]/app-shareholding-pattern/se-content/ion-content/div').get_attribute(
                'innerHTML')
            local_list.append(self.data_table(table, 'Shareholding', 'Pattern', overview='pattern'))
            self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[7]/div[1]/div[3]').click()
            sleep(0.3)
            table = self.getit(
                '//*[@id="se-body"]/app-root/ion-app/ion-split-pane/ion-router-outlet/app-security-dashboard/ion-content/tab-slidebox/ion-slides/div/ion-slide[7]/div[4]/app-bod/se-content/ion-content/div').get_attribute(
                'innerHTML')
            soup = BeautifulSoup(table, 'html.parser')
            soup = soup.find_all('ion-row')
            ddict = {}
            for sou in soup:
                so = sou.find_all('ion-label')
                ddict[so[0].text] = so[1].text
            local_list.append(ddict)
            sleep(0.1)
            self.driver.get('https://www.google.com/')
            self.getit('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(
                c.replace("&", "and"))
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()

            try:
                self.getit('//*[@id="wp-tabs-container"]/div[1]/div/div[2]/div/div/a').click()
                sleep(0.2)
                img_src = self.getit(
                    '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_attribute(
                    'src')
                # print(img_src)
                encoded = base64.b64encode(requests.get(img_src).content)
                # print(encoded)
                # resource = urllib.request.urlopen(img_src)
                # encoded_string = base64.b64encode(resource.read())
                # self.driver.get('data:image/jpg;base64,{}'.format(str(encoded).replace("b'", '').replace("'", '')))
                if 'jpeg' in img_src:
                    local_list.append(
                        'data:image/jpeg;base64,{}'.format(str(encoded).replace("b'", '').replace("'", '')))
                elif 'jpg' in img_src:
                    local_list.append(
                        'data:image/jpg;base64,{}'.format(str(encoded).replace("b'", '').replace("'", '')))
                elif 'png' in img_src:
                    local_list.append(
                        'data:image/png;base64,{}'.format(str(encoded).replace("b'", '').replace("'", '')))
            except:
                pass
            f = open(r"C:\Users\kshit\Desktop\edge.txt", 'a')
            local_list.append(self.fetchtickertape(c, t, first))
            f.write(json.dumps(local_list))
            f.write('\n')
            f.close()

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

    def fetchtickertape(self, c, t, first):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.tickertape.in/")

        mainlist = []
        self.driver.find_element_by_xpath("/html/body/div/div[2]/header/div/div[1]/div[2]/div/div[1]").click()
        sleep(0.8)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/header/div/div[1]/div[2]/div/div[1]/input").send_keys(c)
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
                'window.open("https://www.google.com/search?q=' + c + "+wiki" + "&start=" + str(0) + '","_blank");')
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.findit(
                '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/a/h3',
                '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/h3').click()
            cpany = self.findit('/html/body/div[3]/h1').text
            self.driver.execute_script(
                'window.close();')
            p_html = self.wiki_html.page(cpany)
            mainlist.append(p_html.text[:p_html.text.find('See also') - 4])
            self.driver.switch_to.window(self.driver.window_handles[0])

            return mainlist

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
                self.findit(tb[q], tbal[q],
                            '//*[@id="app-container"]/div/div/div[2]/div[2]/div[3]/div[3]').get_attribute('innerHTML'),
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
        self.driver.execute_script(
            'window.open("https://www.google.com/search?q=' + c.replace("&", "and") + "+wiki" + "&start=" + str(
                0) + '","_blank");')
        self.driver.switch_to.window(self.driver.window_handles[2])
        if 'Wikipedia'.lower() in self.getit(*first).text.lower().strip():
            self.getit(*first).click()
            cpany = self.findit('/html/body/div[3]/h1').text
            self.driver.execute_script(
                'window.close();')
            p_html = self.wiki_html.page(cpany)
            mainlist.append(p_html.text[:p_html.text.find('See also') - 4])
            self.driver.switch_to.window(self.driver.window_handles[0])
            print(mainlist)
            return mainlist
        else:
            self.driver.execute_script(
                'window.close();')
            self.driver.switch_to.window(self.driver.window_handles[0])
            print(mainlist)
            return mainlist


edgescrapper()
