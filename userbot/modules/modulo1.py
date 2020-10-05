from ..events import newMessage

@newMessage(outgoing=True, pattern='start', prefix=['/', '.'])
async def _(event):
	await event.respond("Ehy, ciao, questa è una risposta")
