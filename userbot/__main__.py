from . import LOGS, configs, app
from .functions import getModules
from importlib import import_module

# STARTING CLIENT
app.start()

# LOADING MODULES
LOGS.info(f'Comincio a caricare i moduli...')

for module_name in getModules():
	import_module(f'userbot.modules.{module_name}')
	LOGS.info(f'[{module_name}] Caricato.')

LOGS.info('EasyUserBot caricato ed avviato correttamente!')

# STARTING LOOP
app.run_until_disconnected()
