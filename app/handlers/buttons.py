from telegram import Update
from telegram.ext import ContextTypes
from app.keyboards.menu import  inline_menu

async def menu_command(update, context):
   await update.message.reply_text(
    "Choose an option:",
    reply_markup=inline_menu()
)
    
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
   
    data = query.data

    if data == "jobs":
        await query.edit_message_text("Job list coming soon...")

    elif data == "profile":
        await query.edit_message_text("Your profile")

    elif data == "help":
        await query.edit_message_text("Use /help command")

    