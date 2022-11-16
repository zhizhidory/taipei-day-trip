from flask import *
import mysql.connector.pooling
app=Flask(__name__)

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


app.run(port=3000)

	