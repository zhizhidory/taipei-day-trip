import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",           
    database="taipei_trip",         
    user="root",                
    password="5244"  
)
cursor = db.cursor()

with open("taipei-attractions.json", encoding="utf-8")as file:
    json=json.load(file)
alldata=json["result"]["results"]
sql="INSERT INTO attractions(att_id, name, category, description, address, transport, mrt, lat, lng) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
imagesql="INSERT INTO images(att_id, url ) VALUES(%s, %s);"
for n in range(0, len(alldata)):
    onedata=json["result"]["results"][n]
    dbdata=(onedata["_id"], onedata["name"], onedata["CAT"], onedata["description"], onedata["address"], onedata["direction"], onedata["MRT"], onedata["latitude"], onedata["longitude"])
    cursor.execute(sql, dbdata)
    db.commit()
    imagedata=onedata["file"]
    imagedata=imagedata.replace("https", ",https")
    urls=imagedata.split(",")
    for n in urls:
        if n.endswith("jpg") or n.endswith("JPG"):
            url=(onedata["_id"], n)
            cursor.execute(imagesql, url)
            db.commit()
db.close()