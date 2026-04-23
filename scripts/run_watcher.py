import asyncio
import signal

from app.watchers.job_watcher import watch_jobs
from app.bot import create_bot


async def main():
    app = create_bot()
    await app.initialize()
    await app.start()

    print("👀 Watcher started...")

    # graceful shutdown event
    stop_event = asyncio.Event()

    def stop():
        print("🛑 Shutting down watcher...")
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, stop)
    loop.add_signal_handler(signal.SIGTERM, stop)

    watcher_task = asyncio.create_task(watch_jobs(app))

    await stop_event.wait()

    watcher_task.cancel()

    await app.stop()
    await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())