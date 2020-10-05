import json
import os

from logging import getLogger, basicConfig, INFO

from .functions import loadConfig, dumpConfig

from telethon import TelegramClient
from telethon.sessions import StringSession

# CREATE CONFIGS
if not os.path.exists('config.json'):

    api_id = None
    api_hash = None

    while True:
        if api_id is None:
            api_id = input('API_ID: ')

        if api_hash is None:
            api_hash = input('API_HASH: ')

        if api_hash != None and api_id != None:
            break

    # CREATING SESSION
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        string_session = client.session.save()

    dumpConfig({"telegram": {"api_id": int(api_id), "api_hash": str(api_hash), "string_session": str(string_session)}})

# LOAD CURRENT CONFIG
configs = loadConfig()

# CREATE TELEGRAM CLIENT
app = TelegramClient(
    StringSession(configs['telegram']['string_session']),
    configs['telegram']['api_id'],
    configs['telegram']['api_hash']
)

# LOGS
LOGS = getLogger(__name__)
basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=INFO
)
