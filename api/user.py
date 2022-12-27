from flask import *
import jwt
import time
from connectionDatabase import*


user = Blueprint("user",__name__)

@user.route("/api/user", methods=["POST"])
def signup():
	data=request.json
	email=data["email"]
	con=pool.get_connection()
	cursor=con.cursor(dictionary=True, buffered=True)	
	result={}
	try:
		cursor.execute("SELECT email FROM members WHERE email=%s;", [email])
		multipleEmail=cursor.fetchone()
		if multipleEmail != None:
			return {"error":True, "message":"email已註冊過"}
		name=data["name"]
		password=data["password"]
		insertData=(name, email, password)
		sql="INSERT INTO members(name, email, password) VALUES(%s, %s, %s);"
		cursor.execute(sql,insertData)
		con.commit()
		result["ok"]=True
	except Exception as e:
		result["error"]=True
		result["message"]=e.__class__.__name__+str(e)
	finally:
		cursor.close()
		con.close()
	return result

@user.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def auth():
	if request.method =="GET":
		result={}
		cookie=request.cookies
		try:
			if cookie :
				token=cookie["token"]
				data=jwt.decode(token,jwtkey,algorithms='HS256')
				result["data"]=data
				return result
			return {"data":None}
		except Exception as e:
			return {"data":None}

	if request.method =="PUT":
		result={}
		data=request.json
		inputdata=(data["email"], data["password"])
		con=pool.get_connection()
		cursor=con.cursor(dictionary=True, buffered=True)	
		sql="SELECT id, name, email FROM members WHERE email=%s AND password=%s;"
		try:
			cursor.execute(sql,inputdata)
			memberData=cursor.fetchone()
			if memberData==None:
				result["error"]=True
				return result
			payload={
				"id": memberData["id"],
				"name": memberData["name"],
				"email": memberData["email"],
			}
			token=jwt.encode(payload,jwtkey,algorithm ='HS256')
			result["ok"]=True
			result=make_response(result)
			result.set_cookie(key="token", value=token, expires=time.time()+60*60*24*7)
		except Exception as e:
			result["error"]=True
			result["message"]=e.__class__.__name__+str(e)
		finally:
			cursor.close()
			con.close()
		return result

	if request.method =="DELETE":
		result={}
		result["ok"]=True
		res=make_response(result)
		res.set_cookie(key="token", value="", expires=0)
		return res