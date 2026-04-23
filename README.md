# 🕉️ Aavhan - Priest Booking Telegram Bot

A production-grade Telegram Bot designed to seamlessly connect Yajmans (Hosts) with verified Priests (Pandits) for religious ceremonies and pujas. Built with Python, MongoDB, and the `python-telegram-bot` framework.

---

## ✨ Features

### 🧑‍⚖️ For Priests (Users)
- **KYC Verification:** Automated flow to capture Name, Phone Number, and ID/Document proof.
- **Job Broadcasting:** Instantly receive new Puja Aavhans (job requests) via dynamically generated, beautifully designed image cards.
- **One-Click Actions:** Accept, Reject, or Re-apply to jobs directly from the Telegram chat.
- **Smart Scheduling:** Built-in conflict detection prevents double-booking a priest within a 3-hour window.
- **Job Management:** 
  - `/jobs` - View available open jobs.
  - `/applied` - View confirmed/assigned bookings (Green theme).
  - `/rejected` - View previously rejected jobs (Muted Gray theme) with an option to re-apply.

### 👑 For Admins
- **Secure Access:** Dedicated `/admin_jobs` panel restricted entirely to the configured `ADMIN_ID`.
- **Verification Management:** Approve or reject KYC documents submitted by new priests.
- **Job Dashboard:** 
  - 📬 View all **Open** jobs.
  - ✅ View **Booked** jobs and instantly see which priest is assigned.
  - ❌ View **Rejected** jobs and see the list of priests who declined.

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Framework:** `python-telegram-bot` (v20+)
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
└── bot.py                 # Application builder and route registration
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
python main.py
```
*(Note: Ensure your `main.py` imports and runs the `create_bot()` function from `app.bot`)*

---

## 🛡️ Production Deployment Recommendations

1. **Process Manager:** Use `systemd` or `PM2` to keep the bot running in the background and automatically restart on crashes.
2. **Containerization:** For easier scaling, wrap the application in a `Dockerfile`.
3. **Fonts:** Ensure the host machine has standard fonts installed (`timesbd.ttf`, `arial.ttf`, or `DejaVuSans.ttf`) so the `Pillow` image generator can render text properly.
4. **Webhooks:** Consider switching from long-polling to Webhooks for better performance under heavy load.
