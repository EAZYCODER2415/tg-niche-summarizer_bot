# 🦁 SMU Niche Summarizer (prototype in progress)
⭐ Star this repo if you find it useful ⭐

**Repository Owner:** Pongsavaruth Vorajayudhbong

## 💡 Introduction

How many times have you opened a Telegram group chat to 200 unread pings and just given up? And what's more, felt pressured to catch up on whatever the group is discussing or plotting?

This project aims to ease **FOMO, burnout, isolation, and information overload** for incoming university students. It's a Python-based Telegram bot that summarizes conversations in seconds using LLM processing.

It started as a personal project for a small SMU (Singapore Management University) group chat, and doubles as a first experiment with the `python-telegram-bot` API and LLM APIs in Python.

## 🛠️ Tech Stack

**Language:**
- ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
- ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)

**APIs:**
- python-telegram-bot
- Claude or Qwen

**Pipeline:** Telegram → LLM → Telegram

## ✨ Key Features
*Subject to change — currently under discussion.*

| Feature | Options |
|---|---|
| 🔔 **Trigger** | Command-based (user types the `/summarize` command), or Activity-based (auto-triggers after 50+ unread messages) |
| 📋 **Format** | TL;DR — 3 to 5 bullet points covering major decisions, deadlines, or topics |
| 🔒 **Privacy & scope** | By default, summarizes text only — media, files, and links are excluded. Messages with attachments are included only if tagged `#summarize` |

| Attachment type | Handling |
|---|---|
| 🖼️ **Images** (png, jpg, jpeg) | Compressed before being sent to the LLM API |
| 📄 **Documents** (pdf, docx, etc.) | Filename only, content omitted |
| 🎬 **Audio/video** (mp3, mp4, etc.) | Not yet decided |

*(Based on poll results and suggestions among collaborators.)*

## ⚙️ Usage
The bot mainly runs on **TWO** commands:
1. `/start` → shows an intro and usage guide.
2. `/summarize` → the core command. Takes **TWO** parameters:

    - `time` &ensp;→ hours to look back (max 72)
    - `topic` → a string in quotation marks

**Automatic logging:** the bot also runs `/summarize` on itself once a set number of new messages (e.g. 50) have piled up since the last summary.

## 🤝 Get Involved
This is an open-collaboration project — built by students, for students, as a space to actually learn Python, bots, and LLM integration by doing.

To join, message [@StealrunNshoot](https://t.me/StealrunNshoot) on Telegram with:
1. Your GitHub username
2. Your preferred role(s)
3. A sentence or two on what you want to get out of contributing

No formal application, no gatekeeping on experience — but you should be able to explain your own code. PRs that are clearly copy-pasted without understanding won't be taken seriously.

### Roles

*All coding roles: you should genuinely understand every line you submit, including AI-assisted code — "it works" isn't a substitute for being able to explain it.*

| Role | Responsibilities | Requirements |
|---|---|---|
| 🎨 **Bot Aesthetic Designer** | Profile picture, icons, welcome page, overall look | Anyone with an eye for design |
| 🛠️ **Bot Developer** | Python handlers for Telegram events (commands, message logging) | Basic Python (loops, functions) |
| 🧠 **LLM/Prompt Engineer** | Design and test prompts that turn chat logs into good summaries | Curiosity about AI/LLMs — no ML background needed, but you should understand *why* a prompt works |
| 🛢️ **Database Helper** | Database queries for storing/retrieving messages | Basic Python; SQL is a bonus |
| ⚙️ **DevOps** | Hosting, environment variables/secrets, basic CI, crash restarts | Comfortable with the command line; deployment guides provided |
| 🖌️ **UX/Format Designer** | Decide how summaries should read, test real outputs | Good judgment and meaningful feedback |
| 📝 **Docs & Onboarding** | Improve the README, setup guides, code comments | Good english, readability and basic formatting knowledge |
| 🧪 **QA/Tester** | Run the bot in a real chat, find and file bugs | Patience and attention to detail |
| 🔎 **Reviewer** | Read pull requests, give feedback before merging | Understands basic Python |

### How to Contribute

**Prerequisite**: Have Collaborator access to the repository after position inquiry

See [CONTRIBUTING.md](https://github.com/EAZYCODER2415/tg-niche-summarizer_bot/blob/main/CONTRIBUTING.md) for full setup instructions, coding conventions, and contribution guidelines.

<details>
  <summary><b>Not sure where to start?</b></summary>
  
  Message [@StealrunNshoot](https://t.me/StealrunNshoot) on Telegram and we'll help you get started and clarify any doubts you may have.
</details>

## 📈 Current Work Plan

1. Configure the bot: API setup, event calls, message parameters.
2. Build the LLM pipeline for summarizing text and media by time/topic.
3. Connect the two into one pipeline: Telegram → LLM → Telegram.
4. Testing, QA, and revision (longest phase).
5. Web/server hosting (final step).

## 📌 Conclusion

Thanks for checking out this repo! Again, do support us by starring the repository. Looking forward to your contributions!