 VIVID — Your Daily Workspace
A colorful & bold desktop productivity app built with Python. Manage your tasks and notes with a stunning dark UI — all data saved locally.

✨ Features

📋 Tasks — Add, complete, and delete tasks with color-coded categories
📝 Notes — Colorful sticky-note style cards
🏷️ Categories — Work, Personal, Creative, Health
🔍 Live Search — Filter tasks and notes in real-time
📊 Progress Bar — See how much you've completed
💾 Auto Save — SQLite database, data never lost
⌨️ Keyboard Shortcuts — Ctrl+N new item, Esc close

🚀 Setup & Run
1. Clone the repo
bashgit clone https://github.com/jonayed23-ui/todolist.git
cd todolist
2. Create virtual environment
bash# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bashpip install customtkinter Pillow
4. Run the app
bashpython main.py

🗂️ Project Structure
vivid-app/
│
├── main.py          # Main app UI (CustomTkinter)
├── database.py      # SQLite CRUD operations
├── requirements.txt # Dependencies
└── data/
    └── vivid.db     # Auto-created on first run

🎨 Tech Stack
ToolPurposePython 3.10+Core languageCustomTkinterModern dark UISQLite3Local databasePillowImage support

⌨️ Keyboard Shortcuts
KeyActionCtrl + NNew task or noteEnterSave in dialogEscClose dialog

👤 Author
Jonayed — @jonayed23-ui
