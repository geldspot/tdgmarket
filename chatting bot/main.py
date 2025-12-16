from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

BOT_TOKEN = "8025355615:AAGbpfMrHI2CeKJr2yiM2HZ2MEzv3g8nj0s"
SUPPORT_GROUP_ID = -1003591004367  # আপনার গ্রুপ আইডি

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧑‍💻 Live Support", callback_data="support")],
        [InlineKeyboardButton("🌐 Visit Website", url="https://www.youtube.com/channel/UCKzBO2Rwo8iX0GGw9IyvcQg")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/tdgmarket")]
    ]
    await update.message.reply_text(
        "স্বাগতম! নিচের অপশন বেছে নিন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Button click
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "support":
        context.user_data["support"] = True
        await query.message.reply_text(
            "✍️ আপনার মেসেজ লিখুন, সাপোর্ট টিম রিপ্লাই দেবে।"
        )

# User message → Group
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("support"):
        user = update.message.from_user
        text = update.message.text

        msg = (
            f"📩 New Support Message\n\n"
            f"👤 Name: {user.full_name}\n"
            f"🆔 User ID: {user.id}\n\n"
            f"💬 Message:\n{text}"
        )

        sent = await context.bot.send_message(
            chat_id=SUPPORT_GROUP_ID,
            text=msg
        )

        # Map message ID
        context.bot_data[sent.message_id] = user.id

        await update.message.reply_text(
            "✅ আপনার মেসেজ পাঠানো হয়েছে।"
        )

# Admin reply → User
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = update.message.reply_to_message
    if reply and reply.message_id in context.bot_data:
        user_id = context.bot_data[reply.message_id]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💬 Support Reply:\n{update.message.text}"
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & filters.PRIVATE, user_message))
app.add_handler(MessageHandler(filters.REPLY & filters.Chat(SUPPORT_GROUP_ID), admin_reply))

app.run_polling()
