import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import pandas as pd

conn = sqlite3.connect('prizes')
c = conn.cursor()

c.execute('''DROP TABLE comparison''')
c.execute('''CREATE TABLE comparison (date DATE, store TEXT, title TEXT, price REAL, stock TEXT)''')


def getPriceMM(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    current_date = datetime.datetime.now()
    store = 'Media Markt'
    title = soup.find('h1').text
    price = soup.find('div', {'class': 'StyledBox-sc-1vld6r2-0 goTwsP'}).find('span', {'class': 'ScreenreaderTextSpan-sc-11hj9ix-0 kZCfsu'}).text.replace('undefined', '')
    stock = soup.find('div', {'class': 'StyledAvailabilityHeadingWrapper-sc-901vi5-2 iPyFyN'}).find('span', {'class':'BaseTypo-sc-1jga2g7-0 izkVco StyledInfoTypo-sc-1jga2g7-1 ZaejY StyledAvailabilityTypo-sc-901vi5-7 egVdxU'}).text
    c.execute('''INSERT INTO comparison VALUES(?,?,?,?,?)''', (current_date, store, title, price, stock))
    #print(current_date, store, title, price, stock)
    return

def getPriceBOL(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    current_date = datetime.datetime.now()
    store = 'Game Mania'
    title = soup.find('div', {'class':'pdp-header slot slot--pdp-header js_slot-title'}).find('span', {'class':'u-mr--xs'}).text
    price = soup.find('div', {'class': 'price-block__price'}).find('span', {'class': 'promo-price'}).text.replace('\n', ',99').strip('99,99')
    stock = soup.find('div', {'class': 'buy-block__delivery-text'}).find( 'span').text
    c.execute('''INSERT INTO comparison VALUES(?,?,?,?,?)''', (current_date, store, title, price, stock))
    #print(current_date, store, title, price, stock)
    return

def getPricePS(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    current_date = datetime.datetime.now()
    store = 'BCC'
    title = soup.find('h1').text.replace('\n',' ')
    price = soup.find('div', {'class': 'psw-l-anchor psw-l-stack-left psw-fill-x psw-p-y-4 psw-p-x-5'}).text.replace('€', '')
    stock = soup.find('div', {'class': 'psw-fade-out psw-l-line-left'}).find('span', {'class':'psw-fill-x psw-t-truncate-1 psw-l-space-x-2'}).text
    c.execute('''INSERT INTO comparison VALUES(?,?,?,?,?)''', (current_date, store, title, price, stock))
    #print(current_date, store, title, price, stock)
    return

getPriceMM('https://www.mediamarkt.nl/nl/product/_ps5-fifa-23-ps5-1734919.html')
getPriceBOL('https://www.bol.com/nl/nl/p/fifa-23-ps4/9300000116890730/?Referrer=ADVNLGOO002012-G-138517438515-S-1671973218393-9300000116890730&gclid=CjwKCAjwo_KXBhAaEiwA2RZ8hKHems2ldeJTT3_OzP3h6J7RjnEruty1hMDEZSk1Rifa1DAnrGkMxBoCNsYQAvD_BwE')
getPricePS('https://store.playstation.com/nl-nl/concept/10004336')



conn.commit()
print('complete')

#c.execute('''SELECT * FROM prizes''')
#results = c.fetchall()
#print(results)



df = pd.read_sql_query( "SELECT* FROM comparison", conn)
print(df)
conn.close()
