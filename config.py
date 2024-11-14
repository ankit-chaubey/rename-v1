from decouple import config

# Load configurations using decouple
API_ID = config('API_ID', cast=int)  # Cast to int if the value is an integer
API_HASH = config('API_HASH')        # No cast needed for string values
BOT_TOKEN = config('BOT_TOKEN')
# Convert the ADMIN field from the .env into a list of integers
ADMIN = [int(admin_id) for admin_id in config('ADMIN', default='').split(',') if admin_id]
CAPTION = config('CAPTION', default="")  # Optional field, set a default value if missing

# Set download location for media (can be changed to a configurable value)
DOWNLOAD_LOCATION = "./DOWNLOADS/"
