import logging
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ✅ Load environment variables from Koyeb
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")
KOYEB_DOMAIN = os.getenv("KOYEB_DOMAIN")  # Auto-generated domain from Koyeb

# 📝 NSFW text keywords
NSFW_KEYWORDS = ["sex", "nude", "porn", "xxx", "hot", "adult", "escort"]

# 🔥 Set up logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔍 Function to check NSFW images using DeepAI API
def is_nsfw_image(photo_url):
    try:
        response = requests.post(
            "https://api.deepai.org/api/nsfw-detector",
            data={"image": photo_url},
            headers={"api-key": DEEPAI_API_KEY},
        )
        result = response.json()
        return result.get("output", {}).get("nsfw_score", 0) > 0.5  # 🚨 If score > 50%, mark NSFW
    except Exception as e:
        logging.error(f"NSFW check failed: {e}")
        return False  # If API fails, assume safe

# 🔍 Function to check NSFW text
def is_nsfw_text(text):
    return any(word in text.lower() for word in NSFW_KEYWORDS)

# 📸 Handle photo uploads
async def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo = update.message.photo[-1]  # Get highest resolution image
    file_id = photo.file_id
    caption = update.message.caption or "No description"

    # 🔍 Get file URL from Telegram API
    file_info = await context.bot.get_file(file_id)
    photo_url = file_info.file_path

    # 🔍 Check if the image is NSFW
    if is_nsfw_image(photo_url):
        await update.message.reply_text("⚠️ NSFW content detected! Ad rejected.")
        return

    # 🔍 Check if the caption contains NSFW words
    if is_nsfw_text(caption):
        await update.message.reply_text("⚠️ NSFW words detected! Ad rejected.")
        return

    # 🏷️ Create "Contact Seller" button
    keyboard = [[InlineKeyboardButton("📞 Contact Seller", url=f"tg://user?id={user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 📢 Forward to Channel
    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=file_id, caption=caption, reply_markup=reply_markup)

    await update.message.reply_text("✅ Ad posted successfully!")

# 🔗 Webhook Setup
async def set_webhook():
    webhook_url = f"https://{KOYEB_DOMAIN}/{BOT_TOKEN}"
    app = Application.builder().token(BOT_TOKEN).build()
    await app.bot.set_webhook(url=webhook_url)
    logging.info(f"✅ Webhook set: {webhook_url}")

# 🚀 Start Bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Set webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=8000,
        webhook_url=f"https://{KOYEB_DOMAIN}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    main()
