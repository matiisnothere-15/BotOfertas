import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from scraper.falabella import obtener_falabella
from scraper.paris import obtener_paris
from scraper.ripley import obtener_ripley
from utils.filtros import filtrar
from telegram.bot import enviar_si_nueva
from database.db import conectar_db, cerrar_db
from pytz import timezone

logging.basicConfig(filename='logs/bot.log', level=logging.INFO)

def ejecutar():
    logging.info("Buscando ofertas...")
    productos = obtener_falabella() + obtener_paris() + obtener_ripley()
    ofertas = filtrar(productos)
    db = conectar_db()
    for oferta in ofertas:
        enviar_si_nueva(db, oferta)
    cerrar_db(db)

scheduler = BlockingScheduler(timezone=timezone("America/Santiago"))
scheduler.add_job(ejecutar, 'interval', minutes=1)
scheduler.start()
