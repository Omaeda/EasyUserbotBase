from .. import app
from ..events import newMessage


@newMessage(pattern='purge')
async def _(event):
    reply = await event.get_reply_message()
    if not event.is_reply:
        await event.edit('Responde a un mensaje')
        return
    temp = [event.id]
    async for msg in app.iter_messages(event.input_chat, min_id=reply.id - 1, max_id=event.id):
        temp.append(msg.id)
    await app.delete_messages(event.input_chat, temp)
