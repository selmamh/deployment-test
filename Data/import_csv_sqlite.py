import csv, sqlite3,sys,os

con = sqlite3.connect("..\db.sqlite3")


cur = con.cursor()

#cur.execute("DROP TABLE product; ")
cur.execute("CREATE TABLE product (product_name, price, supermarket, id);") 

cur.execute("DELETE FROM product;") # resets the table 
supermarkets= ['aldi','tesco']

os.system("python aldi_get_data.py ")
#os.system("python spar_get_data.py ")
os.system("python tesco_get_data.py ")


for supermarket in supermarkets:
    file_name =  supermarket+"_discounts.csv"

    with open(file_name,'r',encoding="utf8") as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['product_name'], i['price'], i['supermarket'],i['image_name']) for i in dr]

    cur.executemany("INSERT INTO product (product_name, price, supermarket,image_name) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
con.close()