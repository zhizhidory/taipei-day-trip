from flask import *
import jwt
from connectionDatabase import*

booking_blueprint = Blueprint("booking",__name__)

@booking_blueprint.route("/api/booking", methods=["GET", "POST", "DELETE"])
def tripbooking():
    if request.method=="GET":
        token=request.cookies["token"]
        data=jwt.decode(token,jwtkey,algorithms='HS256')
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True, buffered=True)
        result={}
        try:
            cursor.execute("SELECT attractions.name, attractions.att_id, attractions.address, booking.date, booking.time, booking.price FROM attractions INNER JOIN booking ON booking.attractionId=attractions.att_id WHERE booking.memberId=%s;", [data["id"]])
            bookingData=cursor.fetchone()
            if bookingData :
                id=bookingData["att_id"]
                cursor.execute("SELECT url FROM images WHERE att_id=%s;", [bookingData["att_id"]])
                imageURL=cursor.fetchone()
                result={
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
                result={"data" : None}
        except Exception as e:
            result["error"]=True
            result["message"]=e.__class__.__name__+str(e)
        finally:
            cursor.close()
            con.close()
        return result

    if request.method=="POST":
        data=request.json
        id=data["memberId"]
        insertData=(data["attractionId"], data["date"], data["time"], data["price"] ,data["memberId"])
        result={}
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute("SELECT*From booking WHERE memberId=%s;", [data["memberId"]])
            bookingData=cursor.fetchone()
            if bookingData:
                cursor.execute("DELETE FROM booking WHERE memberId=%s;", [data["memberId"]])
                con.commit()
            sql="INSERT INTO booking(attractionId, date, time, price, memberId) VALUES(%s, %s, %s, %s, %s);"
            cursor.execute(sql,insertData)
            con.commit()
            result={"ok":True}
        except Exception as e:
            result["error"]=True
            result["message"]=e.__class__.__name__+str(e)
        finally:
            cursor.close()
            con.close()
        return result
    if request.method=="DELETE":
        id=request.json["memberId"]
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True, buffered=True)
        result={}
        try:
            cursor.execute("DELETE FROM booking WHERE memberId=%s;", [id])
            con.commit()
            result["ok"]=True
        except Exception as e:
            result["error"]=True
            result["message"]=e.__class__.__name__+str(e)
        finally:
            cursor.close()
            con.close()
        return result
