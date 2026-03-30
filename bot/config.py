from decouple import config
import logging

# Basic logging setup
logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger(__name__)

try:
    # Format: config("VAR_NAME", default=VALUE, cast=TYPE)
    APP_ID = config("APP_ID", default=16732227, cast=int)
    API_HASH = config("API_HASH", default="8b5594ad7ad37f3a0a7ddbfb3963bb51")
    BOT_TOKEN = config("BOT_TOKEN", default="6613265810:AAE02TlVelL0lLMpgxkv7cY4Br4Cq6IGDZs")
    
    DEV = config("DEV", default=5868426717, cast=int)
    OWNER = config("OWNER", default="5868426717")
    
    # FFmpeg commands usually stay as a list or string
    ffmpegcode = ["-preset veryfast -c:v libx264 -b:a 64k -crf 38 -map 0 -c:s copy"]
    
    THUMB = config("THUMBNAIL", default="https://graph.org/file/1cc8d7082dc910c0ccee8.jpg")
    
    # Database configurations
    DB_URI = config("DB_URI", default="mongodb+srv://zuzoo:Movie12345@cluster0.y7xfsuh.mongodb.net")
    DB_NAME = config("DB_NAME", default="vjsavecontentbot")

except Exception as e:
    LOGS.error(f"Error loading configuration: {e}")
    exit()
