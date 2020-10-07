from . import LOGS, configs, app
from .functions import getModules
from importlib import import_module

# Starting Client
app.start()

# Starting loading modules
LOGS.info(f'Loading Modules...')

for module_name in getModules():
	import_module(f'userbot.modules.{module_name}')
	LOGS.info(f'[{module_name}] Loaded.')

# Modules loaded
LOGS.info('EasyUserBot started correctly!')

# Starting Userbot Main Loop
app.run_until_disconnected()
