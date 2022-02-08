from email.policy import default
import os

def getenv(key, default = ""):
  return os.getenv(key) or default

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
BOT_ID = getenv("BOT_ID")

# filters
FILTER_TEXT = getenv("FILTER_TEXT", True)
FILTER_AUDIO = getenv("FILTER_AUDIO", True)
FILTER_DOCUMENT = getenv("FILTER_DOCUMENT", True)
FILTER_PHOTO = getenv("FILTER_PHOTO", True)
FILTER_STICKER = getenv("FILTER_STICKER", True)
FILTER_VIDEO = getenv("FILTER_VIDEO", True)
FILTER_ANIMATION = getenv("FILTER_ANIMATION", True)
FILTER_VOICE = getenv("FILTER_VOICE", True)
FILTER_VIDEO_NOTE = getenv("FILTER_VIDEO_NOTE", True)
FILTER_CONTACT = getenv("FILTER_CONTACT", True)
FILTER_LOCATION = getenv("FILTER_LOCATION", True)
FILTER_VENUE = getenv("FILTER_VENUE", True)
FILTER_POLL = getenv("FILTER_POLL", True)
FILTER_GAME = getenv("FILTER_GAME", True)

# for copy buttons
REPLY_MARKUP = getenv("REPLY_MARKUP", False)
