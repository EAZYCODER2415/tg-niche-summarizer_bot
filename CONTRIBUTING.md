# 🤖 Contributing to TLDRFlow

Thanks for wanting to contribute and congratulations for getting Collaborator access! No prior open-source experience needed. This guide will walk you through everything from setup to submitting your first change.

## 🚀 Getting Started

Pick whichever setup path works for you as both get you to the same place.

<details>
  <summary><b>🖥️ Local setup</b></summary>
  
  1. **Clone** your fork locally:

     ```bash
     git clone https://github.com/EAZYCODER2415/tg-niche-summarizer_bot.git
     cd tg-niche-summarizer_bot
     ```

  2. **Set up a virtual environment** (keeps dependencies isolated):

     ```bash
     python -m venv venv
     source venv/bin/activate      # Windows: venv\Scripts\activate
     ```

  3. **Install dependencies:**

     ```bash
     pip install -r requirements.txt
     ```

</details>

<details>
  <summary><b>☁️ Codespace setup</b></summary>
  
  1. On the repo page, click **Code → Codespaces → Create codespace on main**
  2. Once it opens, install dependencies the same way you would locally — there's no devcontainer config yet, so nothing installs automatically:

     ```bash
     pip install -r requirements.txt
     ```

  3. A virtual environment is optional here (the Codespace container is already isolated per-user), but you can still create one as follows if you prefer:

     ```bash
     python -m venv venv
     source venv/bin/activate      # Windows: venv\Scripts\activate
     ```

</details><br>

## 🗂️ Project Structure

```
.github/
  pull_request_template.md   # Auto-filled template when you open a PR
.env                     # Local secrets (TELEGRAM_BOT_TOKEN, LLM API key)
.gitignore               # Excludes certain files and folders from commits
bot.py                   # Telegram handlers (commands, event handling)
CONTRIBUTING.md          # You are here 📍
db.py                    # Database storage layer (storage/query changes)
imgStorage.py            # Image storage helper library (image database query)
package.json             # Handles Commitizen configuration and dependencies
package-lock.json        # Handles dependencies' versioning
README.md                # Project overview
requirements.txt         # Python dependencies
summarizer.py            # LLM API handler (prompts, etc.)
system_instruction.txt   # Core system prompt for the /tldr command.
```

## ✊ How to Claim Work

1. Check the **Issues** tab for something tagged with your role (`bot-dev`, `prompt-eng`, `devops`, `docs`, `qa`, etc.) or labeled `good first issue`.
2. To avoid duplicate work, comment under the issue you wish to claim:

```
   I want to work on this issue.
```

3. If you have an idea that isn't already an issue, **Issues** → **New issue** and follow the guidelines.

## 🎨 Style Guide
 
- Follow existing formatting in the file you're editing.
- Use clear and meaningful variable/function names over clever short ones
- Add a comment for anything non-obvious (especially async/await behavior, which trips up beginners)
- Don't worry about being perfect — reviewers are here to help polish, not gatekeep

### Setting up Commitizen
 
We use `commitizen` combined with `cz-emoji` to standardise our commit messages with clear visual formatting via emojis. It'll walk you through what to write, so you don't need to memorize a format.
 
1. Install both `commitizen` and `cz-emoji` locally as devDependencies:

```bash
   npm install --save-dev commitizen cz-emoji
```

2. Install `commitizen` globally to get the CLI command:

```bash
   npm install -g commitizen
```

## ✍️ Making Changes

1. Create a new branch off `main`, named `type/short-title`:
   | Type | Use for |
   |---|---|
   | ✨ `feat` | a new feature or capability |
   | 🐛 `fix` | a bug fix |
   | ♻️ `refactor` | restructuring code with no behavior change |
   | 📖 `docs` | documentation-only changes |
   | 🔧 `config` | tooling, dependency, or config changes |

```bash
   git checkout -b type/short-title
```

   > Example branch names:
   > - `feat/sqlite-database-optimisation`
   > - `fix/time-limit-bug`
   > - `docs/contributing-rewrite`)
 
2. Make your changes, testing locally before committing.
3. **Commit** with:

```bash
   git cz
```

> A few pointers on the interactive commit:
> - Reference the `type` from your branch name `type/short-title` for:
>
> ```bash
>    ? Select the type of change you are committing:
>    ? Specify a scope:
> ```
>
> - Short description should mention briefly what you did in what file.
> - You may skip the long description by pressing `Enter`

4. Push your branch:

```bash
   git push origin type/short-title
```

## 📩 Submitting a Pull Request

1. Open a PR from your branch into this repo's `main` branch.

```
   base: main  ←  compare: type/short-title
```

2. Set **PR title** to your **branch name**, and follow the guidelines embedded in the PR description.
3. Wait for a review — the reviewers may take a while to respond depending on their availability. Kindly refrain from spamming pings and be assured that your PR will be reviewed.

> [!NOTE]
> The code review cycle is an iterative process. Do not be discouraged by the back-and-forth communication loop and requested changes.

4. Once approved, choose "Rebase and merge".
5. Once merged, you may optionally safely delete your branch.

## 🔀 Merge Conflicts
 
If `main` has moved on since you branched, rebase instead of merging — it keeps history linear and makes PRs easier to review:
 
```bash
git fetch origin
git rebase origin/main
```

Fix them in the flagged files, then:

```bash
git add <resolved-files>
git rebase --continue
```

Since rebasing rewrites your branch's history, push with:

```bash
git push --force-with-lease origin type/short-title
```

(`--force-with-lease` is safer than `--force` — it refuses to overwrite work if someone else pushed to your branch in the meantime.)

## 🧩 Non-Coding Contributions

Docs, QA/testing, and UX/prompt-format feedback are just as valuable:
- **Docs:** edit `.md` files in a new branch, same PR process as code.
- **QA:** file an issue describing the bug, steps to reproduce, and what you expected instead.
- **UX/format feedback:** comment on the relevant issue or open a new one with example outputs you'd want to see.

## ❓ Questions?

Ask [@StealrunNshoot](https://t.me/StealrunNshoot) on Telegram — no question is too basic. Everyone here is learning this together.
