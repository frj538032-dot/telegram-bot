import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8847317484:AAE67Lq3xSAEMdv6BjwcsHhi5VWfXsai1H8"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main_keyboard():
    keyboard = [
        ["🎮 لعبة التخمين", "ℹ️ المساعدة"],
        ["📌 معلومات البوت"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"أهلاً بك يا {user.first_name}!\n\nمرحباً بك في البوت الخاص بك.\nاختر من القائمة أدناه:"
    await update.message.reply_text(text, reply_markup=main_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "الأوامر والخدمات المتاحة:\n\n/start - تشغيل البوت\n/help - المساعدة\n\nويمكنك استخدام الأزرار في الأسفل."
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎮 لعبة التخمين":
        context.user_data["guess_number"] = 7
        await update.message.reply_text("خمن رقماً بين 1 و 10:")
        return

    if context.user_data.get("guess_number") is not None:
        if text.isdigit():
            guess = int(text)
            number = context.user_data["guess_number"]
            if guess < number:
                await update.message.reply_text("العدد أكبر من ذلك!")
                return
            elif guess > number:
                await update.message.reply_text("العدد أصغر من ذلك!")
                return
            else:
                await update.message.reply_text("مبروك! إجابة صحيحة 🎉")
                context.user_data["guess_number"] = None
                return

    if text == "ℹ️ المساعدة":
        await help_command(update, context)
    elif text == "📌 معلومات البوت":
        await update.message.reply_text("بوت تلجرام يعمل بنجاح على Termux!")
    else:
        await update.message.reply_text("لم أفهم هذا الأمر، استخدم الأزرار بالأسفل.", reply_markup=main_keyboard())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
