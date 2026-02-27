# Setup with `uv`

If you have never used `uv` before, follow these steps.

## 1) Install `uv`

Install using the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Check installation:

```bash
uv --version
```

## 2) Install project dependencies with `uv`

This project backend uses `pyproject.toml` in `backend/`.

```bash
cd backend
uv sync
```

`uv sync` creates a local virtual environment and installs all dependencies from `pyproject.toml`.

## 3) Activate `.venv`

After `uv sync`, activate the virtual environment:

Linux/macOS (bash/zsh):

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

## 4) Run FastAPI server

From `backend/` (with `.venv` activated), start the dev server:

```bash
uv run fastapi dev
```

Then open: `http://127.0.0.1:8000`  
API docs: `http://127.0.0.1:8000/docs`

## Team Git Flow (Simple)

### Roles
- **Developer**: works in a feature branch, opens PR, fixes requested changes.
- **Reviewer**: reviews PR and approves (at least 1 teammate).

### Step-by-step
1. **Sync base branch**
	```bash
	git checkout main
	git pull origin main
	```

2. **Create feature branch** (never code on `main`)
	```bash
	git checkout -b feature/header-fix
	```

3. **Code + commit often** (small save points)
	```bash
	git add .
	git commit -m "feat: fix header layout"
	```

4. **Daily sync with `main`** (avoid big conflicts)
	```bash
	git checkout main
	git pull origin main
	git checkout feature/header-fix
	git merge main
	```

5. **Push and open PR**
	```bash
	git push -u origin feature/header-fix
	```
	Then open a Pull Request to `main`.

6. **Review and refine**
	- Reviewer leaves comments.
	- Developer commits fixes to the same feature branch.

7. **Merge and delete branch**
	- After approval, merge PR into `main`.
	- Delete the feature branch (remote + local).

### If two people edit the same file
- **First merged branch wins**: their code is already in `main`.
- **Second branch gets a merge conflict** during sync/merge with `main`.
- **Fix**: open the conflicted file, choose the correct lines (or combine both), save, then complete merge and commit.

**Rule**: the person who gets the conflict resolves it. If unclear, do a quick call with the teammate who changed the other version.
