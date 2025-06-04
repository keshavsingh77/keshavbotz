from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import save_file, search_file_by_name, get_file_by_id
from utils import create_telegraph_page
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Welcome! Use /search <name> to find movies.")

@app.on_message(filters.command("search"))
async def search_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("🔍 Usage: `/search movie name`", parse_mode="markdown")
    query = message.text.split(None, 1)[1]
    results = search_file_by_name(query)
    if not results:
        return await message.reply("❌ No results found.")
    
    text = f"<b>🎬 Results for <u>{query}</u>:</b>\n\n"
    for res in results:
        text += f"🍿 <b>{res['title']}</b> [{res['quality']}] ({res['size']})\n"
        text += f"👉 <a href='https://t.me/{client.me.username}?start=dl_{res['id']}'>Click to Download</a>\n\n"
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.regex(r"^/start dl_"))
async def download_handler(client, message):
    file_id = message.text.split("dl_")[1]
    file = get_file_by_id(file_id)
    if not file:
        return await message.reply("❌ File not found.")
    await message.reply_document(file_id=file['file_id'], caption=file['caption'])

@app.on_message(filters.document | filters.video)
async def save_media(client, message):
    media = message.document or message.video
    await save_file(media.file_id, media.file_name, media.file_size, "480p", media.mime_type)
    await message.reply("✅ File saved!")

app.run()
