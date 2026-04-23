from app.db.mongo import jobs_col

async def get_available_jobs(user_id):
    jobs = jobs_col.find({
        "status": "open",
        "rejected_by": {"$nin": [user_id]}
    }).sort("created_at", -1)

    return await jobs.to_list(length=20)

async def get_applied_jobs(user_id):
    jobs = jobs_col.find({
        "assigned_priest": user_id,
        "status": "assigned"
    }).sort("created_at", -1)

    return await jobs.to_list(length=20)

async def get_rejected_jobs(user_id):
    jobs = jobs_col.find({
        "rejected_by": user_id
    }).sort("created_at", -1)

    return await jobs.to_list(length=20)

async def get_completed_jobs(user_id):
    jobs = jobs_col.find({
        "assigned_priest": user_id,
        "status": "completed"
    }).sort("created_at", -1)

    return await jobs.to_list(length=20)

async def get_jobs_by_status(status: str):
    """Fetches all jobs with a given status ('open' or 'assigned')."""
    jobs = jobs_col.find({"status": status}).sort("created_at", -1)
    return await jobs.to_list(length=50) # Limit for admin view

async def get_all_rejected_jobs():
    """Fetches all jobs that have been rejected by at least one priest."""
    jobs = jobs_col.find({
        "rejected_by": {"$exists": True, "$ne": []}
    }).sort("created_at", -1)
    return await jobs.to_list(length=50) # Limit for admin view