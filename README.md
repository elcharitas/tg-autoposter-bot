# Telegram Autoposter Bot

This repo started as an offshoot of a work by @FayasNoushad
but turned out to be something far differnt

## Deploy

```sh
git clone https://github.com/elcharitas/tg-autoposter-bot.git
cd tg-autoposter-bot
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

---

## Variables

### Required

- `API_HASH` Your API Hash from my.telegram.org
- `API_ID` Your API ID from my.telegram.org
- `BOT_TOKEN` Your bot token from @BotFather

## Non Required

- `FROM_CHANNELS` From channel ids for auto post
- `TO_CHATS` To channel or group or chat ids for auto post
- `AS_COPY` (bool and optional) For forward as copy
- `FILTER_TEXT` (bool and optional) For text filter
- `FILTER_AUDIO` (bool and optional) For audio filter
- `FILTER_DOCUMENT` (bool and optional) For document filter
- `FILTER_PHOTO` (bool and optional) For photo filter
- `FILTER_STICKER` (bool and optional) For sticker filter
- `FILTER_VIDEO` (bool and optional) For video filter
- `FILTER_ANIMATION` (bool and optional) For animation filter
- `FILTER_VOICE` (bool and optional) For voice filter
- `FILTER_VIDEO_NOTE` (bool and optional) For video note filter
- `FILTER_CONTACT` (bool and optional) For contact filter
- `FILTER_VENUE` (bool and optional) For venue filter
- `FILTER_LOCATION` (bool and optional) For location filter
- `FILTER_POLL` (bool and optional) For poll filter
- `FILTER_GAME` (bool and optional) For game filter
- `REPLY_MARKUP` (bool and optional) For copy reply markup

---
