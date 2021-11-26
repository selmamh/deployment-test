
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

csv_file = open('tesco_discounts.csv', "w", encoding="utf8") 

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['product_name', 'price', 'unit', 'unit_price','image_name','integration_date','supermarket'])

#for i in range(1,30):
source = requests.get('https://tesco.hu/akciok/akcios-termekek/?page=80').text
soup = BeautifulSoup(source, 'lxml')



#all = soup.find('div', class_='m-productListing__productsGrid')

all = soup.find_all('a', class_='details-box')

#print(all)

#print(all)
#tx-tesco-products
for product in all:
    product_price = product.find('div',class_='product__price')
    if (product_price is not None):
        product_price=re.sub('\s+','',product_price.text)
        #print(product_price)
    product_name = product.find('span',class_='product__name')
    if (product_name is not None):
        product_name=re.sub('\n','',product_name.text)
        #print(product_name)
    product_unit = product.find('div',class_='product__currency')
    if (product_unit is not None):
        product_unit=re.sub('\s+','',product_unit.text)
        #print(product_unit)
    product_unit_price = product.find('div',class_='product__secondary-text')
    if (product_unit_price is not None):
        product_unit_price=get_unit_price(re.sub('\s+','',product_unit_price.text))
        #print(product_unit_price)
    product_img_name = product.find('div',class_='product__img-holder')
    product_img_name_alt = product.find('div',class_='product__image-container')

    if (product_img_name is not None):
        product_img_name=get_name(product_img_name.img['src'])
    elif (product_img_name_alt is not None):
        product_img_name = get_name(product_img_name_alt.img['src'])
    
    integration_date=datetime.now()
    if (not product_name or not product_price):
        continue
    csv_writer.writerow([product_name, product_price, product_unit,product_unit_price,product_img_name,integration_date,"tesco"])


csv_file.close()
os.system("python get_imgs.py tesco")
#os.system("python import_csv_sqlite.py")


