from telegram import Bot
from config import BOT_TOKEN, CHAT_ID
import asyncio
import requests

bot = Bot(token=BOT_TOKEN)

async def enviar_si_nueva(db, oferta):
    col = db["productos"]
    existente = col.find_one({"nombre": oferta["nombre"]})

    if not existente:
        col.insert_one(oferta)
        await enviar_telegram(oferta)
    elif existente["precio"] > oferta["precio"]:
        col.update_one({"_id": existente["_id"]}, {"$set": {"precio": oferta["precio"]}})
        await enviar_telegram(oferta, bajada=True)

async def enviar_telegram(oferta, bajada=False):
    mensaje = f"📺 {oferta['nombre']}\n💲 ${oferta['precio']:,}\n🏬 {oferta['tienda']}\n🔗 {oferta['url']}"
    if bajada:
        mensaje = "🔻 BAJÓ DE PRECIO 🔻\n" + mensaje

    if "imagen" in oferta and oferta["imagen"]:
        # Usa HTTP API para enviar foto
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {"chat_id": CHAT_ID, "caption": mensaje, "photo": oferta["imagen"]}
        requests.post(url, data=data)
    else:
        # Envía texto plano si no hay imagen
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
