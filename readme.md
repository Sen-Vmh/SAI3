# SAI3 Project

Folder with all pdfs and documentation: 

https://bernerfachhochschule-my.sharepoint.com/:f:/g/personal/vanms1_bfh_ch/IgDEBeHHzPNfQ5gGpesbVxJGAbQAIz6g9z5DJxgAKUQXCNA?e=GTeyM9 

## 1. Installation

1. Sync the virtual environment: `uv sync`
2. Activate environment: `.venv\Scripts\activate`

### Adding Libraries

If you add new libraries to the project during development, you must update the dependencies list so other users can install them.

Use `uv add <package>` to add new dependencies, which will update the pyproject.toml file.

---

## 2. Services (Docker)

Start Chroma and Ollama:
```bash
docker compose up -d
```

Pull the required models into the Docker Ollama instance:
```bash
docker exec ollama ollama pull nomic-embed-text
docker exec ollama ollama pull llama3.2
```

Stop services:
```bash
docker compose down
```

---

## 3. Pipeline

All scripts must be run from the project root (`SAI3/`).

### PDF Processing (skip if JSONs already in `data/processed/json/`)
```bash
python src/processing/pdf_to_docling.py
```

### Chunking & Embedding
```bash
ollama pull nomic-embed-text
python src/processing/chunk_and_embed.py
```

### Run the app
```bash
streamlit run src/app.py
```


## 4. Branch Management

### The Golden Rule
Never work directly on `main`. `main` must always represent a stable, deployable version of the codebase. Create a new branch for every task.

### Branch Naming Conventions
Structure: `category/short-description` (Always lowercase, use kebab-case for the description).

**Categories:**
* `feat/`: New functionality or features (e.g., `feat/google-login`).
* `fix/`: Bug fixes (e.g., `fix/tokenizer-infinite-loop`).
* `refactor/`: Code changes that neither fix a bug nor add a feature (e.g., `refactor/pyodide-srp`).
* `chore/`: Maintenance tasks, dependencies, environment setup (e.g., `chore/project-setup`).
* `docs/`: Documentation updates (e.g., `docs/readme-setup`).
* `test/`: Adding or correcting tests (e.g., `test/pdf-parser`).

**Best Practices:**
* Keep it specific and atomic: `fix/pyodide-syntax` rather than `fix/bugs`.
* If using a ticketing system, include the ID: `feat/PROJ-123-dark-mode`.

---

## 5. Commit Standards

### The "Two Histories" Concept
1. **Work History (Local Feature Branch):** Commit early and often. These are your "save points."
2. **Project History (Main Branch):** Clean, atomic, and descriptive. Achieved via Squashing.

### The Anatomy of a Perfect Commit
* **Conventional Format:** `type(scope): description` types should be the same as all those listed in the branch section above
* **Imperative Mood:** The subject line must complete the sentence *"If applied, this commit will..."*
    * **Correct:** `fix(auth): handle empty password submission`
    * **Incorrect:** `fixed auth bug` or `fixes password`
* **Structure:**
    * Line 1: Subject (50 chars max).
    * Line 2: Blank.
    * Line 3+: Body (72 char line wrap). Explain the *why*, not the *how*.

### Atomic Commits
Every commit should do **one thing**. Do not mix unrelated changes (e.g., fixing a typo in a CSS file while writing an API endpoint). Use `git add -p` to stage specific chunks of code interactively.

---

## 6. Merging & Pull Requests (PRs)

### When to Merge
Merge only when the work is complete, tested, and code-reviewed.

### Squash and Merge
When bringing a feature branch into `main`, use **Squash and Merge**. This takes all your messy "save point" commits and condenses them into a single, cohesive commit for the project history. Use the squash commit body to detail the architectural decisions or specific sub-tasks completed.

### Keeping Branches Fresh
Avoid merge conflicts by regularly updating your feature branch with changes from `main`:
```bash
git checkout main
git pull
git checkout <your-feature-branch>
git merge main