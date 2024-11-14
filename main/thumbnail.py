from pyrogram import Client, filters
from decouple import config
from config import ADMIN, DOWNLOAD_LOCATION
import os

# Ensure the download location directory exists
if not os.path.exists(DOWNLOAD_LOCATION):
    os.makedirs(DOWNLOAD_LOCATION)

@Client.on_message(filters.private & filters.photo & filters.user(ADMIN))                            
async def set_tumb(bot, msg):       
    try:
        # Check if a thumbnail already exists in the download location
        thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
        
        # If a thumbnail already exists, remove the old one
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
        # Download the new thumbnail
        await bot.download_media(message=msg.photo.file_id, file_name=thumbnail_path)
        return await msg.reply(f"Your permanent thumbnail has been saved ✅️.\nIf you change your server or recreate the app, please reset your thumbnail ⚠️")
    
    except Exception as e:
        print(e)
        return await msg.reply_text(f"An error occurred while saving the thumbnail: {str(e)}")

@Client.on_message(filters.private & filters.command("view") & filters.user(ADMIN))                            
async def view_tumb(bot, msg):
    try:
        # Check if the thumbnail exists before trying to send it
        thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
        if os.path.exists(thumbnail_path):
            await msg.reply_photo(photo=thumbnail_path, caption="This is your current thumbnail")
        else:
            return await msg.reply_text("You don't have any thumbnail set.")
    
    except Exception as e:
        print(e)
        return await msg.reply_text(f"An error occurred while retrieving the thumbnail: {str(e)}")

@Client.on_message(filters.private & filters.command(["del", "del_thumb"]) & filters.user(ADMIN))                            
async def del_tumb(bot, msg):
    try:
        # Check if the thumbnail exists before trying to delete it
        thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
            await msg.reply_text("Your thumbnail has been removed 🚫.")
        else:
            return await msg.reply_text("You don't have any thumbnail to delete.")
    
    except Exception as e:
        print(e)
        return await msg.reply_text(f"An error occurred while deleting the thumbnail: {str(e)}")
