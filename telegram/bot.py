import requests
from config import BOT_TOKEN, CHAT_ID

def enviar_si_nueva(db, oferta):
    col = db["productos"]
    existente = col.find_one({"nombre": oferta["nombre"]})
    if not existente:
        col.insert_one(oferta)
        enviar_telegram(oferta)
    elif existente["precio"] > oferta["precio"]:
        col.update_one({"_id": existente["_id"]}, {"$set": {"precio": oferta["precio"]}})
        enviar_telegram(oferta, bajada=True)

def enviar_telegram(oferta, bajada=False):
    mensaje = f"📺 {oferta['nombre']}\n💲 ${oferta['precio']:,}\n🏬 {oferta['tienda']}\n🔗 {oferta['url']}"
    if bajada:
        mensaje = "🔻 BAJÓ DE PRECIO 🔻\n" + mensaje
    if "imagen" in oferta and oferta["imagen"]:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {"chat_id": CHAT_ID, "caption": mensaje, "photo": oferta["imagen"]}
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": mensaje}
    requests.post(url, data=data)
