try:
    import sys
    import json
    import os
    import time
    import colorama
    import coloredlogs
    import logging

    from .functions import loadConfig, dumpConfig

    from telethon import TelegramClient
    from telethon.sessions import StringSession
except ImportError:
    if sys.platform().startswith('Win'):
        os.system('py -m pip install -r requirements.txt')
    elif sys.platform().startswith('Lin'):
        os.system('python3 -m pip install -r requirements.txt')
    else:
        print('Not supporter OS.')
        sys.exit()
    print('Dependencies installed! Please restart the bot.')
    sys.exit()

colorama.init()

# CREATE CONFIGS
if not os.path.exists('config.json'):

    api_id = None
    api_hash = None

    while True:

        # GET API HASH
        if api_id is None:
            api_id = input('Insert your api id (get it on my.telegram.org): ')
            if not api_id.isnumeric():
                print('api id isn\'t valid!')
                continue

        # GET API HASH
        if api_hash is None:
            api_hash = input('Insert your api hash (get it on my.telegram.org): ')
            if not api_id.isnumeric():
                print('api id isn\'t valid!')
                continue

        # BREAK CICLE
        if api_hash != None and api_id != None:
            break

    # CREATING SESSION
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        string_session = client.session.save()

    # DUMPING FIRST CONFIG
    dumpConfig({"telegram": {"api_id": int(api_id), "api_hash": str(api_hash), "string_session": str(string_session)}})

# LOAD CURRENT CONFIG
configs = loadConfig()

# CREATE TELEGRAM CLIENT
app = TelegramClient(
    session = StringSession(configs['telegram']['string_session']),
    api_id = configs['telegram']['api_id'],
    api_hash = configs['telegram']['api_hash'],
    request_retries = 3,
)

# LOGS
LOGS = logging.getLogger(__name__)

# COLORS
LEVEL_STYLES = dict(
    info=dict(color='green'),
    warning=dict(color='yellow'),
    error=dict(color='red'),
)

# INSTALL COLORS IN LOGGER
coloredlogs.install(
    level='INFO',
    fmt=f"{time.strftime('%Y/%m/%d | %H:%M:%S')} | %(levelname)s » %(message)s",
    level_styles=LEVEL_STYLES
)
