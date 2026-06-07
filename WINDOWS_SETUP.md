# Aura — Windows Setup Guide (New Device)

This guide walks you through setting up the **Aura AI Jewellery Visual Search** project on a **new Windows 10 or Windows 11** machine, from scratch to a running website at `http://localhost:8000`.

**Estimated time:** 30–60 minutes (depending on download speed and whether you need to build the search index).

---

## What You Will Install

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Runs the AI backend and scripts |
| Git | Downloads the project from GitHub |
| RingFIR dataset | ~2,605 earring images used for search |
| Python packages | TensorFlow, FAISS, FastAPI, etc. |

---

## Step 1: Check Your System

### Minimum requirements

- **OS:** Windows 10 (64-bit) or Windows 11
- **RAM:** 8 GB minimum (16 GB recommended for TensorFlow)
- **Disk space:** ~5 GB free (Python, packages, dataset, generated files)
- **Internet:** Required for first-time downloads

### Open PowerShell

1. Press `Win + X`
2. Click **Terminal** or **Windows PowerShell**
3. You will run most commands here

> **Tip:** Right-click the title bar → **Properties** → enable **QuickEdit Mode** so you can paste with right-click.

---

## Step 2: Install Python

1. Go to [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Download **Python 3.12** (or 3.10 / 3.11)
3. Run the installer
4. On the first screen, check **Add python.exe to PATH** (very important)
5. Click **Install Now**
6. When finished, close the installer

### Verify Python

In PowerShell:

```powershell
python --version
```

Expected output example:

```text
Python 3.12.x
```

If `python` is not found, close and reopen PowerShell. If it still fails, reinstall Python and ensure **Add to PATH** is checked.

Also verify `pip`:

```powershell
pip --version
```

---

## Step 3: Install Git

1. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and run the installer
3. Use the default options (Next → Next → Install)

### Verify Git

```powershell
git --version
```

---

## Step 4: Get the Project

Choose a folder for your projects, for example `C:\Projects`.

```powershell
cd C:\Projects
git clone https://github.com/kousikpramanik007-source/Aura---AI-Jewellery-Visual-Search-System.git jewllery_website
cd jewllery_website
```

If you already have the project folder (USB, zip, etc.), open PowerShell in that folder instead:

```powershell
cd C:\path\to\jewllery_website
```

---

## Step 5: Add the RingFIR Dataset

The app expects images at:

```text
data\RingFIR\
```

The dataset is **not included in the Git repository** (it is large). You must copy or download it separately.

### Expected folder layout

```text
data\
└── RingFIR\
    ├── 001\
    │   ├── 001_001.png
    │   └── ...
    ├── 002\
    └── ... (folders up to 046)
```

### How to get the dataset

- Copy `data\RingFIR` from your old machine or team storage, **or**
- Download from wherever your team stores the RingFIR files

### Verify the dataset

```powershell
dir data\RingFIR
```

You should see numbered subfolders (`001`, `002`, etc.). If the folder is missing, `generate_embeddings.py` will stop with an error.

---

## Step 6: Create a Virtual Environment

A virtual environment keeps this project's packages separate from other Python projects.

From the project root (`jewllery_website`):

```powershell
python -m venv .venv
```

### Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

When active, your prompt shows `(.venv)` at the start.

> **If you see "running scripts is disabled"**

Run this once in PowerShell (as your user), then try activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Deactivate later (optional)

```powershell
deactivate
```

---

## Step 7: Install Python Dependencies

With the virtual environment active:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs:

- `tensorflow` — EfficientNetB0 feature extraction
- `faiss-cpu` — vector similarity search
- `fastapi`, `uvicorn` — web server
- `pillow`, `numpy`, `tqdm`, etc.

**First install may take 10–20 minutes** (TensorFlow is large).

### Verify key packages

```powershell
python -c "import tensorflow; import faiss; import fastapi; print('OK')"
```

If you see `OK`, dependencies are installed.

---

## Step 8: Build the Search Index (First-Time Setup)

These files are generated locally and are not in Git:

| File | Created by |
|------|------------|
| `features.npy` | `generate_embeddings.py` |
| `image_paths.pkl` | `generate_embeddings.py` |
| `faiss_index.bin` | `build_index.py` |

If a teammate already gave you these three files, place them in the project root and **skip to Step 9**.

### 8.1 Generate embeddings

```powershell
python generate_embeddings.py
```

- Scans all images under `data\RingFIR`
- Uses EfficientNetB0 (downloads ImageNet weights on first run)
- May take **15–45 minutes** depending on your CPU/GPU

### 8.2 Build the FAISS index

```powershell
python build_index.py
```

This is usually fast (under a minute).

### Confirm output files

```powershell
dir features.npy, image_paths.pkl, faiss_index.bin
```

All three should exist.

---

## Step 9: Start the Web Application

With `.venv` still active:

```powershell
python main.py
```

You should see Uvicorn startup logs, for example:

```text
Uvicorn running on http://localhost:8000
```

### Open in your browser

Go to: **http://localhost:8000**

1. Drag and drop an earring image (or click to upload)
2. Wait a few seconds
3. View the top 10 similar designs

### Stop the server

In the same PowerShell window, press `Ctrl + C`.

---

## Step 10: Daily Use (Quick Reference)

Every time you open a **new** PowerShell window to work on this project:

```powershell
cd C:\Projects\jewllery_website
.\.venv\Scripts\Activate.ps1
python main.py
```

Then open **http://localhost:8000**.

You only need to run Steps 8.1–8.2 again if:

- The dataset changes
- `features.npy`, `image_paths.pkl`, or `faiss_index.bin` are missing or corrupted

---

## Optional: Test Search from the Command Line

```powershell
python search.py data\RingFIR\001\001_001.png
```

This prints similar images and scores without starting the web UI.

---

## Optional: Docker on Windows

If you prefer Docker instead of a local Python setup:

1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Ensure **WSL 2** backend is enabled (Docker installer usually handles this)
3. From the project folder:

```powershell
docker build -t aura-jewellery-search .
docker run -p 8000:8000 aura-jewellery-search
```

> **Note:** You still need the dataset and generated index files available inside the container (see `Dockerfile` in the repo). For most new Windows setups, the Python steps above are simpler.

---

## Troubleshooting

### `python` is not recognized

- Reinstall Python with **Add to PATH** checked
- Or use the full path, e.g. `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`

### Cannot activate `.venv` (execution policy)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### `Dataset directory 'data/RingFIR' not found`

- Create `data\RingFIR` and copy the dataset into it
- Run commands from the **project root**, not from inside `frontend\`

### `pip install` fails on TensorFlow

- Use 64-bit Python (not 32-bit)
- Upgrade pip: `python -m pip install --upgrade pip`
- Try: `pip install tensorflow --upgrade`

### `No module named 'faiss'`

```powershell
pip install faiss-cpu
```

### Port 8000 already in use

- Close other apps using port 8000, or
- Edit `main.py` and change `port=8000` to another port (e.g. `8080`)

### Search returns no results / server error on startup

- Confirm these exist: `faiss_index.bin`, `image_paths.pkl`
- Re-run `python build_index.py` and `python generate_embeddings.py` if needed

### Slow embedding generation

- Normal on CPU-only machines
- Close heavy apps to free RAM
- Do not interrupt; wait until `generate_embeddings.py` finishes

### Windows path vs Linux paths in docs

| macOS / Linux | Windows (PowerShell) |
|---------------|----------------------|
| `source .venv/bin/activate` | `.\.venv\Scripts\Activate.ps1` |
| `data/RingFIR/001/001_001.png` | `data\RingFIR\001\001_001.png` |

---

## Setup Checklist

Use this to confirm everything is ready:

- [ ] Python 3.10+ installed and `python --version` works
- [ ] Git installed (if cloning from GitHub)
- [ ] Project folder cloned or copied
- [ ] `data\RingFIR\` contains the image dataset
- [ ] Virtual environment created: `.venv`
- [ ] Virtual environment activated: `(.venv)` in prompt
- [ ] `pip install -r requirements.txt` completed without errors
- [ ] `features.npy`, `image_paths.pkl`, `faiss_index.bin` exist
- [ ] `python main.py` starts without errors
- [ ] Browser opens `http://localhost:8000` and search works

---

## Related Documentation

- [README.md](README.md) — project overview and architecture
- [documentation.md](documentation.md) — how the AI search works in plain English
- [guide.md](guide.md) — developer architecture guide

---

## Summary

| Step | Action |
|------|--------|
| 1 | Install Python (with PATH) and Git |
| 2 | Clone or copy the project |
| 3 | Place RingFIR images in `data\RingFIR\` |
| 4 | `python -m venv .venv` → activate → `pip install -r requirements.txt` |
| 5 | `python generate_embeddings.py` → `python build_index.py` |
| 6 | `python main.py` → open **http://localhost:8000** |

You are ready to use Aura on your new Windows device.
