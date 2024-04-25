from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = MongoClient(host=db_host, port=db_port, username=db_user, password=db_password)
db = conn.get_database(db_name)
