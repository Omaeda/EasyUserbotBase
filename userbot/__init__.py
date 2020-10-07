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
    if sys.platform.lower().startswith('win'):
        os.system('py -m pip install -r requirements.txt')
    elif sys.platform.lower().startswith('lin'):
        os.system('python3 -m pip install -r requirements.txt')
    else:
        print('Not supporter OS.')
        sys.exit()
    print('Dependencies installed! Please restart the bot.')
    sys.exit()

colorama.init()

# Check far configs.json
if not os.path.exists('config.json'):

    api_id = None
    api_hash = None

    while True:

        # Getting Api Id
        if api_id is None:
            api_id = input('Insert your api id (get it on my.telegram.org): ')
            if not api_id.isnumeric():
                print('api id isn\'t valid!')
                continue

        # Getting Api Hash
        if api_hash is None:
            api_hash = input('Insert your api hash (get it on my.telegram.org): ')
            if not api_id.isnumeric():
                print('api id isn\'t valid!')
                continue

        # BREAK CICLE
        if api_hash != None and api_id != None:
            break

    # Creating Client for saving string_session in configs
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        string_session = client.session.save()

    # Dumping first config
    dumpConfig({"telegram": {"api_id": int(api_id), "api_hash": str(api_hash), "string_session": str(string_session)}})

# Load currenti configs
configs = loadConfig()

# Create Main Client
app = TelegramClient(
    session = StringSession(configs['telegram']['string_session']),
    api_id = configs['telegram']['api_id'],
    api_hash = configs['telegram']['api_hash'],
    request_retries = 3,
)

# Creating Logs
LOGS = logging.getLogger(__name__)

# Manage Colors
LEVEL_STYLES = dict(
    info=dict(color='green'),
    warning=dict(color='yellow'),
    error=dict(color='red'),
)

# Install colors in Logs
coloredlogs.install(
    level='INFO',
    fmt=f"{time.strftime('%Y/%m/%d | %H:%M:%S')} | %(levelname)s » %(message)s",
    level_styles=LEVEL_STYLES
)
