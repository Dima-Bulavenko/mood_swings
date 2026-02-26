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
