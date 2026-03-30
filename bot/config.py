#    This file is part of the Compressor distribution.
#    Copyright (c) 2021 Danish_00

from decouple import config
import logging

# Basic logging setup for config errors
logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger(__name__)

try:
    APP_ID = config("APP_ID", cast=int)
    API_HASH = config("API_HASH")
    BOT_TOKEN = config("BOT_TOKEN")
    DEV = config("DEV", default=5868426717, cast=int)
    OWNER = config("OWNER" , "5868426717")
    ffmpegcode = ["-preset veryfast -c:v libx264 -b:a 64k -crf 38 -map 0 -c:s copy"]
    THUMB = config("THUMBNAIL" , "https://graph.org/file/1cc8d7082dc910c0ccee8.jpg")
    
    # ADDED: Database configurations for the Restricted Content Login
    DB_URI = config("DB_URI", default="")
    DB_NAME = config("DB_NAME", default="vjsavecontentbot")
except Exception as e:
    LOGS.info("Environment vars Missing")
    LOGS.info("something went wrong")
    LOGS.info(str(e))
    exit()
