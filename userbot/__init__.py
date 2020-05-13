import json

from logging import getLogger, basicConfig, INFO
from telethon import TelegramClient
from telethon.sessions import StringSession

with open('config.json') as config:
    data = json.load(config)
    API_ID = data['api_id']
    API_HASH = data['api_hash']
    STRING_SESSION = data['string_session']
    ADMIN = data['admin']

LOGS = getLogger(__name__)

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=INFO)
