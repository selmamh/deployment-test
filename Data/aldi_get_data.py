
from bs4 import BeautifulSoup, NavigableString
import requests
import csv
import re
import os
from datetime import datetime

def get_name( s):
   
    r=s.split('/')
    return r[len(r)-1]
def get_unit_price( s):
    try:
        r=s[s.index("(")+1:s.index(")")]
    except:
        r=""
        pass
    return r

def del_spaces(s):
    return re.sub('\s+','',s)

csv_file = open('aldi_discounts.csv', "w", encoding="utf8") 

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['product_name', 'price', 'image_name','integration_date','supermarket'])

#for i in range(1,30):
source = requests.get('https://www.aldi.hu/hu/ajanlatok/akciok-aldi-aron/').text
soup = BeautifulSoup(source, 'lxml')


all = soup.find_all('div', class_='box')
for product in all:
    product_price_info = product.find_all('span',class_='box--value')
    if (len(product_price_info) !=0):
       product_price=product_price_info[0].text
    else:
        product_price=None
   

    product_name = product.find('div',class_='box--description--header')
    if (product_name is not None):
       product_name=product_name.text.strip()
#     product_unit = product.find('div',class_='product__currency')
#     if (product_unit is not None):
#         product_unit=re.sub('\s+','',product_unit.text)
#         #print(product_unit)
#     product_unit_price = product.find('div',class_='product__secondary-text')
#     if (product_unit_price is not None):
#         product_unit_price=get_unit_price(re.sub('\s+','',product_unit_price.text))
#         #print(product_unit_price)
       product_img_name = product.find('img')
       product_img_name = del_spaces(get_name(product_img_name['src']))
       

#     if (product_img_name is not None):
#         product_img_name=get_name(product_img_name.img['src'])
#     elif (product_img_name_alt is not None):
#         product_img_name = get_name(product_img_name_alt.img['src'])
    
       integration_date=datetime.now()
       if (not product_name or not product_price):
          continue
       csv_writer.writerow([product_name, product_price,product_img_name,integration_date,"aldi"])


csv_file.close()
os.system("python get_imgs.py aldi")



