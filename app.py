# platform specific imports
from os import getenv
from asyncio import get_event_loop
from pydoc import cli

# telethon specific imports
from telethon import TelegramClient as Client, events
from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRequestPhone


# custom imports
from session import MongoSession
from constants import ( API_HASH, API_ID, BOT_ID )

# instantiate new session
Session = MongoSession()

async_jobs = get_event_loop()
client = Client(Session, API_ID, API_HASH)

START_TEXT = """Hello {}, Ill be needing your contact to set up the integration!"""
START_BUTTONS = ReplyKeyboardMarkup(
  [
    [
      KeyboardButtonRequestPhone("Send Phone Number"),
    ],
  ]
)

async def start_process():
  Bot = await client.start(bot_token = BOT_ID)

  @Bot.on(events.NewMessage(incoming=True))
  async def bot_start(bot, update):
    await update.reply_text(
      text=START_TEXT.format(update.from_user.mention),
      disable_web_page_preview=True,
      reply_markup=START_BUTTONS,
    )

  @Bot.on(events.NewMessage(incoming=True))
  async def sent_contact(bot, update):
    print(update)
    await client.start(update.text)

  async def start(phone) -> None:
    await client.start(phone)
    host = await client.get_me()
    print(host)

  for phone in Session.find("hosts"):
    task = start(phone)
    async_jobs.create_task(task)

async_jobs.create_task(start_process())

async_jobs.run_forever()
