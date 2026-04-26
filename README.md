# VIVID — Your Daily Workspace

A colorful & bold desktop task + notes manager built with Python & CustomTkinter.

---

## A to Z Setup (VS Code)

### Step 1 — Prerequisites install karo

Python 3.10 or higher lagbe.
Download: https://www.python.org/downloads/

VS Code download: https://code.visualstudio.com/

---

### Step 2 — Project folder create karo

VS Code open koro, then:
  File → Open Folder → New Folder banao name "vivid-app" → Select Folder

---

### Step 3 — Files copy karo

Ei 3ta file "vivid-app" folder-e rakho:
  - main.py
  - database.py
  - requirements.txt

---

### Step 4 — VS Code Terminal open koro

  View → Terminal   (অথবা Ctrl + `)

---

### Step 5 — Virtual environment create karo

Windows:
  python -m venv venv
  venv\Scripts\activate

Mac/Linux:
  python3 -m venv venv
  source venv/bin/activate

Terminal-e (venv) দেখা গেলে বুঝবে activate হয়েছে।

---

### Step 6 — Dependencies install karo

  pip install -r requirements.txt

---

### Step 7 — App run karo

  python main.py

---

## Features

- Tasks — add, complete, delete with color-coded categories
- Notes — colorful sticky-note cards
- Categories — Work, Personal, Creative, Health
- Search — real-time filter
- Sidebar progress bar
- SQLite database — data saves automatically
- Keyboard shortcuts: Ctrl+N = new item, Esc = close dialog

## Shortcuts

| Key     | Action        |
|---------|---------------|
| Ctrl+N  | New item      |
| Esc     | Close dialog  |
| Enter   | Save (in dialog) |
