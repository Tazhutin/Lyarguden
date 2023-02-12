
import logging
import asyncio
from loguru import logger

from src import *



from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, PicklePersistence, ConversationHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)




START, MEETING = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("*Hello!*\n\nI'm your personal assistant — Lyarguden.\n\nUnfortunately, I'm at an early stage of development at the moment and my options are limited.", parse_mode="markdown")

    await update.message.reply_chat_action("typing")
    await asyncio.sleep(3)
    
    await context.bot.send_message(chat_id=os.environ['ADMIN_CHAT_ID'], text="User ", parse_mode="markdown")

    await update.message.reply_text("Please enter a name by which I can contact you:", reply_markup=ReplyKeyboardMarkup(keyboard=[["Sir", "Madame"]], input_field_placeholder="You can write something like... My lord or my king and etc. ", resize_keyboard=True))


    return MEETING
    




async def meeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    entered_name = update.message.text

    await update.message.reply_text(f"Okay, from now I will call you — {entered_name}\n\nNice to meet you!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END





def main() -> None:
    persistence = PicklePersistence(filepath="conversationbot")
    print(os.environ["API_KEY"])
    application = Application.builder().token(os.environ["API_KEY"]).concurrent_updates(True).persistence(persistence).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MEETING: [MessageHandler(filters.TEXT & ~filters.COMMAND, meeting)],
        },
        fallbacks=[],
        name="start_conv",
        persistent=True,
    )

    application.add_handler(conv_handler)

    application.run_polling()




if __name__ == "__main__":
    main()
