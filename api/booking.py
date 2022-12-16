from flask import *
from connectionDatabase import*

booking_blueprint = Blueprint("booking",__name__)

@booking_blueprint.route("/api/booking", methods=["GET", "POST", "DELETE"])
def tripbooking():
    if request.method=="GET":
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True, buffered=True)
        data={}
        try:
            cursor.execute("SELECT attractions.name, attractions.att_id, attractions.address, booking.date, booking.time, booking.price FROM attractions INNER JOIN booking ON booking.attractionId=attractions.att_id;")
            bookingData=cursor.fetchone()
            if bookingData :
                id=bookingData["att_id"]
                cursor.execute("SELECT url FROM images WHERE att_id=%s;", [bookingData["att_id"]])
                imageURL=cursor.fetchone()
                data={
                    "data" : {
                        "attraction" : {
                            "id" : bookingData["att_id"],
                            "name" : bookingData["name"],
                            "address": bookingData["address"],
                            "image": imageURL["url"]
                        },
                        "date" : bookingData["date"],
                        "time" : bookingData["time"],
                        "price" : bookingData["price"]
                    }
                }
            else : 
                data={"data" : None}
        finally:
            cursor.close()
            con.close()
        return data
    if request.method=="POST":
        data=request.json
        insertData=(data["attractionId"], data["date"], data["time"], data["price"])
        result={}
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute("TRUNCATE TABLE booking;")
            con.commit()
            sql="INSERT INTO booking(attractionId, date, time, price) VALUES(%s, %s, %s, %s);"
            cursor.execute(sql,insertData)
            con.commit()
            result={"ok":True}
        finally:
            cursor.close()
            con.close()
        return result
    if request.method=="DELETE":
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True, buffered=True)
        result={}
        try:
            cursor.execute("TRUNCATE TABLE booking")
            con.commit()
            result["ok"]=True
        finally:
            cursor.close()
            con.close()
        return result
