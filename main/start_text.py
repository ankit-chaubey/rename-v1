from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
from config import ADMIN


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, msg):
    txt = "This bot is for personal use only!"
    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("Creator 🎉", url="https://t.me/ankit_chaubey")
    ], [
        InlineKeyboardButton("More ❔", url="https://t.me/chaubey_ankit")
    ]])

    # If the user is not an admin, show the start message
    if msg.from_user.id not in ADMIN:
        return await msg.reply_text(text=txt, reply_markup=btn, disable_web_page_preview=True)

    # If the user is an admin, send the advanced start message
    await start(bot, msg, cb=False)


@Client.on_callback_query(filters.regex("start"))
async def start(bot, msg, cb=True):
    txt = f"👋🏻 Hello {msg.from_user.mention}, I’m a super-speed bot, quickly renaming files and updating thumbnails in a flash!"
    button = [[
        InlineKeyboardButton("Creator 🎉", url="https://t.me/ankit_chaubey")
    ], [
        InlineKeyboardButton("Commands❔", callback_data="help"),
        InlineKeyboardButton("About Me❕", callback_data="about")
    ]]

    # Editing the message if it's a callback, or sending a new one if it's not
    if cb:
        await msg.message.edit(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
    else:
        await msg.reply_text(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)


@Client.on_callback_query(filters.regex("help"))
async def help(bot, msg):
    txt = "Just send a file and use the /rename <new name> command with a reply to your file.\n\n"
    txt += "Send a photo to set the thumbnail automatically.\n"
    txt += "/view to see your thumbnail.\n"
    txt += "/del to delete your thumbnail."

    button = [[
        InlineKeyboardButton("🚫 Close", callback_data="del"),
        InlineKeyboardButton("⬅️ Back", callback_data="start")
    ]]

    # Editing the help message with the options to close or go back
    await msg.message.edit(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)


@Client.on_callback_query(filters.regex("about"))
async def about(bot, msg):
    me = await bot.get_me()
    master = "<Ankit Chaubey"
    source = "private"

    txt = f"<b>I’m {me.mention}, crafted with the Pyrogram MTProto library for personal use. I’m your trusted assistant for file uploads, downloads, and renaming—all powered by a secure, closed-source codebase to keep things just for you!</b>"
    button = [[
        InlineKeyboardButton("🚫 Close", callback_data="del"),
        InlineKeyboardButton("⬅️ Back", callback_data="start")
    ]]

    # Editing the about message with the source and back options
    await msg.message.edit(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)


@Client.on_callback_query(filters.regex("del"))
async def closed(bot, msg):
    try:
        # Try to delete the message when the user presses "close"
        await msg.message.delete()
    except Exception as e:
        # If there is an error, return silently
        print(f"Error deleting message: {e}")
        return
