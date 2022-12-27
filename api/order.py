from flask import *
from connectionDatabase import*
import time, jwt
import requests
import json

order_blueprint = Blueprint("order",__name__)

@order_blueprint.route("/api/orders", methods=["POST"])
def createorders():
    con=pool.get_connection()
    cursor=con.cursor(dictionary=True, buffered=True)	
    orderData=request.json
    token=request.cookies["token"]
    userdata=jwt.decode(token,jwtkey,algorithms='HS256')
    prime=orderData["prime"]
    order=orderData["order"]
    contact=order["contact"]
    trip=order["trip"]
    attraction=trip["attraction"]
    number=time.strftime("%Y%m%d%H%M%S", time.gmtime())
    url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    header={"Content-Type": "application/json", "x-api-key": partnerkey}
    tapPayData={
        "prime":prime,
        "partner_key": partnerkey,
        "merchant_id": "Flora0408_CTBC",
        "details":"TapPay Test",
        "amount": order["price"],
        "cardholder": {
            "phone_number": contact["phone"],
            "name": contact["name"],
            "email": contact["email"]
        }   
    }
    tapPayData=json.dumps(tapPayData)
    try:
        cursor.execute("DELETE FROM booking WHERE memberId=%s;", [userdata["id"]])
        con.commit()
        cursor.execute("SELECT COUNT(*) FROM orders;")
        rows=cursor.fetchone()
        number=number+str(rows["COUNT(*)"]+1)
        result={"data" : {"number":number, "payment":{"status" :1, "msg": "付款失敗"}}}
        sqlData=(number, order["price"], attraction["id"], attraction["name"],  attraction["address"], attraction["image"],  trip["date"], trip["time"], contact["name"], contact["email"], contact["phone"],  1)
        cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", sqlData)
        con.commit()
        response = requests.post(url, headers=header, data=tapPayData).json()
        status=response["status"]
        if status == 0:
            cursor.execute("UPDATE orders SET payment_status=0 WHERE number=%s;", [number])
            con.commit()
            result["data"]["payment"].update({"status" :0, "msg": "付款成功"})
    except Exception as e:
        result={"error" :True, "msg" : e.__class__.__name__+str(e)}
    finally:
        cursor.close()
        con.close()
    return result

@order_blueprint.route("/api/order/<number>", methods=["GET"])
def checkorders(number):
    con=pool.get_connection()
    cursor=con.cursor(buffered=True)	
    sql="SELECT *FROM orders WHERE number=%s;"
    finalData={}
    try:
        cursor.execute(sql, [number])
        data=cursor.fetchone()
        if data:
            result={"number":data[0], "price": data[1], "status":data[11]}
            result["contact"]={"name":data[8], "email": data[9], "phone": data[10]}
            result["trip"]={"attraction":{"id":data[2], "name":data[3], "address":data[4], "image":data[5]}, "date":data[6], "time":data[7]}
            finalData={"data":result}
        else:
            finalData={"data":None}
    except Exception as e:
        finalData={"error": True, "message": e.__class__.__name__+str(e)}
    finally:
        cursor.close()
        con.close()
    return finalData
    


