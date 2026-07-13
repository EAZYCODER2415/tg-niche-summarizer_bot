# Contributing to SMU Niche Summarizer 🦁

Thanks for wanting to contribute and congratulations for getting Collaborator access! This project is built by students, for students — no prior open-source experience needed. This guide will walk you through everything from setup to submitting your first change.

## Getting Started

1. **Clone** your fork locally:
   ```bash
   git clone https://github.com/EAZYCODER2415/tg-niche-summarizer_bot.git
   cd PROJECT-NAME
   ```
   **OR** just run it on a **Codespace**
2. **Set up a virtual environment** (keeps dependencies isolated):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
    ```
    pip install python-telegram-bot --upgrade [INSTALL telegram py library]
    export TELEGRAM_BOT_TOKEN="[INSERT_TOKEN_HERE]"
    python bot.py 
    ```
    **Additions**:
    - `TELEGRAM_BOT_TOKEN` — get this from [@BotFather](https://t.me/BotFather)
    - Your LLM API key (Claude, Qwen, etc.)
5. **Run it locally:**
   ```bash
   python bot.py
   ```

## Project Structure

```
bot.py              # Telegram handlers (commands, message logging)
db.py               # SQLite storage layer (log/retrieve messages)
summarizer.py       # LLM API handler (prompts, e.t.c)
requirements.txt    # Python dependencies
README.md           # Project overview
CONTRIBUTING.md     # You are here
package.json        # Handles Commitizen configuration and dependencies
package-lock.json   # Handles dependencies' versioning
```

- Telegram-related changes (commands, event handling) → `bot.py`
- Storage/query changes → `db.py`
- LLM/prompt work → will live in a new `summarizer.py` (see [open issues](https://github.com/EAZYCODER2415/tg-niche-summarizer_bot/issues))

## How to Claim Work

1. Check the **Issues** tab for something tagged with your role (`bot-dev`, `prompt-eng`, `devops`, `docs`, `qa`, etc.) or labeled `good first issue`
2. Comment on the issue saying you're picking it up — this avoids two people duplicating work
3. If you have an idea that isn't already an issue, open one first and describe it before starting work, so we can discuss approach

## Making Changes

1. Create a new branch off `main`, named for what you're doing:
   ```bash
   git checkout -b feature/short-description
   ```
   (e.g. `feature/sqlite-time-filter`, `fix/summarize-empty-buffer`)
2. Make your changes, testing locally before committing
3. Write clear commit messages:
   ```bash
   git commit -m "Add time-window filtering to /summarize command"
   ```
   Explain *what* changed and briefly *why* — not just "fixed stuff"
4. Push your branch:
   ```bash
   git push origin feature/short-description
   ```

## Submitting a Pull Request

1. Open a PR from your branch into this repo's `main` branch
2. In the description, include:
   - What the change does
   - Which issue it addresses (e.g. "Closes #12")
   - How you tested it (even just "ran locally in a test group chat")
3. Wait for a review — a maintainer may ask for small changes before merging. This is normal and not a rejection of your work.
4. Once approved, a maintainer merges it in

## Code Style

- Follow existing formatting in the file you're editing
- Use clear variable/function names over clever short ones
- Add a comment for anything non-obvious (especially async/await behavior, which trips up beginners)
- Don't worry about being perfect — reviewers are here to help polish, not gatekeep

## Non-Coding Contributions

Docs, QA/testing, and UX/prompt-format feedback are just as valuable as code:
- **Docs:** edit `.md` files directly, same PR process as code
- **QA:** file an issue describing the bug, steps to reproduce, and what you expected instead
- **UX/format feedback:** comment on the relevant issue or open a new one with example outputs you'd want to see

## Questions?

Ask in **SMU niche telegram gc** — no question is too basic. Everyone here is learning this together.