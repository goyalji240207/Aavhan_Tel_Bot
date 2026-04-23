from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from app.db.mongo import users_col
from app.handlers.auth import start_verification
from config import ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Auto-verify the admin so they immediately get access to the menu
    if user.id == int(ADMIN_ID):
        await users_col.update_one(
            {"_id": user.id},
            {"$set": {"verified": True, "verification_status": "approved", "role": "admin", "name": user.full_name}},
            upsert=True
        )

    db_user = await users_col.find_one({"_id": user.id})
    
    if not db_user:
        return await start_verification(update, context)
    
    if not db_user.get("verified"):
        status = db_user.get("verification_status")
        
        if status == "pending":
            await update.message.reply_text("⏳ Your verification is in progress.")
        
        elif status == "rejected":
            await update.message.reply_text("❌ Verification rejected. Contact admin.")
            return ConversationHandler.END
        else:
            return await start_verification(update, context)
            
        return ConversationHandler.END
    
    # Build the main menu keyboard
    if user.id == int(ADMIN_ID):
        keyboard = [
            [KeyboardButton("/admin_jobs"), KeyboardButton("/broadcast")],
            [KeyboardButton("/help")]
        ]
    else:
        keyboard = [
            [KeyboardButton("/jobs"), KeyboardButton("/applied")],
            [KeyboardButton("/rejected"), KeyboardButton("/help")]
        ]
        
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🙏 Welcome back! You are verified.\n\nChoose an option from the menu below:", 
        reply_markup=reply_markup
    )

    return ConversationHandler.END