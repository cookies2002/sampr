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

        log_target = config.LOG_GROUP_ID if config.LOG_GROUP_ID != 0 else config.LOG_GROUP_USERNAME
        LOGGER(__name__).info(f"📤 Trying to send log message to: {log_target}")

        log_message = (
            f"<b>✅ {self.mention} Bot started successfully!</b>\n\n"
            f"<b>ID:</b> <code>{self.id}</code>\n"
            f"<b>Name:</b> {self.name}\n"
            f"<b>Username:</b> @{self.username}"
        )

        try:
            await self.send_message(log_target, log_message)
        except errors.PeerIdInvalid:
            LOGGER(__name__).warning("⚠️ Group ID or username not recognized.")
            LOGGER(__name__).info("💡 Sending fallback log to OWNER_ID instead.")
            try:
                await self.send_message(config.OWNER_ID, f"⚠️ Could not log to group.\n\n{log_message}")
            except Exception as e:
                LOGGER(__name__).error(f"❌ Fallback to OWNER_ID failed: {e}")
            exit()
        except errors.ChatAdminRequired:
            LOGGER(__name__).error("❌ Bot is not admin in the log group.")
            exit()
        except errors.ChannelInvalid:
            LOGGER(__name__).error("❌ The log group is invalid or deleted.")
            exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Unknown error while sending log message: {e}")
            exit()

        # Check admin rights only if numeric ID is used
        if config.LOG_GROUP_ID != 0:
            try:
                member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
                if member.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error("❌ Bot is NOT admin in the log group.")
                    exit()
            except Exception as e:
                LOGGER(__name__).error(f"❌ Could not verify admin status: {e}")
                exit()

        LOGGER(__name__).info(f"✅ Bot fully started as {self.name} (@{self.username})")

    async def stop(self):
        LOGGER(__name__).info("🛑 Stopping bot...")
        await super().stop()
        LOGGER(__name__).info("✅ Bot stopped.")
