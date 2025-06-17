import asyncio
import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from scraper.falabella import obtener_falabella
from scraper.paris import obtener_paris
from scraper.ripley import obtener_ripley
from utils.filtros import filtrar
from notificaciones.bot import enviar_si_nueva
from database.db import conectar_db, cerrar_db
from config import MAX_PRICE

# Asegurar carpeta de logs y configurar logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),
    ],
)

async def tarea(db):
    logging.info("Buscando ofertas...")
    productos = []
    for func in (obtener_falabella, obtener_paris, obtener_ripley):
        try:
            productos.extend(func())
        except Exception:
            logging.exception("Error al obtener datos de %s", func.__name__)
    ofertas = filtrar(productos, max_precio=MAX_PRICE)
    for oferta in ofertas:
        await enviar_si_nueva(db, oferta)

async def main():
    db = conectar_db()
    scheduler = AsyncIOScheduler(timezone=timezone("America/Santiago"))
    scheduler.add_job(tarea, "interval", minutes=1, args=[db])
    scheduler.start()

    logging.info("Bot iniciado. Esperando tareas...")
    try:
        await asyncio.Event().wait()  # mantiene el programa corriendo
    finally:
        cerrar_db(db)

if __name__ == "__main__":
    asyncio.run(main())
