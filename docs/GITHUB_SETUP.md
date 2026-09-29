# Create your GitHub repository

Use one repository for this frontend and backend: they form one application.

## Repository metadata

**Name:** `clearclause`  
**Description:** AI-powered legal document assistant that simplifies PDF agreements, highlights clauses for review, and answers document-based questions using Google Gemini and FastAPI.  
**Topics:** `generative-ai`, `gemini-api`, `fastapi`, `python`, `nlp`, `legal-tech`, `pdf`, `document-analysis`

## Easiest method: upload files

1. Sign in to GitHub and create a repository named `clearclause`.
2. Choose Public for a portfolio, or Private if you prefer.
3. Leave the initialize-with-README, .gitignore and license options unchecked: this project already provides the first two.
4. Extract `clearclause-github.zip` on your computer.
5. Open the extracted `clearclause` folder. Upload its contents, not the ZIP itself.
6. Use “uploading an existing file” / “Add file → Upload files”; commit with `Initial commit: ClearClause legal document assistant`.
7. Make sure README.md and main.py are at repository root. Include `.github`, `.gitignore`, `.dockerignore` and `.env.example`; use the Git method below if your file browser hides them.
8. Never upload your real `.env`, virtual environment, API keys or private contracts.
9. Edit repository About and add the description/topics above.
10. Wait for the Tests action and pin the repository on your GitHub profile if desired.

## Git method (recommended for all files)

Install Git, then open a terminal inside the extracted `clearclause` folder.
Create an empty GitHub repository first and replace `YOUR_USERNAME` below.

```bash
git init
git branch -M main
git add .
git status
git commit -m "Initial commit: ClearClause legal document assistant"
git remote add origin https://github.com/YOUR_USERNAME/clearclause.git
git push -u origin main
```

If Git asks for identity, configure your own name and GitHub-linked email. Authenticate
with GitHub's supported sign-in flow; do not paste passwords or tokens into project files.
Review `git status` before committing and confirm that `.env` is absent.

## Optional: GitHub CLI

If you already have `gh` installed and signed in, after the initial local commit:

```bash
gh repo create clearclause --public --source=. --remote=origin --push
```

Use `--private` instead if desired. Use this instead of manually adding the remote.

## After upload

- Capture a real screenshot after running the example; add it to the README.
- Add your confirmed competition name and year only when verified.
- Add actual collaborators with their consent.
- Do not claim features from the roadmap as implemented.
- GitHub upload is not live app hosting. Run locally or deploy the Python app separately.
