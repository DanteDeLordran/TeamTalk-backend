from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")

conn = MongoClient(f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
db = conn.get_database(db_name)
