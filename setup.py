import json

from telethon import TelegramClient
from telethon.sessions import StringSession

from userbot import LOGS

API_ID = YOUY_API_ID
API_HASH = "YOUY_API_HASH"
ADMIN = YOUR_ID

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    STRING_SESSION = client.session.save()
    data = {
        "api_id": API_ID,
        "api_hash": API_HASH,
        "string_session": STRING_SESSION,
        "admin": ADMIN,
    }
    with open('config.json', 'w+') as outfile:
        json.dump(data, outfile)
    LOGS.info("Bot configurato correttamente!")
