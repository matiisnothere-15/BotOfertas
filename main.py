import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from scraper.falabella import obtener_falabella
from scraper.paris import obtener_paris
from scraper.ripley import obtener_ripley
from utils.filtros import filtrar
from notificaciones.bot import enviar_si_nueva
from database.db import conectar_db, cerrar_db

logging.basicConfig(filename='logs/bot.log', level=logging.INFO)

async def ejecutar():
    logging.info("Buscando ofertas...")
    productos = obtener_falabella() + obtener_paris() + obtener_ripley()
    ofertas = filtrar(productos)
    db = conectar_db()
    for oferta in ofertas:
        await enviar_si_nueva(db, oferta)
    cerrar_db(db)

if __name__ == "__main__":
    scheduler = AsyncIOScheduler(timezone=timezone("America/Santiago"))
    scheduler.add_job(ejecutar, "interval", minutes=1)
    scheduler.start()

    # Ejecutar loop de eventos
    asyncio.get_event_loop().run_forever()
