from telegram import Update
from telegram.ext import ContextTypes

from app.db.mongo import users_col

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # ===== APPROVE USER =====
    if data.startswith("approve_user_"):
        user_id = int(data.split("_")[2])

        await users_col.update_one(
            {"_id": user_id},
            {"$set": {"verified": True, "verification_status": "approved"}}
        )

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="🎉 You are VERIFIED! You can now use the bot."
            )
        except Exception as e:
            print("Send error:", e)

        await query.edit_message_text("✅ Approved")

    # ===== REJECT USER =====
    elif data.startswith("reject_user_"):
        user_id = int(data.split("_")[2])

        await users_col.update_one(
            {"_id": user_id},
            {"$set": {"verified": False, "verification_status": "rejected"}}
        )

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Your verification was rejected."
            )
        except Exception as e:
            print("Send error:", e)

        await query.edit_message_text("❌ Rejected")