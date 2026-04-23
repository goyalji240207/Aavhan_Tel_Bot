from app.db.mongo import users_col


async def get_user_details(user_id: int):
    """Fetches a single user by their ID."""
    return await users_col.find_one({"_id": user_id})


async def get_users_details(user_ids: list[int]):
    """Fetches multiple users from a list of IDs."""
    if not user_ids:
        return []
    users_cursor = users_col.find({"_id": {"$in": user_ids}})
    return await users_cursor.to_list(length=len(user_ids))