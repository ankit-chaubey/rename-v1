import time, os
from decouple import config
from pyrogram import Client, filters
from config import DOWNLOAD_LOCATION, CAPTION, ADMIN
from main.utils import progress_message, humanbytes

@Client.on_message(filters.command("rename") & filters.user(ADMIN))             
async def rename_file(bot, msg):
    reply = msg.reply_to_message
    
    # Ensure there's a file reply and a new name in the command
    if len(msg.command) < 2 or not reply:
        return await msg.reply_text("Please reply to a file (video or audio) with filename + .extension (e.g., `.mkv`, `.mp4`, `.zip`).")
    
    media = reply.document or reply.audio or reply.video
    
    # If the reply is not media (file), prompt the user
    if not media:
        return await msg.reply_text("Please reply to a file (video or audio) with filename + .extension (e.g., `.mkv`, `.mp4`, `.zip`).")
    
    # Get the original media and the new filename
    og_media = getattr(reply, reply.media.value)
    new_name = msg.text.split(" ", 1)[1]
    
    # Ensure that the filename length does not exceed 60 characters, including the file extension
    extension = os.path.splitext(new_name)[1]  # Get file extension
    max_length = 60 - len(extension)
    if len(new_name) > max_length:
        new_name = new_name[:max_length]  # Truncate to fit within 60 characters
    
    new_name_with_extension = new_name + extension  # Final filename with extension
    
    # Inform the user that the download is starting
    sts = await msg.reply_text("Downloading... Please wait.")
    c_time = time.time()
    
    try:
        # Download the media with the new name
        downloaded = await reply.download(file_name=new_name_with_extension, progress=progress_message, progress_args=("Download in progress...", sts, c_time)) 
    except Exception as e:
        return await sts.edit(f"Error during download: {e}")
    
    # Get the human-readable file size
    filesize = humanbytes(og_media.file_size)                
    
    # Handle the caption, if configured
    if CAPTION:
        try:
            cap = CAPTION.format(file_name=new_name_with_extension) #, file_size=filesize)
        except Exception as e:
            return await sts.edit(text=f"Caption Error: Unexpected keyword → ({e})")           
    else:
        # Use full input as caption
        full_caption = msg.text.split(" ", 1)[1]  # Full user input after /rename command
        cap = f"<code>{full_caption}</code>"

    # Thumbnail handling (download if not already present)
    file_thumb = None  # Initialize to avoid reference errors
    try:
        dir_files = os.listdir(DOWNLOAD_LOCATION)
        if len(dir_files) == 0:
            file_thumb = await bot.download_media(og_media.thumbs[0].file_id)
            og_thumbnail = file_thumb
        else:
            og_thumbnail = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"  # Use the existing thumbnail if available
    except Exception as e:
        print(f"Error with thumbnail: {e}")
        og_thumbnail = None
        
    # Upload the downloaded file with the caption and thumbnail
    await sts.edit("Uploading... Please wait.")
    c_time = time.time()
    try:
        await bot.send_document(
            msg.chat.id, 
            document=downloaded, 
            thumb=og_thumbnail, 
            caption=cap, 
            progress=progress_message, 
            progress_args=("Upload in progress...", sts, c_time)
        )        
    except Exception as e:
        return await sts.edit(f"Error during upload: {e}")
    
    # Clean up: Remove the downloaded file and thumbnail if they exist
    try:
        if file_thumb:
            os.remove(file_thumb)
        os.remove(downloaded)
    except Exception as e:
        print(f"Error during cleanup: {e}")

    await sts.delete()
