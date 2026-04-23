from app.db.mongo import users_col

async def is_verified(user_id):
    user = await users_col.find_one({"_id": user_id})
    return user and user.get("verified")