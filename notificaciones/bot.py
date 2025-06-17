from telegram import Bot
import logging

from config import BOT_TOKEN, CHAT_ID

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
    mensaje = (
        f"📺 {oferta['nombre']}\n"
        f"💲 ${oferta['precio']:,}\n"
        f"🏬 {oferta['tienda']}\n"
        f"🔗 {oferta['url']}"
    )
    if bajada:
        mensaje = "🔻 BAJÓ DE PRECIO 🔻\n" + mensaje

    try:
        if oferta.get("imagen"):
            await bot.send_photo(chat_id=CHAT_ID, photo=oferta["imagen"], caption=mensaje)
        else:
            await bot.send_message(chat_id=CHAT_ID, text=mensaje)
    except Exception:
        logging.exception("Error enviando mensaje a Telegram")
