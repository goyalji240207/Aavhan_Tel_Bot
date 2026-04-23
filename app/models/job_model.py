def create_job_schema(title, date, time, fees, location):
    return {
        "_id": "...",
        "title": title or "Griha Pravesh Puja",
        "date": date or "2026-04-25",
        "time": time or "10:00",
        "location": location or "Kanpur",
        "fees": fees or 1500,
        "status": "open",
        "assigned_priest": None,  
        "rejected_by": [],        
        "created_at": "...",
        "updated_at": "..."
    }