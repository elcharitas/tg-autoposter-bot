# platform specific imports
from os import getenv
from asyncio import get_event_loop
from pydoc import cli
from random import random

# telethon specific imports
from telethon import TelegramClient as Client
from telethon.events import NewMessage
from telethon.tl.types import Message
from telethon.sessions import SQLiteSession


# custom imports
from session import MongoSession
from constants import (
  API_HASH,
  API_ID,
  BOT_ID,
  START_TEXT,
  START_BUTTONS
)

# instantiate new session
Session = MongoSession()
async_jobs = get_event_loop()

async def start_process():
  bot = Client(Session, API_ID, API_HASH)
  await bot.start(bot_token = BOT_ID)

  @bot.on(NewMessage(incoming=True, pattern="^/start$"))
  async def start_command(message):
    reply = START_TEXT.format(message.sender.username)
    await message.reply(reply)
  
  @bot.on(NewMessage(incoming=True, pattern="^/new"))
  async def add_host_command(message):
    async with bot.conversation(message.chat) as conv:
      # replace input with a conversation
      async def request_code():
        await conv.send_message("Input code sent by telegram")
        return (await conv.get_response()).raw_text
      
      await conv.send_message("What's the number you wish to add?")
      phone = await conv.get_response()
      client = Client("sessions/" + phone.raw_text, API_ID, API_HASH)

      # attempt to signin user
      #try:
      await client.start(
        phone.raw_text,
        code_callback=request_code
      )
      await conv.send_message("Number Added successfully")
      # except:
      #   await conv.send_message("Number could not be added. Please try again")

  @bot.on(NewMessage(incoming=True, pattern="^/add"))
  async def add_message(message):
    async with bot.conversation(message.chat) as conv:
      await conv.send_message("Input new message to add")
      Session.cursor("messages").insert_one({
        "message": (await conv.get_response()).raw_text
      })
      await conv.send_message("Message added succesfully")

  @bot.on(NewMessage(pattern="/send", incoming=True))
  async def send_messages(update):
    async_jobs.create_task(
        start(phoneSession) for phoneSession in SQLiteSession.list_sessions()
    )

  # start sending messages on behalf of accounts
  async def start(phoneSession) -> None:
    client = Client(
      phoneSession,
      API_ID,
      API_HASH
    )
    await client.start(phoneSession.id)
    # profile = await client.get_me()
    @client.on(NewMessage())
    async def send_msg(message):
      msgs = Session.cursor("message").find()
      message.reply(msgs[random(0, len(msgs))])

# create main task and start running
async_jobs.create_task(start_process())
async_jobs.run_forever()
