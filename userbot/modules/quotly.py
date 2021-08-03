import asyncio

from telethon import events
from telethon.errors import YouBlockedUserError

from ..events import newMessage


@newMessage(pattern="q(?: |$)(.*)")
async def _(event):
    reply_to = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    message = ""
    messages_id = []
    if reply:
        if input_str and input_str.isnumeric():
            messages_id.append(reply.id)
            async for message in event.client.iter_messages(
                    event.chat_id,
                    limit=(int(input_str) - 1),
                    offset_id=reply.id,
                    reverse=True,
            ):
                if message.id != event.id:
                    messages_id.append(message.id)
        elif input_str:
            message = input_str
        else:
            messages_id.append(reply.id)
    elif input_str:
        message = input_str
    else:
        await event.edit("Responda al mensaje o proporcione información para que funcione correctamente")
        await asyncio.sleep(5)
        return event.delete()
    chat = "@QuotLyBot"
    catevent = await event.edit("Procesando...")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            if messages_id:
                await event.client.forward_messages(chat, messages_id, event.chat_id)
            elif message != "":
                await event.client.send_message(conv.chat_id, message)
            else:
                await event.edit(
                    catevent, "Supongo que has usado una sintaxis inválida."
                )
                await asyncio.sleep(5)
                return event.delete()
            response = await response
        except YouBlockedUserError:
            await catevent.edit("Por favor desbloquea @QuotLyBot")
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        await catevent.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_to
        )
