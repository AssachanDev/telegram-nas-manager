<div align="center">

# telegram-nas-manager

A private NAS file management bot for Telegram — upload, browse, search, and organize files directly from your phone.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://github.com/aiogram/aiogram)
[![License](https://img.shields.io/badge/License-MIT-6B7280?style=flat-square)](LICENSE)

</div>

---

## Overview

`telegram-nas-manager` is a Telegram bot that acts as a file manager for a self-hosted NAS (Network Attached Storage). Instead of using a web dashboard or SSH, you interact with your storage directly through Telegram — uploading files, browsing folders, searching by name, and monitoring disk health — all from a mobile-friendly interface.

Built with Python and [aiogram v3](https://github.com/aiogram/aiogram). Designed to run as a persistent systemd service.

---

## Features

- **File Upload** — Send any file type (up to 50 MB); the bot detects its category and suggests the correct folder. Navigate the full directory tree to choose a custom destination.
- **File Browser** — Browse NAS contents by category with pagination, file size, and last-modified timestamps.
- **Full-text Search** — Recursive filename search across the entire NAS via `/find`. Supports pagination for large result sets.
- **Folder Management** — Create new directories or move existing ones to trash via an interactive inline menu.
- **Storage Monitor** — Real-time disk usage with a visual progress bar and health indicator.
- **Safe Deletion** — Files and folders are moved to `.trash/` with a timestamp prefix, never deleted immediately.
- **Rate Limiting** — Built-in cooldown on write operations to protect the NAS from rapid successive requests.
- **Access Control** — Whitelist-based authorization. Unauthorized users are blocked at every entry point.
- **Path Traversal Protection** — All file paths are validated to stay within the NAS root directory.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12+ |
| Bot Framework | [aiogram](https://github.com/aiogram/aiogram) v3 |
| Concurrency | asyncio |
| Filesystem | pathlib, shutil |
| API | [Telegram Bot API](https://core.telegram.org/bots/api) (official) |

---

## Project Structure

```
telegram-nas-manager/
├── main.py              # Entry point — router registration and startup
├── config.py            # Environment loading, validation, and authorization
├── requirements.txt     # Python dependencies
├── handlers/
│   ├── commands.py      # /start, /space, and keyboard button handlers
│   ├── files.py         # File upload flow and folder selection
│   ├── search.py        # Category browser, pagination, /find, file actions
│   └── folders.py       # Folder Manager — create and delete wizards
└── utils/
    └── storage.py       # Disk usage, path validation, sanitization, rate limiting
```

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/AssachanDev/telegram-nas-manager.git
cd telegram-nas-manager

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `ALLOWED_USER_ID` | Comma-separated list of authorized Telegram user IDs (get yours from [@userinfobot](https://t.me/userinfobot)) |
| `NAS_PATH` | Absolute path to the NAS root directory (must exist and be writable) |

### 3. Run

```bash
python main.py
```

---

## Running as a Service

To run the bot automatically on boot as a systemd service:

**`/etc/systemd/system/telegram-nas-manager.service`**

```ini
[Unit]
Description=Telegram NAS Manager Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram-nas-manager
ExecStart=/path/to/telegram-nas-manager/venv/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-nas-manager.service
sudo systemctl start telegram-nas-manager.service

# View logs
sudo journalctl -u telegram-nas-manager.service -f
```

---

## Usage

The bot uses a persistent **Reply Keyboard** — no need to type commands manually.

```
[ 🔍 Browse ]  [ 🔎 Find    ]
[ 📂 Folders ] [ 📊 Storage ]
```

| Button / Command | Description |
|---|---|
| Browse / `/search` | Browse NAS categories with pagination |
| Find / `/find [name]` | Search files by name across the entire NAS |
| Folders / `/mkdir` | Open Folder Manager — create or delete directories |
| Storage / `/space` | View disk usage and health status |
| _(send any file)_ | Start the upload flow — select destination folder |

---

## File Categories

The bot auto-suggests a destination folder based on the file extension:

| Category | Extensions |
|---|---|
| Documents | `.pdf` `.docx` `.xlsx` `.txt` `.pptx` `.md` |
| Media | `.png` `.jpg` `.jpeg` `.mp4` `.mov` `.gif` `.mp3` `.wav` `.mkv` |
| Data | `.csv` `.json` `.sql` `.xml` `.yaml` `.yml` |
| Scripts | `.py` `.sh` `.js` `.ts` `.go` `.c` `.cpp` |
| Archives | `.zip` `.tar` `.gz` `.7z` `.rar` |
| Other | _(everything else)_ |

---

## Trash & Recovery

Deleted files and folders are moved to `.trash/` inside `NAS_PATH` with a Unix timestamp prefix — never permanently removed immediately.

```
/mnt/nas/.trash/
├── 1711900000_report.pdf
└── 1711900050_old-project/
```

To recover, move the file back to its original location via SSH or a file manager. The `.trash/` folder is not auto-purged.

---

## Troubleshooting

**`Bad Request: can't parse entities`**
The bot uses HTML parse mode. If modifying message text manually, ensure `<`, `>`, and `&` are properly escaped. Filenames are handled automatically.

**Files not saving to NAS**
Verify the user running the bot has write permissions on `NAS_PATH`:
```bash
touch /mnt/nas/test_file && rm /mnt/nas/test_file
```

**File too large to upload**
The standard Telegram Bot API supports files up to 50 MB. Files exceeding this limit will be rejected by Telegram before reaching the bot.

**Bot not responding**
Check that your Telegram user ID is correctly set in `ALLOWED_USER_ID`. Get your ID from [@userinfobot](https://t.me/userinfobot).

---

## License

[MIT](LICENSE)
