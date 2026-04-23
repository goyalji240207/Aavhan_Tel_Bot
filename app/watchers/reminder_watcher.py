import asyncio
from datetime import datetime
from app.db.mongo import jobs_col


async def reminder_loop(app):
    print("⏰ Reminder system started...")

    while True:
        now = datetime.utcnow()

        jobs = jobs_col.find({"status": "assigned"})

        async for job in jobs:

            # ✅ safety (avoid crash)
            if "datetime" not in job:
                continue

            job_time = job["datetime"]
            priest_id = job.get("assigned_priest")

            if not priest_id:
                continue

            diff = (job_time - now).total_seconds()

            # skip past jobs
            if diff <= 0:
                continue

            if diff <= 86400 and "24h" not in job.get("reminders_sent", []):
                await send_reminder(app, priest_id, job, "24h")

            if diff <= 7200 and "2h" not in job.get("reminders_sent", []):
                await send_reminder(app, priest_id, job, "2h")

            if diff <= 3600 and "1h" not in job.get("reminders_sent", []):
                await send_reminder(app, priest_id, job, "1h")

        await asyncio.sleep(60)

def format_time_left(seconds):
    if seconds <= 0:
        return "Starting now"

    minutes = int(seconds // 60)
    hours = int(minutes // 60)

    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes} minutes"
    else:
        return f"{int(seconds)} sec"


def format_datetime(dt):
    return dt.strftime("%d %b, %I:%M %p")


async def send_reminder(app, user_id, job, tag):
    try:
        now = datetime.utcnow()
        job_time = job["datetime"]

        diff = (job_time - now).total_seconds()
        time_left = format_time_left(diff)

        # 🎯 tag styling
        if tag == "24h":
            title = "🔔 Reminder — Tomorrow"
            emoji = "🕊️"
        elif tag == "2h":
            title = "⚠️ Reminder — 2 Hours Left"
            emoji = "⏳"
        elif tag == "1h":
            title = "🚨 URGENT — 1 Hour Left"
            emoji = "🔥"
        else:
            title = "🔔 Reminder"
            emoji = "📿"

        text = f"""
{title}

{emoji} *{job['title']}*
📍 {job['location']}

🕒 *Scheduled:* {format_datetime(job_time)}
⏳ *Time left:* {time_left}

🙏 Please be ready before time.
"""

        await app.bot.send_message(
            chat_id=user_id,
            text=text.strip(),
            parse_mode="Markdown"
        )

        # ✅ mark sent
        await jobs_col.update_one(
            {"_id": job["_id"]},
            {"$addToSet": {"reminders_sent": tag}}
        )

    except Exception as e:
        print("Reminder error:", e)