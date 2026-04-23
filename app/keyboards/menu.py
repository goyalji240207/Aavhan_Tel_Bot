from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def inline_menu():
    keyboard=[
        [
            InlineKeyboardButton("Jobs", callback_data="jobs"),
            InlineKeyboardButton("profile", callback_data="profile")
        ],
        [
            InlineKeyboardButton("Help", callback_data="help")
        ]
    ] 
    
    return InlineKeyboardMarkup(keyboard)   