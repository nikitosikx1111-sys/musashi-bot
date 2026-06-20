from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from googletrans import Translator

TOKEN = "YOUR_TELEGRAM_TOKEN"

translator = Translator()
lang = "en"


# 🟢 старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇺🇦 UA", callback_data="uk"),
            InlineKeyboardButton("🇷🇺 RU", callback_data="ru"),
            InlineKeyboardButton("🇬🇧 EN", callback_data="en"),
        ]
    ]

    await update.message.reply_text(
        "Надішли текст — я перекладу його 🌍",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🎛 вибір мови
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lang
    query = update.callback_query
    await query.answer()

    lang = query.data
    await query.edit_message_text(f"Мова вибрана: {lang}")


# 💬 обробка тексту
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        result = translator.translate(text, dest=lang).text
    except:
        result = "Помилка перекладу 😢"

    await update.message.reply_text(result)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()