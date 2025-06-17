from pymongo import MongoClient
from config import MONGO_URI

def conectar_db():
    client = MongoClient(MONGO_URI)
    db = client["ofertas_tv"]
    return db

def cerrar_db(db):
    db.client.close()
