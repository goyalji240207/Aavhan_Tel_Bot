# 🕉️ Aavhan - Priest Booking Telegram Bot

A production-grade Telegram Bot designed to seamlessly connect Yajmans (Hosts) with verified Priests (Pandits) for religious ceremonies and pujas. Built with Python, MongoDB, and the `python-telegram-bot` framework.

---

## ✨ Features

### 🧑‍⚖️ For Priests (Users)
- **KYC Verification:** Automated flow to capture Name, Phone Number, and ID/Document proof.
- **Job Broadcasting:** Instantly receive new Puja Aavhans (job requests) via dynamically generated, beautifully designed image cards.
- **One-Click Actions:** Accept, Reject, or Re-apply to jobs directly from the Telegram chat.
- **Smart Scheduling:** Built-in conflict detection prevents double-booking a priest within a 3-hour window.
- **Automated Reminders:** Get notified 24 hours, 2 hours, and 1 hour before a scheduled Puja.
- **Job Management:** 
  - `/jobs` - View available open jobs.
  - `/applied` - View confirmed/assigned bookings (Green theme).
  - `/rejected` - View previously rejected jobs (Muted Gray theme) with an option to re-apply.
  - `/history` - View your past successfully completed jobs.

### 👑 For Admins
- **Secure Access:** Dedicated `/admin_jobs` panel restricted entirely to the configured `ADMIN_ID`.
- **Verification Management:** Approve or reject KYC documents submitted by new priests.
- **Broadcast Messaging:** Send custom text announcements to all verified priests using `/broadcast <message>`.
- **Job Dashboard:** 
  - 📬 View all **Open** jobs.
  - ✅ View **Booked** jobs and instantly see which priest is assigned.
  - ❌ View **Rejected** jobs and see the list of priests who declined.
  - 🎉 View **Completed** jobs and review finished pujas.

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Framework:** `python-telegram-bot` (v20+)
- **Web Server:** `FastAPI` & `Uvicorn` (for handling Webhooks)
- **Database:** MongoDB (using `motor` for async I/O)
- **Image Processing:** `Pillow` (PIL) for on-the-fly generation of rich Pujan Invitation cards.

---

## 📂 Project Structure

```text
app/
├── db/
│   └── mongo.py           # MongoDB connection and collections setup
├── handlers/
│   ├── admin.py           # User approval/rejection handlers
│   ├── auth.py            # Registration & KYC conversation
│   ├── help.py            # Dynamic help menus
│   ├── job_actions.py     # Apply, Reject, Cancel, Re-apply logic
│   ├── jobs.py            # User job listing commands
│   └── start.py           # Entry point and Keyboard generation
├── services/
│   ├── admin_jobs.py      # Admin-only dashboard logic
│   ├── broadcast.py       # Pushing new jobs to verified priests
│   ├── conflict_service.py# Time-overlap prevention logic
│   ├── image_service.py   # Dynamic invitation card generation
│   ├── job_service.py     # Database queries for jobs
│   └── user_service.py    # Database queries for users
├── middleware/
│   └── auth.py            # Verification checks
├── routes/
│   └── webhook.py         # FastAPI webhook endpoints
├── watchers/
│   ├── job_watcher.py     # MongoDB change stream watcher for auto-broadcasts
│   └── reminder_watcher.py# Background task for upcoming job reminders
└── bot.py                 # Application builder and route registration
config.py                  # Environment variables manager
main.py                    # FastAPI application entry point
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.9 or higher
- A running instance of MongoDB (Local or Atlas)
- A Telegram Bot Token (from @BotFather)

### 2. Clone and Install

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root of the project and add the following keys:

```ini
# .env
BOT_TOKEN=your_telegram_bot_token_here
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
ADMIN_ID=your_personal_telegram_user_id
```

### 4. Run the Bot

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
*(Note: Ensure your `main.py` imports and runs the `create_bot()` function from `app.bot`)*

---
