import sys
if sys.platform != "win32":
    import uvloop
    uvloop.install()

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info("🔁 Initializing bot client...")
        super().__init__(
            name="AviaxMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        LOGGER(__name__).info(f"✅ Logged in as {self.name} (@{self.username})")

        # ✅ Test sending log message
        LOGGER(__name__).info(f"📤 Trying to send log message to group ID: {config.LOG_GROUP_ID}")
        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                f"<b>✅ {self.mention} Bot started successfully!</b>\n\n"
                f"<b>ID:</b> <code>{self.id}</code>\n"
                f"<b>Name:</b> {self.name}\n"
                f"<b>Username:</b> @{self.username}",
            )
        except errors.ChatAdminRequired:
            LOGGER(__name__).error(f"❌ Bot is not admin in the log group ({config.LOG_GROUP_ID}).")
            exit()
        except errors.ChannelInvalid:
            LOGGER(__name__).error(f"❌ The log group ID is invalid or no longer exists: {config.LOG_GROUP_ID}")
            exit()
        except errors.PeerIdInvalid:
            LOGGER(__name__).error(
                f"❌ PeerIdInvalid: Telegram doesn’t recognize this group ID yet.\n"
                f"➡️ Make sure your bot received a message from the log group at least once."
            )
            LOGGER(__name__).info("💡 Tip: Send a message in the log group or restart the bot after /getid")
            exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Unknown error while sending log message: {e}")
            exit()

        # ✅ Check if bot is admin in the log group
        try:
            member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Bot is NOT admin in the log group.")
                exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Could not verify bot's admin status. Reason: {e}")
            exit()

        LOGGER(__name__).info(f"✅ Music Bot started successfully as {self.name} (@{self.username})")

    async def stop(self):
        LOGGER(__name__).info("🛑 Stopping bot...")
        await super().stop()
        LOGGER(__name__).info("✅ Bot stopped.")
