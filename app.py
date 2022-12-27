from flask import *
from flask_cors import CORS
from api.attractions import attractions
from api.user import user
from api.booking import booking_blueprint
from api.order import order_blueprint

app=Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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


app.register_blueprint(attractions)

app.register_blueprint(user)

app.register_blueprint(booking_blueprint)

app.register_blueprint(order_blueprint)


if __name__ =="__main__":
	app.run(port=3000, debug=True)

	