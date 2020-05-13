from userbot.events import message
from telethon import functions, types

#OUTGOING=TRUE è per i comandi fatti da voi stessi

@message(outgoing=True, pattern='-start')
async def EasyRespond(e):
	await e.respond("Ehy, ciao, questa è una risposta")