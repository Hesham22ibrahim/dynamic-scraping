# -*- coding: utf-8 -*-
"""
this code is practice project to scrape dyrnamic websites, in this case beerwulf.com.
"""


from requests_html import HTMLSession
import pandas as pd

s = HTMLSession()
url='https://www.beerwulf.com/en-gb/c?q=beer&type=0&routeQuery=c&page='
drinklist=[]

def requests(url):
    r=s.get(url)
    r.html.render(sleep=1)
    r.status_code
    return r.html.xpath('//*[@id="product-items-container"]',first=True )

def parse(products):
    for item in products.absolute_links:
        r=s.get(item)
        #print('{}/{}'.format(list(products.absolute_links).index(item)+1,len(products.absolute_links)))
        try:name=r.html.find('div.product-detail-info-title',first=True).text
        except: name='None'
        try:subtext=r.html.find('div.product-subtext',first=True).text
        except: subtext='None'
        try:price=r.html.find('span.price',first=True).text
        except: price='None'
        try:rating=r.html.find('span.label-stars',first=True).text
        except: rating = 'None'
        if r.html.find('div.add-to-cart-container'):
            stock='In stock'
        else: 
            stock='Out of stock'
    
        drink={'name':name,
              'subtext':subtext,
              'rating':rating,
              'price':price,
              'stock':stock}
        drinklist.append(drink)
        


def csv_output():
    df=pd.DataFrame(drinklist)
    df.to_csv('drinklist.csv',index=False)
    print('collected {} items'.format(df.shape[0]))
    print('saved to csv')





x=int(input('enter total pages number:'))

for i in range (1,x+1):
    pro=requests(url+str(i))
    parse(pro)

csv_output()
