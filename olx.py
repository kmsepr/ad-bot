import logging
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ✅ Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
KOYEB_DOMAIN = os.getenv("KOYEB_DOMAIN")  # Auto-generated domain from Koyeb

# 🔥 Set up logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# 📸 Handle photo uploads
async def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo = update.message.photo[-1]  # Get highest resolution image
    file_id = photo.file_id
    caption = update.message.caption or "No description"

    # 🏷️ Create "Contact Seller" button
    keyboard = [[InlineKeyboardButton("📞 Contact Seller", url=f"tg://user?id={user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 📢 Forward to Channel
    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=file_id, caption=caption, reply_markup=reply_markup)

    await update.message.reply_text("✅ Ad posted successfully!")

# 🚀 Start Bot with Webhook
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Start webhook with correct parameters
    app.run_webhook(
        listen="0.0.0.0",
        port=8000,
        url_path=BOT_TOKEN,  # Corrected argument
        webhook_url=f"https://{KOYEB_DOMAIN}/{BOT_TOKEN}"  # Ensure KOYEB_DOMAIN is set
    )

if __name__ == "__main__":
    main()