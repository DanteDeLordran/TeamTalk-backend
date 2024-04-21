from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")

conn = MongoClient(host=db_host, port=db_port)
db = conn.get_database(db_name)