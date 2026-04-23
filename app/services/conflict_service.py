from datetime import timedelta
from app.db.mongo import jobs_col

# A standard duration for pujas, used to calculate time conflicts.
# For a more advanced system, this could be a field in the job document itself.
PUJA_DURATION_HOURS = 3


async def has_conflict(priest_id, job_datetime):
    """
    Checks if the priest has another assigned job that conflicts with the new one.

    A conflict exists if the time windows of two jobs overlap. We assume a
    fixed duration for each puja to calculate its time window.
    """
    
    # The end time of the new job, assuming a fixed duration.
    new_job_end_time = job_datetime + timedelta(hours=PUJA_DURATION_HOURS)
    
    # Duration in milliseconds for the MongoDB query.
    duration_ms = PUJA_DURATION_HOURS * 60 * 60 * 1000

    # We need to find if there's any existing job that overlaps with the new one.
    # Two intervals [start1, end1] and [start2, end2] overlap if:
    # (start1 < end2) and (start2 < end1).
    #
    # For us, this translates to:
    # existing_job.datetime < new_job_end_time
    # new_job_datetime < (existing_job.datetime + DURATION)
    #
    # We use MongoDB's $expr to perform this comparison on the server side.
    conflict = await jobs_col.find_one({
        "assigned_priest": priest_id,
        "status": "assigned",
        "$expr": {
            "$and": [
                # existing_job_start < new_job_end
                {"$lt": ["$datetime", new_job_end_time]},
                # new_job_start < existing_job_end
                {"$lt": [job_datetime, {"$add": ["$datetime", duration_ms]}]}
            ]
        }
    })

    return conflict is not None