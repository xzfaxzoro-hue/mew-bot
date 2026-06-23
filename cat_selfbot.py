import asyncio
import random
from telethon import TelegramClient, events

# === تنظیمات: اینا رو از https://my.telegram.org بگیر ===
API_ID = 38559502          # عدد api_id خودت
API_HASH = "d176a13acfb7dbd702aa2549cf2cbb57"  # رشته api_hash خودت

client = TelegramClient("cat_selfbot_session", API_ID, API_HASH)

ON_TRIGGER = "پیشی روشن"
OFF_TRIGGER = "پیشی خاموش"
MEOW_INTERVAL = 5 * 61  # هر ۶ دقیقه
MEOW_WORDS = ["میو", "مع"]

active_tasks = {}  # chat_id -> task فعال


async def meow_loop(chat_id):
    try:
        while True:
            await asyncio.sleep(MEOW_INTERVAL)
            await client.send_message(chat_id, random.choice(MEOW_WORDS))
    except asyncio.CancelledError:
        pass


@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    text = (event.raw_text or "").strip()
    chat_id = event.chat_id

    if text == ON_TRIGGER:
        if chat_id in active_tasks:
            active_tasks[chat_id].cancel()
        active_tasks[chat_id] = asyncio.create_task(meow_loop(chat_id))
        await event.respond("پیشی روشن شد😼")

    elif text == OFF_TRIGGER:
        task = active_tasks.pop(chat_id, None)
        if task:
            task.cancel()
        await event.respond("پیشی خاموش شد😿")


print("start...")
client.start()
client.run_until_disconnected()