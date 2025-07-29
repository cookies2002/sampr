import sys
if sys.platform != "win32":
    import uvloop
    uvloop.install()

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="AviaxMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        # ✅ Test message to log group
        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                f"<b>✅ {self.mention} Bot started successfully!</b>\n\n"
                f"<b>ID:</b> <code>{self.id}</code>\n"
                f"<b>Name:</b> {self.name}\n"
                f"<b>Username:</b> @{self.username}",
            )
        except (errors.ChatAdminRequired, errors.ChannelInvalid, errors.PeerIdInvalid) as e:
            LOGGER(__name__).error(
                f"❌ Cannot send message to LOG_GROUP_ID ({config.LOG_GROUP_ID}).\nReason: {type(e).__name__}"
            )
            exit()
        except Exception as e:
            LOGGER(__name__).error(
                f"❌ Unknown error while sending log message: {e}"
            )
            exit()

        # ✅ Check admin rights
        try:
            member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Bot is not admin in the log group.")
                exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Cannot verify bot's admin status.\nReason: {e}")
            exit()

        LOGGER(__name__).info(f"✅ Music Bot started as {self.name}")

    async def stop(self):
        await super().stop()
