# TLDRFlow 🚀🤖

<p align="left">
  <strong>An intelligent, multilingual Telegram group chat summarizer powered by LLMs via OpenRouter. Never miss a conversation context again.</strong>
</p>

<p align="left">

  ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
  ![SQLite](https://img.shields.io/badge/SQLite-4169E1?logo=sqlite&logoColor=fff&style=plastic)

</p>

---

## 📖 Overview

**TLDRFlow** is a lightweight, high-performance Telegram bot designed to solve information overload in active university, club, and project group chats. Instead of scrolling through hundreds of missed messages, users can instantly generate structured, context-aware summaries covering multi-lingual discussions (English, Chinese, Japanese, and Tamil).

---

## ✨ Key Features

- **Instant Summarization:** Summarize active conversation logs instantly on demand from slash command.
- **Multilingual Summarization:** Native support for processing and summarizing cross-lingual conversations seamlessly.
- **Smart Flat-Timeline Logging:** Captures messages, captions, and attachments into a robust SQLite backing store.
- **Private Message (PM) & Language Customization:** Configure bot preferences and interact via private chats or specific language commands (`/lang`).
- **Robust Error Handling:** Automatic fallbacks for Markdown parsing errors and built-in safety guardrail management.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** `python-telegram-bot`
- **Database:** SQLite
- **LLM Gateway:** OpenRouter (<abbr title="Application Programming Interface">API</abbr>) utilizing advanced Qwen models.

---

## 🔒 Privacy & Data Transparency

We take user privacy seriously. Please review how TLDRFlow handles data:
- **What is collected:** Group message text contents, timestamps, sender usernames, and attachment indicators are logged to maintain chronological chat flow for summarization.
- **Where it goes:** Recent message logs are processed transiently through third-party LLM providers (via OpenRouter) strictly to generate the requested summary. 
- **Storage & Retention:** Data is stored locally in an encrypted or standard SQLite instance. No message logs are monetized, sold, or shared with advertisers. Group admins retain full authority over adding or removing the bot.

---

## 🚀 Getting Started (Self-Hosting)

### Prerequisites
- Python 3.10 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- An OpenRouter API Key

### Installation

1. **Clone the repository:**
<pre><code class="language-bash">git clone https://github.com/EAZYCODER2415/tldr-bot-telegram.git
cd tldr-bot-telegram</code></pre>

2. **Install Dependencies**
<pre><code class="language-bash">pip install -r requirements.txt</code></pre>

3. **Configure Environment Variables**
<pre><code class="language-bash">TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
</code></pre>

5. **Run the Bot**
<pre><code class="language-bash">python bot.py</code></pre>

---

## 📋 Commands
- ⚡ **`/tldr`** `[hours]` `[topic (optional)]`:
Generate an instant summary within a specific timeframe (in hours, e.g., `2` or `1.5`) and optional target topic.

- 📎 **File Tagging**: Include `#summarize` in file or media captions so the bot parses them into summary data!

-⚙️ **`/config`** `[setting]`:"
Manage automatic summary settings for the chat:

• `/config topic/here` — Route automated summaries to the current topic

• `/config default` — Reset routing to default

• `/config enable` — Turn on automatic threshold summaries

• `/config disable` — Turn off automatic threshold summaries

- `/lang` — Selects preferred language for generated summaries.

- `/report` — Submits feedback or bug reports securely.

---

## 📜 License

Distributed under the MIT License. See LICENSE for more information.
