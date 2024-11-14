from pyrogram import Client
from config import *
import os

class Bot(Client):
    # Ensure DOWNLOAD_LOCATION exists when the Bot class is initialized
    def __init__(self):
        if not os.path.isdir(DOWNLOAD_LOCATION):
            os.makedirs(DOWNLOAD_LOCATION)

        super().__init__(
            name="rename",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100,
            plugins={"root": "main"},  # Adjust if 'main' is the right folder for plugins
            sleep_threshold=10,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{me.first_name} | @{me.username} Started..⚡️")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped")

# Initialize and run the bot
bot = Bot()
bot.run()
