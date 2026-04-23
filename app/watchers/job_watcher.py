import asyncio
from app.db.mongo import jobs_col
from app.services.broadcast import broadcast_job


sent_jobs = set()

async def watch_jobs(app):
    async with jobs_col.watch([{"$match": {"operationType": "insert"}}]) as stream:
        async for change in stream:
            job = change["fullDocument"]
            job_id = str(job["_id"])

            if job_id in sent_jobs:
                continue

            sent_jobs.add(job_id)

            print("🔥 New job detected:", job_id)

            await broadcast_job(app, job)