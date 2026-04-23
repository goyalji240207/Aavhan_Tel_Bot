from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from config import ADMIN_ID


async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    base_text = (
        "*User Commands:*\n"
        "/start - start bot\n"
        "/help - help menu\n"
        "/menu - show buttons\n"
        "/jobs - list available jobs\n"
        "/applied - view your applied/assigned jobs\n"
        "/rejected - view your rejected jobs"
    )

    admin_text = "\n\n*Admin Commands:*\n/admin_jobs - Open the admin job panel"

    if user_id == int(ADMIN_ID):
        keyboard = [[KeyboardButton("/admin_jobs"), KeyboardButton("/help")]]
    else:
        keyboard = [
            [KeyboardButton("/jobs"), KeyboardButton("/applied")],
            [KeyboardButton("/rejected"), KeyboardButton("/help")]
        ]
        
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if user_id == int(ADMIN_ID):
        await update.message.reply_text(base_text + admin_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(base_text, reply_markup=reply_markup, parse_mode="Markdown")