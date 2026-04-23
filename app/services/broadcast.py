from app.db.mongo import users_col
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.services.image_service import generate_job_image

async def broadcast_job(app, job):
    rejected_priests = job.get("rejected_by", []) or []

    # Find all verified users who have NOT rejected this job
    users = users_col.find({
        "verified": True,
        "_id": {"$nin": rejected_priests}
    })

    # Generate the custom image dynamically from the job data
    image_bytes = generate_job_image(job)
    photo_to_send = image_bytes

    async for user in users:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Apply",
                    callback_data=f"apply_job_{job['_id']}"
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject_job_{job['_id']}"
                )
            ]
        ])

        try:
            msg = await app.bot.send_photo(
                chat_id=user["_id"],
                photo=photo_to_send,
                caption=f"""
🕉️ <b>{job['title']}</b>

📍 <b>Location:</b> {job['location']}
📅 <b>Date & Time:</b> {job.get('date', 'N/A')} {job.get('time', 'N/A')}
💰 <b>Dakshina:</b> ₹{job.get('fees', 'N/A')}

🙏 <i>Please accept or reject this Aavhan.</i>
""",
                parse_mode="HTML",
                reply_markup=keyboard
            )
            
            # Cache the uploaded image file_id to send instantly to other priests
            if isinstance(photo_to_send, bytes):
                photo_to_send = msg.photo[-1].file_id
                
        except Exception as e:
            print(f"Error sending broadcast to {user.get('_id')}: {e}")