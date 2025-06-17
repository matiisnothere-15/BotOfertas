from pymongo import MongoClient

from config import MONGO_URI

def conectar_db():
    if not MONGO_URI:
        raise ValueError("MONGO_URI no configurado")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client["ofertas_tv"]

def cerrar_db(db):
    db.client.close()
