from . import LOGS, configs, app

from .functions import getModules

from importlib import import_module

# STARTING CLIENT
app.start()

for module_name in getModules():
	import_module(f'userbot.modules.{module_name}')
	LOGS.info(f'Sto caricando {module_name}')

LOGS.info('EasyUserBot avviato correttamente!')

# STARTING LOOP
app.run_until_disconnected()
