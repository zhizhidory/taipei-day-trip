from flask import *
from flask_cors import CORS
import mysql.connector.pooling
import jwt
import time

app=Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

dbconfig={
	"host":"localhost",
	"user":"root",
	"password":"5244",
	"database":"taipei_trip"
}
pool=mysql.connector.pooling.MySQLConnectionPool(
	pool_name="taipeipool",
	pool_size=3,
	**dbconfig
)

@app.route("/api/attraction/<id>", methods=["GET"])
def attractionID_api(id):
	con=pool.get_connection()
	cursor=con.cursor(dictionary=True, buffered=True)	
	attSql="SELECT att_id AS id, name, category, description, address, transport, mrt, lat, lng FROM attractions WHERE att_id=%s"
	imageSql="SELECT url FROM images WHERE att_id=%s"
	result=None
	try:
		id=int(id)
		cursor.execute(attSql, [id])
		result=cursor.fetchone()
		if result:
			cursor=con.cursor()
			cursor.execute(imageSql, [id])
			image=cursor.fetchall()
			image=list(list(items) for items in list(image))
			image=sum(image, [])
			result["image"]=image
		data={
			"data": result
		}
	except ValueError:
		data={
			"error":True,
			"message":"景點編號錯誤"
		}
	except Exception as e:
		data={
			"error":True,
			"message":e.__class__.__name__+str(e)
		}
	finally:
		cursor.close()
		con.close()
	return data

@app.route("/api/attractions", methods=["GET"])
def attractions_api():
	con=pool.get_connection()
	cursor=con.cursor(dictionary=True)
	sql="SELECT att_id AS id, name, category, address, mrt, description, transport, lat, lng FROM attractions limit %s,12;"
	keywordSql="SELECT att_id AS id, name, category, address, mrt, description, transport, lat, lng FROM attractions WHERE (case WHEN category<>%s THEN name LIKE%s ELSE category=%s END) limit %s,12;"
	imgSql="SELECT images.url FROM images INNER JOIN attractions ON images.att_id=attractions.att_id WHERE images.att_id=%s;"
	try:
		pageNumber=int(request.args.get("page",""))
		insert=(pageNumber*12,)
		keyword=request.args.get("keyword","")
		if keyword :
			sql=keywordSql
			insert=(keyword, "%{}%".format(keyword), keyword, pageNumber*12)
		cursor.execute(sql, insert)
		result=cursor.fetchall()
		for n in range(0, len(result)):
			id=result[n]["id"]
			cursor=con.cursor()
			cursor.execute(imgSql, [id])
			images=cursor.fetchall()
			images=list(list(items) for items in list(images))
			images=sum(images, [])
			result[n]["image"]=images
		pageNumber+=1
		if len(result)<12:
			pageNumber=None
		data={
			"nextPage":pageNumber,
			"data": result,
		}
	except (ValueError, mysql.connector.ProgrammingError):
		data={
			"error":True,
			"message": "輸入格式錯誤"
		}
	except Exception as e:
		data={
			"error":True,
			"message":e.__class__.__name__+":"+str(e)
		}
	finally:
		cursor.close()
		con.close()
	return data

@app.route("/api/categories", methods=["GET"])
def categories_api():
	con=pool.get_connection()
	cursor=con.cursor()
	sql="SELECT DISTINCT category FROM attractions"
	try:
		cursor.execute(sql)
		result=cursor.fetchall()
		categoriesList=[]
		for n in result:
			categoriesList.append(n[0])
		data={
			"data": 
				categoriesList	
		}
	except Exception as e:
		data={
			"error":True,
			"message":e.__class__.__name__+str(e)
		}
	finally:
		cursor.close()
		con.close()
	return data

@app.route("/api/user", methods=["POST"])
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

@app.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def auth():
	if request.method =="GET":
		result={}
		cookie=request.cookies
		try:
			if cookie :
				token=cookie["token"]
				key="taipeiDayTripKey"
				data=jwt.decode(token,key,algorithms='HS256')
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
			key="taipeiDayTripKey"
			token=jwt.encode(payload,key,algorithm ='HS256')
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
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ =="__main__":
	app.run(port=3000, debug=True)

	