# 🦁 SMU Niche Summarizer (WORK IN PROGRESS)
A Telegram bot run on Python's python-telegram-bot API that summarizes conversations based on timeframes or activity detection using ____ LLM API.

## 📰 Introduction
**Repository Owner:** Pongsavaruth Vorajayudhbong

This started out as a personal project for a small Telegram group chat for Singapore Management University (SMU) , making this the first experimentation with the Telegram's python-telegram-bot API and ____ LLM API on Python, thus, this is entirely run in Python. 

## ⭐ Key Features
The bot operates in these factors as follows (subject to change and currently under discussion):

1. ⌨️ Summarize Event Trigger
[ ] On-Demand Command: When someone types the command to trigger the summarization.
[ ] Daily Digest: An automated summary sent every evening.
[ ] Activity-Based: Whenever a massive wave of unread messages happens (e.g., 50+ new messages).

2. 📋 Formatting Style 
[ ] TL;DR Bullet Points: 3–5 quick bullet points highlighting major decisions, deadlines, or topics.
[ ] The "Narrative" Style: A short, paragraph-style story of what went down while one was gone.
[ ] Action-Items Only: Strict focus on who needs to do what, plus any upcoming dates.

3. 🔒 Privacy & Scope
[ ] Everything: Analyze all messages in the main chat to ensure nothing gets missed.
[ ] Opt-In Only: Only summarize messages that include a specific tag (like *⁠#important*⁠ or ⁠*#summary*⁠).
[ ] Exclude Media/Links: Summarize text chatter only, ignoring shared files, memes, and links.
[ ] Systemic Selection: Take messages with attachments AND with the *#summarize*

## Usage
The bot mainly runs on two functions:
- ### **/start** command:
Provides the introduction and guide to using the summarizer.

- ### **/summarize** command:
The main function of this bot, which are as follows (this is also in the **/start** command):

1. Once the command is typed, the bot will ask for a time range, in which it could be from weeks to minutes.

2. It will ask for a specific prompt asking for a topic. If there is no known topic or unspecified, type "NA". 

## Open-Source Collaboration
Currently, only invited people are allowed to collaborate on the project (ask owner for more details).
For additional information, roles are open for inquiry (reserved for SMU students only):

1. **Frontend Designer** - Design profile picture, about icon, welcome page, and overall aesthetics
2. **Telegram Backend Team** — Telegram API handlers, message buffering, event flow
3. **LLM AI Team** - LLM integration — prompt design, summarization logic, API calls
4. **DevOps** — hosting, webhook vs polling deployment, secrets management, CI
5. **Prompt/UX design** — deciding summary formatting, tone, testing outputs against real chat logs
6. **Docs & onboarding** — README, setup guide, contributing guidelines
7. **QA/testing** — running the bot in a real group chat, catching edge cases, filing issues
8. **Peer Reviewer** — no dedicated coding, just reviews PRs before merge (good role for someone less into Python but organized)

## Current Work Plan
The steps to the work plan of this project are as follows:

1. Telegram API: Configure the bot and use the API to write its code template and set event calls to send messages.
2. LLM API that computes text messages and other specific media, based on given parameters and time-based.
3. Connect both APIs together to create an agentic info transfer system (input from Telegram -> LLM summarize output -> Send its output via Telegram)!
4. Overall testing, QA, and revision cycle in debugging (LONGEST PHASE)
5. Web/Server Hosting **(FINAL DESTINATION)**

## Conclusion
Thank you for checking this repository out, have a nice day!

