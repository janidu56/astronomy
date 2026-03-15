import requests
import schedule
import time
import asyncio
from telegram import Bot

# ===== SETTINGS =====
NASA_API_KEY = "ivsZDZ7bavbt66AhhjXFafBiwDhVUC6d9YMztZDm"
TELEGRAM_TOKEN = "8798451038:AAFlIBp6UWfxrIg8XDbL9MthJ1Jp1Q--Mes"
CHANNEL_ID = "@hiarjuna"  # e.g. @astronomy_daily

bot = Bot(token=TELEGRAM_TOKEN)

async def post_apod():
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
        data = requests.get(url).json()

        image_url = data["url"]
        title = data["title"]
        explanation = data["explanation"]
        media_type = data.get("media_type", "image")

        if media_type != "image":
            # Video / non-image content
            message = f"🌌 Astronomy Picture of the Day\n\n📌 {title}\nToday APOD is a video: {image_url}"
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
            print("Video link sent to channel")
            return

        caption = f"""
🌌 Astronomy Picture of the Day

📌 {title}

{explanation[:700]}...

#astronomy #space #nasa
"""
        await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=caption)
        print("Photo posted to channel successfully")

    except Exception as e:
        print("Error:", e)


def run_bot():
    asyncio.run(post_apod())


# Optional: test immediately
run_bot()

# Schedule daily post at 02:49 AM (local PC time)
schedule.every().day.at("02:49").do(run_bot)

print("Bot started... posting to channel")

while True:
    schedule.run_pending()
    time.sleep(30)
