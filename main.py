"""
main.py — VIVID Desktop App
A colorful & bold daily task + notes manager.
Run: python main.py
"""

import customtkinter as ctk
import database as db

# ── THEME CONSTANTS ──────────────────────────────────────────
BG      = "#0D0D0D"
BG2     = "#161616"
BG3     = "#1E1E1E"
BORDER  = "#2A2A2A"
TEXT    = "#F0F0F0"
MUTED   = "#777777"
PINK    = "#FF3399"
CYAN    = "#00C8E0"
YELLOW  = "#D4B800"
LIME    = "#2BB84A"
ORANGE  = "#FF6B35"
PURPLE  = "#A855F7"

CAT_COLORS = {
    "Work":     PINK,
    "Personal": CYAN,
    "Creative": YELLOW,
    "Health":   LIME,
}

NOTE_COLORS = [PINK, CYAN, YELLOW, LIME, ORANGE, PURPLE]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ════════════════════════════════════════════════════════════
#  MAIN APPLICATION WINDOW
# ════════════════════════════════════════════════════════════
class VividApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        db.init_db()

        self.title("VIVID — Your Workspace")
        self.geometry("1200x740")
        self.minsize(1000, 640)
        self.configure(fg_color=BG)

        self.current_cat  = "All"   # All / Work / Personal / Creative / Health
        self.current_view = "tasks" # tasks / notes / done

        self._build_layout()
        self.refresh_all()

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda e: self.open_add_dialog())
        self.bind("<Escape>",    lambda e: self.focus())

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidePanel(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = MainPanel(self)
        self.main.grid(row=0, column=1, sticky="nsew")

    def refresh_all(self):
        self.sidebar.refresh()
        self.main.refresh()

    def switch_view(self, view, cat=None):
        if cat is not None:
            self.current_cat = cat
        self.current_view = view
        self.main.update_tabs()
        self.refresh_all()

    def open_add_dialog(self):
        AddDialog(self)


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
class SidePanel(ctk.CTkFrame):
    def __init__(self, app: VividApp):
        super().__init__(app, width=270, fg_color=BG2, corner_radius=0)
        self.app = app
        self.grid_propagate(False)
        self.count_labels: dict[str, ctk.CTkLabel] = {}
        self._build()

    def _build(self):
        # ── Logo ──
        logo_row = ctk.CTkFrame(self, fg_color="transparent")
        logo_row.pack(fill="x", padx=22, pady=(26, 0))
        ctk.CTkLabel(
            logo_row, text="⬤ VIVID",
            font=ctk.CTkFont("Helvetica", 26, "bold"),
            text_color=TEXT
        ).pack(side="left")

        self._divider()

        # ── Navigation ──
        self._section("WORKSPACE")
        self._nav_btn("📋   All Tasks",  lambda: self.app.switch_view("tasks", "All"))
        self._nav_btn("📝   Notes",      lambda: self.app.switch_view("notes"))
        self._nav_btn("✅   Completed",  lambda: self.app.switch_view("done"))

        self._divider()

        # ── Categories ──
        self._section("CATEGORIES")
        self._cat_row("All", "#FFFFFF")
        for cat, color in CAT_COLORS.items():
            self._cat_row(cat, color)

        self._divider()

        # ── Progress stats (bottom) ──
        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x", padx=22, pady=16)

        self.prog_label = ctk.CTkLabel(
            stats, text="Progress  —  0 / 0",
            font=ctk.CTkFont("Helvetica", 12),
            text_color=MUTED, anchor="w"
        )
        self.prog_label.pack(fill="x", pady=(0, 6))

        self.prog_bar = ctk.CTkProgressBar(
            stats, progress_color=PINK,
            fg_color=BG3, height=5, corner_radius=4
        )
        self.prog_bar.set(0)
        self.prog_bar.pack(fill="x")

    # helpers
    def _divider(self):
        ctk.CTkFrame(self, height=1, fg_color=BORDER).pack(fill="x", pady=10)

    def _section(self, text):
        ctk.CTkLabel(
            self, text=text,
            font=ctk.CTkFont("Helvetica", 10, "bold"),
            text_color=MUTED
        ).pack(anchor="w", padx=22, pady=(0, 3))

    def _nav_btn(self, text, cmd):
        ctk.CTkButton(
            self, text=text, anchor="w", height=40,
            fg_color="transparent", hover_color=BG3,
            text_color=MUTED, font=ctk.CTkFont("Helvetica", 14),
            command=cmd, corner_radius=8
        ).pack(fill="x", padx=10, pady=1)

    def _cat_row(self, cat, color):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=1)

        ctk.CTkLabel(
            row, text="⬤", text_color=color,
            font=ctk.CTkFont("Helvetica", 9), width=24
        ).pack(side="left", padx=(10, 2))

        ctk.CTkButton(
            row, text=cat, anchor="w", height=34,
            fg_color="transparent", hover_color=BG3,
            text_color=MUTED, font=ctk.CTkFont("Helvetica", 13),
            command=lambda c=cat: self.app.switch_view("tasks", c),
            corner_radius=6
        ).pack(side="left", fill="x", expand=True)

        lbl = ctk.CTkLabel(
            row, text="0", width=32,
            font=ctk.CTkFont("Helvetica", 11),
            text_color=MUTED, fg_color=BG3, corner_radius=8
        )
        lbl.pack(side="right", padx=6)
        self.count_labels[cat] = lbl

    def refresh(self):
        total, done = db.get_stats()
        pct = done / total if total else 0
        self.prog_bar.set(pct)
        self.prog_label.configure(text=f"Progress  —  {done} / {total}")

        all_tasks = db.get_tasks()
        active = [t for t in all_tasks if not t[3]]

        if "All" in self.count_labels:
            self.count_labels["All"].configure(text=str(len(active)))
        for cat in CAT_COLORS:
            cnt = len([t for t in active if t[2] == cat])
            if cat in self.count_labels:
                self.count_labels[cat].configure(text=str(cnt))


# ════════════════════════════════════════════════════════════
#  MAIN PANEL
# ════════════════════════════════════════════════════════════
class MainPanel(ctk.CTkFrame):
    def __init__(self, app: VividApp):
        super().__init__(app, fg_color=BG, corner_radius=0)
        self.app = app
        self._build()

    def _build(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Top bar ──
        top = ctk.CTkFrame(self, fg_color=BG2, corner_radius=0, height=72)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        top.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            top, text="Hey, let's get things done. ✦",
            font=ctk.CTkFont("Helvetica", 20, "bold"),
            text_color=TEXT
        ).grid(row=0, column=0, padx=28, sticky="w")

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *_: self.refresh())
        ctk.CTkEntry(
            top, placeholder_text="🔍  Search...",
            width=210, height=38,
            fg_color=BG3, border_color=BORDER,
            text_color=TEXT, placeholder_text_color=MUTED,
            font=ctk.CTkFont("Helvetica", 13),
            textvariable=self.search_var
        ).grid(row=0, column=1, padx=12, sticky="e")

        ctk.CTkButton(
            top, text="＋  New",
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            fg_color=PINK, hover_color="#CC1177",
            height=38, width=110, corner_radius=10,
            command=self.app.open_add_dialog
        ).grid(row=0, column=2, padx=(0, 24))

        # ── Tabs ──
        tabs = ctk.CTkFrame(self, fg_color=BG, corner_radius=0, height=50)
        tabs.grid(row=1, column=0, sticky="ew")

        self.btn_tasks = ctk.CTkButton(
            tabs, text="Tasks",
            font=ctk.CTkFont("Helvetica", 14, "bold"),
            fg_color=PINK, hover_color="#CC1177",
            height=34, width=100, corner_radius=8,
            command=lambda: self.app.switch_view("tasks")
        )
        self.btn_tasks.pack(side="left", padx=(24, 6), pady=8)

        self.btn_notes = ctk.CTkButton(
            tabs, text="Notes",
            font=ctk.CTkFont("Helvetica", 14, "bold"),
            fg_color=BG3, hover_color=BORDER, text_color=MUTED,
            height=34, width=100, corner_radius=8,
            command=lambda: self.app.switch_view("notes")
        )
        self.btn_notes.pack(side="left", pady=8)

        ctk.CTkFrame(self, height=1, fg_color=BORDER).grid(row=1, column=0, sticky="ews")

        # ── Scrollable content ──
        self.content = ctk.CTkScrollableFrame(
            self, fg_color=BG2, corner_radius=0,
            scrollbar_button_color=BG3,
            scrollbar_button_hover_color=BORDER
        )
        self.content.grid(row=2, column=0, sticky="nsew")

    def update_tabs(self):
        view = self.app.current_view
        is_task_view = view in ("tasks", "done")

        self.btn_tasks.configure(
            fg_color=PINK if is_task_view else BG3,
            text_color=TEXT if is_task_view else MUTED,
            hover_color="#CC1177" if is_task_view else BORDER
        )
        self.btn_notes.configure(
            fg_color=PINK if not is_task_view else BG3,
            text_color=TEXT if not is_task_view else MUTED,
            hover_color="#CC1177" if not is_task_view else BORDER
        )

    def refresh(self):
        for w in self.content.winfo_children():
            w.destroy()

        view  = self.app.current_view
        query = self.search_var.get().strip().lower()

        if view == "notes":
            self._render_notes(query)
        elif view == "done":
            self._render_tasks(query, only_done=True)
        else:
            self._render_tasks(query)

    # ── Tasks ──
    def _render_tasks(self, query="", only_done=False):
        cat = self.app.current_cat
        tasks = db.get_tasks(None if cat == "All" else cat)

        if only_done:
            tasks = [t for t in tasks if t[3]]
        if query:
            tasks = [t for t in tasks if query in t[1].lower()]

        active = [t for t in tasks if not t[3]]
        done   = [t for t in tasks if t[3]]

        if not tasks:
            self._empty("🎯", "No tasks found.\nHit  ＋ New  or  Ctrl+N  to add one.")
            return

        if active and not only_done:
            self._section_label("ACTIVE")
            for t in active:
                TaskRow(self.content, t, self.app).pack(
                    fill="x", padx=22, pady=4
                )

        if done:
            self._section_label("COMPLETED" if not only_done else "COMPLETED TASKS")
            for t in done:
                TaskRow(self.content, t, self.app).pack(
                    fill="x", padx=22, pady=4
                )

    # ── Notes ──
    def _render_notes(self, query=""):
        notes = db.get_notes()
        if query:
            notes = [n for n in notes
                     if query in n[1].lower() or query in (n[2] or "").lower()]

        if not notes:
            self._empty("🗒️", "No notes yet.\nHit  ＋ New  or  Ctrl+N  to add one.")
            return

        cols = 3
        for i, note in enumerate(notes):
            if i % cols == 0:
                row_frame = ctk.CTkFrame(self.content, fg_color="transparent")
                row_frame.pack(fill="x", padx=22, pady=6)
            NoteCard(row_frame, note, self.app).pack(
                side="left", fill="both", expand=True, padx=5
            )

    # ── Helpers ──
    def _section_label(self, text):
        ctk.CTkLabel(
            self.content, text=text,
            font=ctk.CTkFont("Helvetica", 10, "bold"),
            text_color=MUTED, anchor="w"
        ).pack(fill="x", padx=26, pady=(16, 2))

    def _empty(self, icon, msg):
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.pack(expand=True, pady=80)
        ctk.CTkLabel(frame, text=icon,
                     font=ctk.CTkFont("Helvetica", 48)).pack()
        ctk.CTkLabel(frame, text=msg, text_color=MUTED,
                     font=ctk.CTkFont("Helvetica", 14),
                     justify="center").pack(pady=12)


# ════════════════════════════════════════════════════════════
#  TASK ROW WIDGET
# ════════════════════════════════════════════════════════════
class TaskRow(ctk.CTkFrame):
    """Single task row: accent bar | checkbox | text | tag | delete"""

    def __init__(self, parent, task: tuple, app: VividApp):
        super().__init__(parent, fg_color=BG3, corner_radius=12, height=54)
        self.task = task   # (id, text, category, done, created_at)
        self.app  = app
        self.pack_propagate(False)
        self._build()

    def _build(self):
        tid, text, cat, done, _ = self.task
        color = CAT_COLORS.get(cat, PINK)
        is_done = bool(done)

        # Colored left accent bar
        ctk.CTkFrame(
            self, width=4,
            fg_color=color if not is_done else MUTED,
            corner_radius=3
        ).pack(side="left", fill="y", padx=(8, 0), pady=8)

        # Checkbox
        var = ctk.BooleanVar(value=is_done)
        ctk.CTkCheckBox(
            self, variable=var, text="",
            checkbox_width=22, checkbox_height=22,
            checkmark_color=BG, fg_color=color,
            border_color="#555", hover_color=color,
            command=lambda: (db.toggle_task(tid), self.app.refresh_all()),
            width=36
        ).pack(side="left", padx=10)

        # Task text
        ctk.CTkLabel(
            self, text=text,
            font=ctk.CTkFont("Helvetica", 14,
                              slant="italic" if is_done else "roman"),
            text_color=MUTED if is_done else TEXT,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # Delete button
        ctk.CTkButton(
            self, text="✕", width=30, height=30,
            fg_color="transparent", hover_color="#3A0D0D",
            text_color="#555", font=ctk.CTkFont("Helvetica", 13),
            corner_radius=6,
            command=lambda: (db.delete_task(tid), self.app.refresh_all())
        ).pack(side="right", padx=10)

        # Category tag [MODIFIED TO FIX TclError]
        ctk.CTkLabel(
            self, text=f"  {cat}  ",
            font=ctk.CTkFont("Helvetica", 11, "bold"),
            text_color=color,
            fg_color=BG, # Changed from color + "30" to BG to avoid invalid color name error
            corner_radius=6, height=26
        ).pack(side="right", padx=4)


# ════════════════════════════════════════════════════════════
#  NOTE CARD WIDGET
# ════════════════════════════════════════════════════════════
class NoteCard(ctk.CTkFrame):
    """Colored note card with title, body, date, delete."""

    def __init__(self, parent, note: tuple, app: VividApp):
        nid, title, body, color, date = note
        # NOTE: If this card also throws a TclError, change fg_color to color or BG3
        super().__init__(
            parent,
            fg_color=BG3, # Changed for stability
            border_color=color,
            border_width=1,
            corner_radius=14
        )
        self.note = note
        self.app  = app
        self._build()

    def _build(self):
        nid, title, body, color, date = self.note

        # Title
        ctk.CTkLabel(
            self, text=title,
            font=ctk.CTkFont("Helvetica", 15, "bold"),
            text_color=color, anchor="w", wraplength=185
        ).pack(fill="x", padx=16, pady=(16, 6))

        # Body text
        ctk.CTkLabel(
            self, text=body or "",
            font=ctk.CTkFont("Helvetica", 12),
            text_color="#CCCCCC",
            anchor="nw", justify="left", wraplength=185
        ).pack(fill="x", padx=16, pady=(0, 12))

        # Footer row
        foot = ctk.CTkFrame(self, fg_color="transparent")
        foot.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkLabel(
            foot, text=date,
            font=ctk.CTkFont("Helvetica", 11),
            text_color="#555"
        ).pack(side="left")

        ctk.CTkButton(
            foot, text="✕", width=28, height=28,
            fg_color="transparent", hover_color="#3A0D0D",
            text_color="#555", font=ctk.CTkFont("Helvetica", 12),
            corner_radius=6,
            command=lambda: (db.delete_note(nid), self.app.refresh_all())
        ).pack(side="right")


# ════════════════════════════════════════════════════════════
#  ADD DIALOG
# ════════════════════════════════════════════════════════════
class AddDialog(ctk.CTkToplevel):
    def __init__(self, app: VividApp):
        super().__init__(app)
        self.app   = app
        self.itype = "task"                 # "task" or "note"
        self.note_color = NOTE_COLORS[0]

        self.title("New Item")
        self.geometry("480x510")
        self.resizable(False, False)
        self.configure(fg_color=BG2)
        self.grab_set()
        self.focus()
        self.lift()

        self._build()
        self.inp_title.focus()

    def _build(self):
        pad = dict(padx=28)

        # Heading
        ctk.CTkLabel(
            self, text="New Item",
            font=ctk.CTkFont("Helvetica", 22, "bold"),
            text_color=TEXT
        ).pack(anchor="w", pady=(26, 14), **pad)

        # Type toggle
        toggle = ctk.CTkFrame(self, fg_color=BG3, corner_radius=10)
        toggle.pack(fill="x", pady=(0, 14), **pad)

        self.btn_type_task = ctk.CTkButton(
            toggle, text="Task",
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            fg_color=PINK, hover_color="#CC1177",
            height=38, corner_radius=8,
            command=lambda: self._set_type("task")
        )
        self.btn_type_task.pack(side="left", fill="x", expand=True, padx=4, pady=4)

        self.btn_type_note = ctk.CTkButton(
            toggle, text="Note",
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            fg_color="transparent", hover_color=BORDER, text_color=MUTED,
            height=38, corner_radius=8,
            command=lambda: self._set_type("note")
        )
        self.btn_type_note.pack(side="right", fill="x", expand=True, padx=(0, 4), pady=4)

        # Title input
        ctk.CTkLabel(self, text="TITLE",
                     font=ctk.CTkFont("Helvetica", 10, "bold"),
                     text_color=MUTED).pack(anchor="w", **pad)
        self.inp_title = ctk.CTkEntry(
            self, placeholder_text="What's on your mind?",
            height=42, fg_color=BG3, border_color=BORDER,
            text_color=TEXT, font=ctk.CTkFont("Helvetica", 14),
            placeholder_text_color=MUTED
        )
        self.inp_title.pack(fill="x", pady=(4, 14), **pad)
        self.inp_title.bind("<Return>", lambda e: self._save())

        # ── Task: category select ──
        self.frm_cat = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_cat.pack(fill="x", **pad)
        ctk.CTkLabel(self.frm_cat, text="CATEGORY",
                     font=ctk.CTkFont("Helvetica", 10, "bold"),
                     text_color=MUTED).pack(anchor="w")
        self.inp_cat = ctk.CTkComboBox(
            self.frm_cat, values=list(CAT_COLORS.keys()),
            height=42, fg_color=BG3, border_color=BORDER,
            text_color=TEXT, button_color=BORDER,
            dropdown_fg_color=BG3, dropdown_text_color=TEXT,
            font=ctk.CTkFont("Helvetica", 14)
        )
        self.inp_cat.set("Work")
        self.inp_cat.pack(fill="x", pady=(4, 0))

        # ── Note: body textarea ──
        self.frm_body = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(self.frm_body, text="CONTENT",
                     font=ctk.CTkFont("Helvetica", 10, "bold"),
                     text_color=MUTED).pack(anchor="w")
        self.inp_body = ctk.CTkTextbox(
            self.frm_body, height=90,
            fg_color=BG3, border_color=BORDER, border_width=1,
            text_color=TEXT, font=ctk.CTkFont("Helvetica", 13),
            wrap="word"
        )
        self.inp_body.pack(fill="x", pady=(4, 0))

        # ── Note: color swatches ──
        self.frm_color = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(self.frm_color, text="COLOR",
                     font=ctk.CTkFont("Helvetica", 10, "bold"),
                     text_color=MUTED).pack(anchor="w")
        swatch_row = ctk.CTkFrame(self.frm_color, fg_color="transparent")
        swatch_row.pack(anchor="w", pady=(6, 0))

        self.swatch_btns: list[ctk.CTkButton] = []
        for i, col in enumerate(NOTE_COLORS):
            btn = ctk.CTkButton(
                swatch_row, text="", width=32, height=32,
                fg_color=col, hover_color=col, corner_radius=8,
                border_width=3 if i == 0 else 0,
                border_color=TEXT,
                command=lambda c=col, idx=i: self._pick_color(c, idx)
            )
            btn.pack(side="left", padx=4)
            self.swatch_btns.append(btn)

        # Action buttons (pinned to bottom)
        act = ctk.CTkFrame(self, fg_color="transparent")
        act.pack(fill="x", side="bottom", pady=(10, 24), **pad)

        ctk.CTkButton(
            act, text="Cancel",
            font=ctk.CTkFont("Helvetica", 14),
            fg_color=BG3, hover_color=BORDER, text_color=MUTED,
            height=44, corner_radius=10,
            command=self.destroy
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            act, text="Save  →",
            font=ctk.CTkFont("Helvetica", 14, "bold"),
            fg_color=PINK, hover_color="#CC1177",
            height=44, corner_radius=10,
            command=self._save
        ).pack(side="right", fill="x", expand=True)

    def _set_type(self, t: str):
        self.itype = t
        self.btn_type_task.configure(
            fg_color=PINK if t == "task" else "transparent",
            text_color=TEXT if t == "task" else MUTED
        )
        self.btn_type_note.configure(
            fg_color=PINK if t == "note" else "transparent",
            text_color=TEXT if t == "note" else MUTED
        )
        if t == "task":
            self.frm_body.pack_forget()
            self.frm_color.pack_forget()
            self.frm_cat.pack(fill="x", padx=28)
        else:
            self.frm_cat.pack_forget()
            self.frm_body.pack(fill="x", padx=28)
            self.frm_color.pack(fill="x", padx=28, pady=(10, 0))

    def _pick_color(self, color: str, idx: int):
        self.note_color = color
        for i, btn in enumerate(self.swatch_btns):
            btn.configure(border_width=3 if i == idx else 0)

    def _save(self):
        title = self.inp_title.get().strip()
        if not title:
            self.inp_title.focus()
            return

        if self.itype == "task":
            db.add_task(title, self.inp_cat.get())
        else:
            body = self.inp_body.get("1.0", "end").strip()
            db.add_note(title, body, self.note_color)

        self.app.refresh_all()
        self.destroy()


# ════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = VividApp()
    app.mainloop()