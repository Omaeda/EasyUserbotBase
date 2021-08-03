from ..events import newMessage
from datetime import datetime

@newMessage(pattern='ping')
async def _(event):
    start = datetime.now()
    await event.edit('**PONG!!**')
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await event.edit(f"**PONG!!**\n{duration}ms")
