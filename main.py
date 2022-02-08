import os
from click import command
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def getenv(key, default=""):
  return os.getenv(key) or default

client = MongoClient(getenv("DB_URL")) 
db = client.sketchstorm
hosts = db.users

FROM_CHANNELS = {int(x) for x in getenv("FROM_CHANNELS").split()}
TO_CHATS = {int(x) for x in getenv("TO_CHATS").split()}
AS_COPY = getenv("AS_COPY", True)

# filters for auto post
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

Bot = Client(
    "Channel Auto Post Bot",
    bot_token=getenv("BOT_TOKEN"),
    api_id=int(getenv("API_ID")),
    api_hash=getenv("API_HASH"),
)

START_TEXT = """Hello {},"""
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Channel", url="https://telegram.me/"),
            InlineKeyboardButton("Feedback", url="https://telegram.me/"),
        ],
    ]
)


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
  hosts.insert_one(update.from_user)
  await update.reply_text(
    text=START_TEXT.format(update.from_user.mention),
    disable_web_page_preview=True,
    reply_markup=START_BUTTONS,
  )

@Bot.on_message(
    filters.private
    & (
        filters.text
        if FILTER_TEXT
        else None | filters.audio
        if FILTER_AUDIO
        else None | filters.document
        if FILTER_DOCUMENT
        else None | filters.photo
        if FILTER_PHOTO
        else None | filters.sticker
        if FILTER_STICKER
        else None | filters.video
        if FILTER_VIDEO
        else None | filters.animation
        if FILTER_ANIMATION
        else None | filters.voice
        if FILTER_VOICE
        else None | filters.video_note
        if FILTER_VIDEO_NOTE
        else None | filters.contact
        if FILTER_CONTACT
        else None | filters.location
        if FILTER_LOCATION
        else None | filters.venue
        if FILTER_VENUE
        else None | filters.poll
        if FILTER_POLL
        else None | filters.game
        if FILTER_GAME
        else None
    )
)
async def autopost(bot, update):
    print(update.text)
    chat_id = getenv("TO_CHATS")
    if (
        len(FROM_CHANNELS) == 0
        or len(TO_CHATS) == 0
        or update.chat.id not in FROM_CHANNELS
    ):
        return
    try:
      await update.forward(chat_id=chat_id)
    except Exception as error:
      print(error)


Bot.run()
