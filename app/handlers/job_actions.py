from telegram import Update
from telegram.ext import ContextTypes
from bson import ObjectId
from app.services.conflict_service import has_conflict
from app.services.broadcast import broadcast_job

from app.db.mongo import jobs_col


async def job_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    async def edit_reply(new_text):
        # Automatically detect if the message is an image (broadcast) or text (/jobs command)
        if query.message and getattr(query.message, "photo", None):
            await query.edit_message_caption(caption=new_text)
        else:
            await query.edit_message_text(text=new_text)

    # ===== APPLY =====
    if data.startswith("apply_job_"):
        job_id = ObjectId(data.split("_")[2])

        job = await jobs_col.find_one({"_id": job_id})

        if not job:
           await edit_reply("❌ Job not found.")
           return

        if job.get("status") != "open":
           await edit_reply("❌ Job already taken.")
           return
       
        job_datetime = job.get("datetime")
        if job_datetime and await has_conflict(user_id, job_datetime):
           await edit_reply("⛔ Time conflict! You already have a nearby booking.")
           return

        await jobs_col.update_one(
            {"_id": job_id},
            {
            "$set": {
                "status": "assigned",
                "assigned_priest": user_id
            }
            }
        )

        await edit_reply("✅ You applied successfully!")

    # ===== REJECT =====
    elif data.startswith("reject_job_"):
       job_id = ObjectId(data.split("_")[2])

       await jobs_col.update_one(
         {"_id": job_id},
         {
            "$addToSet": {"rejected_by": user_id}
         }
       )

       await edit_reply("❌ Job hidden for you.")

    # ===== CANCEL / WITHDRAW =====
    elif data.startswith("cancel_job_"):
       job_id = ObjectId(data.split("_")[2])

       update_result = await jobs_col.update_one(
         {"_id": job_id, "assigned_priest": user_id},
         {
            "$set": {"status": "open"},
            "$unset": {"assigned_priest": ""},
            "$addToSet": {"rejected_by": user_id}
         }
       )

       if update_result.modified_count > 0:
           # Fetch the updated job to broadcast
           job_to_broadcast = await jobs_col.find_one({"_id": job_id})
           if job_to_broadcast:
               await broadcast_job(context.application, job_to_broadcast)
           
           await edit_reply("❌ You have cancelled your assignment. The job has been re-listed for other priests.")
       else:
           await edit_reply("Could not cancel. The job may no longer be assigned to you.")

    # ===== RE-APPLY =====
    elif data.startswith("reapply_job_"):
        job_id = ObjectId(data.split("_")[2])

        job = await jobs_col.find_one({"_id": job_id})

        if not job:
           await edit_reply("❌ Job not found.")
           return

        if job.get("status") != "open":
           await edit_reply("❌ Job already taken by another priest.")
           return
       
        job_datetime = job.get("datetime")
        if job_datetime and await has_conflict(user_id, job_datetime):
           await edit_reply("⛔ Time conflict! You already have a nearby booking.")
           return

        await jobs_col.update_one(
            {"_id": job_id},
            {
                "$set": {"status": "assigned", "assigned_priest": user_id},
                "$pull": {"rejected_by": user_id}
            }
        )

        await edit_reply("✅ You successfully re-applied and got the job!")