# Setup with `uv`

If you have never used `uv` before, follow these steps.

## 1) Install `uv`

Install from PyPI with `pip`:

```bash
pip install uv
```

Check installation:

```bash
uv --version
```

Upgrade later with:

```bash
pip install --upgrade uv
```

## 2) Install project dependencies with `uv`

This project backend uses `pyproject.toml` in `backend/`.

```bash
cd backend
uv sync
```

`uv sync` creates a local virtual environment and installs all dependencies from `pyproject.toml`.
