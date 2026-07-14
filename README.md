# 🦁 SMU Niche Summarizer (PROTOTYPE IN PROGRESS)
**Repository Owner:** Pongsavaruth Vorajayudhbong

## 🌟 Introduction

**How many times have you opened a Telegram group chat to 200 unread pings and just given up?** And what's more, **pressured to catch up on whatever the group is discussing or plotting on?** This project aims to alleviate feelings of **FOMO, burnout, isolation and information overload** for starting university students. This is a Telegram bot heavily run on Python that summarizes conversations within seconds using advanced LLM processing.

This started out as a personal project for a small Telegram group chat for Singapore Management University (SMU) students, making this the first experimentation with the Telegram's python-telegram-bot API and advanced LLM APIs on Python.

## 📰 Key Resources Used

### 📁 Programming Syntax 
- Python 🐍
- SQL 📊

### 📁 APIs
- python-telegram-bot 🤖
- Claude or Qwen 🤖

### Three-Stage Pipeline: 📩 Telegram -> 📠 LLM -> 📩 Telegram 

## ⭐ Key Features
The bot operates in these factors as follows (subject to change and currently under discussion):

| Feature | Sub-feature A | Sub-feature B |
|---|---|---|
| ⌨️ Summarize Event Trigger | **Command Trigger:** When someone types the command to trigger the summarization. | **Activity-Based:** Whenever a massive wave of unread messages happens (e.g., 50+ new messages). |
| 📋 Formatting Style | **TL;DR Bullet Points:** 3–5 quick bullet points highlighting major decisions, deadlines, or topics. | N/A |
| 🔒 Privacy & Scope | **All Text Messages Excluding Media/Links:** Summarize text chatter only, ignoring shared files, memes, and links as default. | **Systemic Attachment Processing:** While summarizing, take messages with attachments AND with the *#summarize* into account to answer privacy concerns. |

### Additional Remarks 🔵
- PNG/JPG/JPEG Images - Compressed to efficient size for processing by LLM API.
- PDF or Similar Documents - Content omitted, except filename.
- MP4, MP3, and Similar Files - TO BE DETERMINED.

*(This information is according to poll votes and extra suggestions from the gc)*

## ⚙️ Usage
The bot mainly runs on two functions:
- ### **/start** command:
Provides the introduction and guide to using the summarizer.

- ### **/summarize** command:
The main function of this bot, which are as follows (this is also in the **/start** command):
**Parameters**:
1. Time (measured in hours, maximum 72 hours which is 3 days)
2. Topic (string format parameter, must be enclosed in quotation marks)

- ### **Automatic Activity Logging**:
The Telegram bot will run the /summarize command on itself when it reaches a set limit of messages buffered since last summary (e.g. 50 new messages).

## 🤝 Get Involved

This is an open-collaboration project — built by students, for students. **NO** prior Git or bot-development experience needed to contribute, as we value a low-stakes development enviroment, aimed to synchronize learning with creating!!

### Roles

Pick whichever role fits your interest — no application process, fully open for inquiry. Ask away, give your Github credentials, and we will add you as a Collaborator to the repository!!

| Role | What you'd actually do | Good for |
|---|---|---|
| 🖼️ **Bot Aesthetic Designer** | Design profile picture, about icon, welcome page, and overall aesthetics | No requirements needed at all |
| 🐍 **Bot Developer** | Write Python handlers for Telegram events (commands, message logging) | Anyone comfortable with basic Python (loops, functions) |
| 🧠 **LLM/Prompt Engineer** | Design and test the prompts that turn raw chat logs into good summaries | Curiosity about AI/LLMs — no ML background needed |
| 🗄️ **Database Helper** | Work with SQLite queries for storing/retrieving messages | Basic Python; SQL is a bonus, not a requirement |
| ⚙️ **DevOps** | Get the bot running 24/7 (hosting, env vars/secrets, basic CI, restarts on crash) | Command-line comfort; no infra experience needed — mostly following deployment guides |
| 🎨 **UX / Format Designer** | Decide how summaries should read (highly effective bullet points), test real outputs | No coding required — just good judgment and feedback |
| 📝 **Docs & Onboarding** | Write/improve README, setup guides, comments in code | Great first contribution — no coding required |
| 🐛 **QA / Tester** | Run the bot in a real chat, find bugs, file clear issues | No coding required — just patience and attention to detail |
| 👀 **Reviewer** | Read others' pull requests, leave feedback before merging | Some Python reading ability, not necessarily writing |
|  👾 **null** | null | null |

### Skill Requirements

- **Required:** willingness to learn, detail-oriented code review/writing fundamental Python *(only for coding roles — Docs, QA, and UX roles need none of this)*
- **Not required:** prior bot development, prior open-source experience, Git mastery (we'll help you with your first PR)
- **Helpful but optional:** familiarity with APIs, SQL, or prompt engineering — you'll pick this up by contributing, not before

### How to Contribute

**Prerequisite**: Have Collaborator access to the repository after position inquiry

1. Either **clone** the repository locally or run it in a **Codespace**
2. Once you get to your IDE, go to Bash, type **git checkout -b feature/short-description** to start your contribution
3. Check the **Issues** tab — look for labels like `good first issue` or the role tag matching your interest
4. Comment on the issue to claim it (avoids two people doing the same thing)
5. Make your change, **git commit** your branch, then open a **Pull Request** — describe what you did and why
6. A maintainer reviews it, suggests changes if needed, and merges it in

See [CONTRIBUTING.md](https://github.com/EAZYCODER2415/tg-niche-summarizer_bot/blob/main/CONTRIBUTING.md) for full setup instructions and coding conventions.

### Not Sure Where to Start?

Message **@StealrunNshoot** on Telegram — we'll help match you to something that fits your comfort level.

## 📈 Current Work Plan
The steps to the work plan of this project are as follows:

1. Configure the bot and use the API to write its config setup, set event calls to send messages, and identify needed message parameters.
2. LLM API that computes text messages and other specific media, based on given parameters and time-based.
3. Connect both APIs together to create an agentic info transfer system (input from Telegram -> LLM summarize output -> Send its output via Telegram)!
4. Overall testing, QA, and revision cycle in debugging **(LONGEST PHASE)**
5. Web/Server Hosting **(FINAL DESTINATION)**

## :dependabot: Conclusion
Thank you for checking this repository out, have a nice day! If you are interested in contributing with the project, send me a Telegram DM **(@StealrunNshoot)** and indicate you desired position!!

