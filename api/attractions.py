from flask import *
from connectionDatabase import*

attractions = Blueprint("attractions",__name__)



@attractions.route("/api/attraction/<id>", methods=["GET"])
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

@attractions.route("/api/attractions", methods=["GET"])
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

@attractions.route("/api/categories", methods=["GET"])
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