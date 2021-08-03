from telethon import events
from telethon.errors import YouBlockedUserError, StickersetInvalidError
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto, InputStickerSetShortName
from telethon.tl import functions, types
from .. import app as client
from typing import BinaryIO, List, Sequence, Tuple, Union
from ..events import newMessage
import itertools
from telethon.events import NewMessage
import datetime
from .. import LOGS

conversation_args = {
    'entity': '@Stickers',
    'timeout': 10,
    'exclusive': True
}
DEFAULT_MUTE = types.InputPeerNotifySettings(
    silent=True,
    mute_until=datetime.timedelta(days=365)
)

async def get_image(event):
    if event and event.media:
        if event.photo:
            return event.photo
        elif event.document:
            if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in event.media.document.attributes:
                return
            if event.gif or event.video or event.audio or event.voice:
                return

            return event.media.document
        else:
            return
    else:
        return


@newMessage(pattern='stickimg')
async def _(event):
    await event.edit("Creando sticker PNG...")
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await get_image(reply_message)

        if not data:
            await event.edit("Responde a una imagen para hacer un sticker!")
            return
    else:
        await event.edit("Responde a una imagen para hacer un sticker!")
        return
    chat = '@stickerator_bot'

    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=384614990)
            )
            await event.client.forward_messages(conv.chat_id, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("Por favor desbloquea @stickerator_bot")
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.delete()
        await event.client.send_message(event.chat_id, response.message, force_document=True)


def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False


def is_animeted_sticker(message):
    try:
        if message.media and message.media.document:
            mime_type = message.media.document.mime_type
            if "tgsticker" in mime_type:
                return True
            else:
                return False
        else:
            return False
    except Exception:
        return False


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


async def stickerset_exists(conv, setname):
    try:
        await client(GetStickerSetRequest(InputStickerSetShortName(setname)))
        response = await silently_send_message(conv, "/addsticker")
        if response.text == "Invalid pack selected.":
            await silently_send_message(conv, "/cancel")
            return False
        await silently_send_message(conv, "/cancel")
        return True
    except StickersetInvalidError:
        return False


@newMessage(pattern='robar ?(.*)')
async def _(event):
    if not event.is_reply:
        await event.edit('Responde a una foto o sticker para robarlo')
        return
    reply_msg = await event.get_reply_message()
    emoji = "🔥"
    input_str = event.pattern_match.group(1)
    if input_str:
        emoji = input_str
    user_id = event.sender_id
    user = await event.client.get_entity(user_id)
    username = "@" + user.username if user.username else user.first_name
    pack_name = f"Pack de Stickers de {username}"
    packshortname = f"StickersB_{user_id}"
    is_a_s = is_animeted_sticker(reply_msg)
    uploaded_sticker = None
    if is_a_s:
        uploaded_sticker = reply_msg.media
        pack_name = f"Pack de Stickers Animados de {username}"
        packshortname = f"StickersAnimados_{user_id}"
    elif not is_message_image(reply_msg):
        await event.edit("Tipo de mensaje no soportado")
        return
    else:
        async with event.client.conversation("@stickerator_bot") as conv:
            try:
                await silently_send_message(conv, "/start")
            except YouBlockedUserError:
                return await event.edit("Desbloquea a @stickerator_bot")
            await conv.send_file(
                file=reply_msg.media,
                allow_cache=False,
                force_document=True
            )
            response = await conv.get_response()
            uploaded_sticker = response.media
    await event.edit("Robando...")
    async with event.client.conversation("@Stickers") as bot_conv:
        if not await stickerset_exists(bot_conv, packshortname):
            await silently_send_message(bot_conv, "/cancel")
            if is_a_s:
                response = await silently_send_message(bot_conv, "/newanimated")
            else:
                response = await silently_send_message(bot_conv, "/newpack")
            if ("Un nuevo pack" or "Yay!") not in response.text:
                await event.edit(f"**FALLADO!!** @Stickers respondió: {response.text}")
                return
            response = await silently_send_message(bot_conv, pack_name)
            if not response.text.startswith("¡Bien!" or "Alright!"):
                await event.edit(f"**FALLADO!!** @Stickers respondió: {response.text}")
                return
            await bot_conv.send_file(
                file=uploaded_sticker,
                allow_cache=False,
                force_document=True
            )
            response = await bot_conv.get_response()
            if ("Lo siento" or "Sorry") in response.text:
                await event.edit(f"**FALLADO!!** @Stickers respondió: {response.text}")
                return
            await silently_send_message(bot_conv, emoji)
            await silently_send_message(bot_conv, "/publish")
            await silently_send_message(bot_conv, f"<{pack_name}>")
            await silently_send_message(bot_conv, "/skip")
            response = await silently_send_message(bot_conv, packshortname)
            if response.text == (
                    "Lo siento, este nombre corto ya está ocupado." or "Sorry, this short name is already taken."):
                await event.edit(f"**FALLADO!!** @Stickers respondió: {response.text}")
                return
        else:
            await silently_send_message(bot_conv, "/cancel")
            await silently_send_message(bot_conv, "/addsticker")
            await silently_send_message(bot_conv, packshortname)
            await bot_conv.send_file(
                file=uploaded_sticker,
                allow_cache=False,
                force_document=True
            )
            response = await bot_conv.get_response()
            if ("Lo siento" or "Sorry") in response.text:
                await event.edit(f"**FALLADO!!** @Stickers respondio: {response.text}")
                return
            await silently_send_message(bot_conv, response)
            await silently_send_message(bot_conv, emoji)
            await silently_send_message(bot_conv, "/done")
    await event.client.send_message(
        "me",
        f"**STICKER AÑADIDO AL PACK**\nPuedes encontrar tu pack [aquí](t.me/addstickers/{packshortname})"
    )
    await event.edit("**ROBADO 👍**")

@newMessage(pattern="delsticker")
async def delsticker(event: NewMessage.Event) -> None:
    """
    Remove a sticker from your existing pack.


    `{prefix}delsticker` in reply to your sticker
    """
    try:
        if not event.reply_to_msg_id:
            await event.answer("`Reply to a sticker to delete it.`")
            return

        reply = await event.get_reply_message()
        if not reply.sticker:
            await event.answer("`Replied to message isn't a sticker.`")
            return

        stickerset = None
        for a in reply.document.attributes:
            if isinstance(a, types.DocumentAttributeSticker):
                stickerset = a.stickerset
                break

        if not stickerset:
            await event.answer("`Couldn't find the sticker set.`")
            return

        result = await client(functions.messages.GetStickerSetRequest(
            stickerset=stickerset
        ))
        short_name = result.set.short_name
        notif = await client(functions.account.GetNotifySettingsRequest(
            peer="Stickers"
        ))
        await _update_stickers_notif(DEFAULT_MUTE)
        await event.answer("`Fetching all your sticker packs.`")
        packs, first_msg = await _list_packs()
        target_pack = None
        for pack in packs:
            if short_name in pack:
                target_pack = pack
                break

        if not target_pack:
            await event.answer("`Couldn't find the specified set in your packs.`")
            await _delete_sticker_messages(first_msg)
            await _update_stickers_notif(notif)
            return

        await event.answer("`Deleting the sticker from your pack.`")
        async with client.conversation(**conversation_args) as conv:
            await conv.send_message('/delsticker')
            await conv.get_response()
            await conv.send_message(target_pack)
            r1 = await conv.get_response()
            LOGS.debug("Stickers:" + r1.text)
            await reply.forward_to("@Stickers")
            r2 = await conv.get_response()
            LOGS.debug("Stickers:" + r2.text)
            if "I have deleted that sticker for you" in r2.text:
                status = True
            else:
                status = r2.text
            await conv.send_message('/cancel')
            await conv.get_response()

        if status is True:
            pack = f"[{short_name}](https://t.me/addstickers/{short_name})"
            await event.answer(
                f"`Successfully removed the sticker from` {pack}"
            )
            await _delete_sticker_messages(first_msg)
        else:
            await event.answer(
                f"**Couldn't delete the sticker. Perhaps it's not in your pack.**"
                "\n`Check the chat with @Stickers for more information.`"
            )
            await client.send_read_acknowledge("@Stickers")
        await _update_stickers_notif(notif)
    except Exception as e:
        import traceback
        traceback.print_exc()


async def _update_stickers_notif(notif: types.PeerNotifySettings) -> None:
    await client(functions.account.UpdateNotifySettingsRequest(
        peer="Stickers",
        settings=types.InputPeerNotifySettings(**vars(notif))
    ))

async def _update_stickers_notif(notif: types.PeerNotifySettings) -> None:
    await client(functions.account.UpdateNotifySettingsRequest(
        peer="Stickers",
        settings=types.InputPeerNotifySettings(**vars(notif))
    ))

async def _delete_sticker_messages(
    message: types.Message
) -> Sequence[types.messages.AffectedMessages]:
    messages = [message]
    async for msg in client.iter_messages(
        entity="@Stickers",
        offset_id=message.id,
        reverse=True
    ):
        messages.append(msg)

    return await client.delete_messages('@Stickers', messages)


async def _list_packs() -> Tuple[List[str], types.Message]:
    async with client.conversation(**conversation_args) as conv:
        first = await conv.send_message('/cancel')
        r1 = await conv.get_response()
        LOGS.debug("Stickers:" + r1.text)
        await client.send_read_acknowledge(conv.chat_id)
        await conv.send_message('/packstats')
        r2 = await conv.get_response()
        LOGS.debug("Stickers:" + r2.text)
        if r2.text.startswith("You don't have any sticker packs yet."):
            return [], first
        await client.send_read_acknowledge(conv.chat_id)
        buttons = list(itertools.chain.from_iterable(r2.buttons or []))
        await conv.send_message('/cancel')
        r3 = await conv.get_response()
        LOGS.debug("Stickers:" + r3.text)
        await client.send_read_acknowledge(conv.chat_id)

        return [button.text for button in buttons] if buttons else [], first