from ..events import newMessage

@newMessage(outgoing=True, pattern='eval')
async def _(event):
	evaluated = event.text.split(' ', 1)[1]

	try:
		return_value = eval(evaluated)
	except Exception as err:
		return_value = err

	await event.respond(f"**EVAL**\n`{evaluated}`\n\n**RETURN**\n`{return_value}`")
