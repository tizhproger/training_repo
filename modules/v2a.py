# ---------------------------------------------------------------------------------
#  ,_     _          
#  |\_,-~/          
#  / _  _ |    ,--.  🌐 This module was loaded through https://t.me/hikkamods_bot
# (  @  @ )   / ,-'  🔐 Licensed under the GNU AGPLv3.
#  \  _T_/-._( (     
#  /         `. \    ⚠️ Owner of this bot doesn't take responsibility for any
# |         _  \ |   errors caused by this module or this module being non-working
#  \ \ ,  /      |   and doesn't take ownership of any copyrighted material.
#   || |-_\__   /    
#  ((_/`(____,-'     
# ---------------------------------------------------------------------------------
# Name: v2a
# Description: Converts video \ round messages to audio \ voice messages
# Author: hikariatama
# Commands:
# .v2a | .waveform
# ---------------------------------------------------------------------------------

#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.hikari.gay/v2a_icon.png
# meta developer: @hikarimods
# meta banner: https://mods.hikariatama.ru/badges/v2a.jpg
# scope: ffmpeg
# scope: hikka_only
# scope: hikka_min 1.3.0

import asyncio
import io
import os
import logging
import tempfile

from telethon.tl.types import Message, DocumentAttributeAudio
import telethon.utils as tlutils

import utils

logger = logging.getLogger(__name__)



class Video2Audio:
    """Converts video \ round messages to audio \ voice messages"""

    strings = {
        "name": "Video2Audio",
        "no_video": "🚫 **Ответь на видео**",
        "converting": "🧚‍♀️ **Конвертирую...**",
        "_cls_doc": "Конвертирует видео в аудио",
        "error": "🚫 **Ошибка при конвертировании**",
    }
    
    def __init__(self, client):
        self._client = client


    async def v2acmd(self, message: Message):
        """<reply> [-vm] [-b] - Convert video to audio
        -vm - Use voice message instead"""
        use_voicemessage = "-vm" in utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply or not reply.video:
            await utils.answer(message, self.strings["no_video"])
            return

        if use_voicemessage:
            await self.waveform(message)
        else:
            await utils.answer(message, self.strings["converting"])
            sound = await reply.download_media(bytes)

            audiofile = io.BytesIO(sound)
            audiofile.name = "audio.mp3"

            await self._client.send_file(
                message.peer_id,
                audiofile,
                voice_note=use_voicemessage,
                reply_to=reply.id,
                attributes=[
                    DocumentAttributeAudio(
                        duration=next(
                            (
                                attr.duration
                                for attr in reply.document.attributes
                                if hasattr(attr, "duration")
                            ),
                            0,
                        ),
                        voice=False
                    )
                ],
            )

            if message.out:
                await message.delete()

    async def waveform(self, message: Message):
        """<reply to voice> - Create buggy waveform"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings["no_video"])
            return

        await utils.answer(message, self.strings["converting"])
        document = io.BytesIO(await reply.download_media(bytes))
        document.name = "audio.ogg"

        await self._client.send_file(
            message.peer_id,
            document,
            voice_note=True,
            reply_to=reply.id,
            attributes=[
                DocumentAttributeAudio(
                    duration=next(
                        (
                            attr.duration
                            for attr in reply.document.attributes
                            if hasattr(attr, "duration")
                        ),
                        0,
                    ),
                    voice=True,
                    waveform=tlutils.encode_waveform(
                        bytes(
                            (
                                *tuple(range(0, 30, 5)),
                                *reversed(tuple(range(0, 30, 5))),
                            )
                        )
                        * 20
                    ),
                )
            ],
        )

        if message.out:
            await message.delete()
