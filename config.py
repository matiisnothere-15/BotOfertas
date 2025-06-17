import os
from dotenv import load_dotenv
load_dotenv()



BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "0"))
MONGO_URI = os.getenv("MONGO_URI")
