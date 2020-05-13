from importlib import import_module
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot import LOGS, bot
from userbot.modules import ALL_MODULES

try:
    bot.start()
except PhoneNumberInvalidError:
    print('\nERROR: Numero di cellulare non valido')
    exit(1)

for module_name in ALL_MODULES:
	try:
		imported_module = import_module("userbot.modules." + module_name)
		LOGS.info("Sto caricando  " + module_name)
	except Exception as err:
		LOGS.error(module_name + "non caricato, errore: " + str(err))

LOGS.info("UserBot avviato!")
bot.run_until_disconnected()
