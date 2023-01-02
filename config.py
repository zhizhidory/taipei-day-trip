import mysql.connector.pooling
import os
from dotenv import load_dotenv
load_dotenv()

jwtkey=os.getenv("key")

partnerkey=os.getenv("partnerkey")

dbconfig={
	"host":os.getenv("host"),
	"user":os.getenv("user"),
	"password":os.getenv("password"),
	"database":os.getenv("database")
}
pool=mysql.connector.pooling.MySQLConnectionPool(
	pool_name="taipeipool",
	pool_size=5,
	**dbconfig
)