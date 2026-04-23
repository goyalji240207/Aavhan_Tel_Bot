import asyncio
from fastapi import APIRouter, Request
from telegram import Update

from app.bot import create_bot
from app.watchers.job_watcher import watch_jobs
from config import WEBHOOK_URL, BOT_TOKEN
from app.watchers.reminder_watcher import reminder_loop

router = APIRouter()

telegram_app = create_bot()

@router.on_event("startup")
async def startup():
 
    await telegram_app.initialize()
    url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    info = await telegram_app.bot.get_webhook_info()
    if info.url != url:
        await telegram_app.bot.set_webhook(url)

    # start background systems
    asyncio.create_task(watch_jobs(telegram_app))
    asyncio.create_task(reminder_loop(telegram_app))

    print("🚀 Webhook active and MongoDB Watcher started!")

@router.on_event("shutdown")
async def shutdown():
    """
    Runs when the server stops.
    Cleanly shuts down the bot and removes the webhook.
    """
    await telegram_app.bot.delete_webhook()
    await telegram_app.stop()
    await telegram_app.shutdown()

@router.post(f"/{BOT_TOKEN}")
async def webhook_handler(request: Request):
    """
    Receives updates from Telegram and pushes them into the bot's update queue.
    """
    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        
        await telegram_app.process_update(update)
        
        return {"ok": True}
    except Exception as e:
        print(f"Error processing update: {e}")
        return {"ok": False, "error": str(e)}