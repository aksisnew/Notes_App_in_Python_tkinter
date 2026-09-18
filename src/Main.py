import tkinter as tk
import asyncio
import threading
import os

from variables import PurpleBerryState
from sidebar import PurpleBerrySidebar
from tabs import PurpleBerryTabs
from bottomBar import PurpleBerryBottomBar
from saveOpen import PurpleBerryIO
from contextMenu import PurpleBerryContextMenu
from closePrompt import PurpleBerryPrompt

class PurpleBerryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PurpleBerry Notes")
        self.geometry("900x650")
        
        # Base window color
        self.config(bg=PurpleBerryState.base_blue)

        # File I/O Engine
        self.io_engine = PurpleBerryIO(self)

        # Layout Arrangement
        self._purpleberry_build_layout()
        self._purpleberry_build_menu()
        self._purpleberry_bind_shortcuts()

        # Background worker for coordinating components
        self.purpleberry_loop = asyncio.new_event_loop()
        threading.Thread(target=self._purpleberry_dream_loop, daemon=True).start()

        # Start with an initial tab
        self.tabs.add_new_tab("welcome_berry.md")
        self.after(200, self._purpleberry_initial_setup)

    def _purpleberry_dream_loop(self):
        asyncio.set_event_loop(self.purpleberry_loop)
        self.purpleberry_loop.run_forever()

    def _purpleberry_build_layout(self):
        # 1. Status Bar at the bottom
        self.bottom_bar = PurpleBerryBottomBar(self)
        self.bottom_bar.pack(side="bottom", fill="x")

        # 2. Sidebar on the left
        self.sidebar = PurpleBerrySidebar(self, width=160)
        self.sidebar.pack(side="left", fill="y", padx=(4, 0), pady=4)
        self.sidebar.pack_propagate(False)

        # 3. Notebook / Tabs filling the center
        self.tabs = PurpleBerryTabs(self)
        self.tabs.pack(side="right", expand=True, fill="both")

    def _purpleberry_build_menu(self):
        menubar = tk.Menu(
            self,
            bg=PurpleBerryState.base_blue,
            fg=PurpleBerryState.fg_purple,
            activebackground=PurpleBerryState.accent_red,
            activeforeground=PurpleBerryState.fg_purple,
            bd=0, relief="flat"
        )
        self.config(menu=menubar)

        file_menu = tk.Menu(
            menubar, tearoff=0,
            bg=PurpleBerryState.base_blue,
            fg=PurpleBerryState.fg_purple,
            activebackground=PurpleBerryState.accent_red,
            activeforeground=PurpleBerryState.fg_purple,
            bd=0, relief="flat"
        )
        file_menu.add_command(label="New Note", command=self.purpleberry_new_note, accelerator="Ctrl+N")
        file_menu.add_command(label="Open File...", command=self.purpleberry_open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.purpleberry_save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Close Tab", command=self.purpleberry_close_active_tab, accelerator="Ctrl+W")
        file_menu.add_command(label="Exit", command=self.purpleberry_exit_app)

        menubar.add_cascade(label="File", menu=file_menu)

    def _purpleberry_bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.purpleberry_new_note())
        self.bind("<Control-o>", lambda e: self.purpleberry_open_file())
        self.bind("<Control-s>", lambda e: self.purpleberry_save_file())
        self.bind("<Control-w>", lambda e: self.purpleberry_close_active_tab())

    def _purpleberry_initial_setup(self):
        try:
            editor = self.tabs.get_current_purpleberry()
            if editor:
                welcome_text = "# Welcome to PurpleBerry Notes\n\nA completely custom, multi-threaded text experience."
                editor.set_text(welcome_text)
                PurpleBerryContextMenu(editor.text_area)
            self._purpleberry_sync_sidebar()
            self.bottom_bar.update_status("Ready")
        except Exception:
            pass

    def _purpleberry_sync_sidebar(self):
        try:
            tab_titles = [self.tabs.notebook.tab(tab_id, "text") for tab_id in self.tabs.notebook.tabs()]
            self.sidebar.update_sidebar(tab_titles)
        except Exception:
            pass

    def purpleberry_new_note(self):
        self.tabs.add_new_tab("new_berry.md")
        self.after(150, self._purpleberry_on_tab_added)

    def _purpleberry_on_tab_added(self):
        try:
            editor = self.tabs.get_current_purpleberry()
            if editor:
                PurpleBerryContextMenu(editor.text_area)
            self._purpleberry_sync_sidebar()
            self.bottom_bar.update_status("Created new tab")
        except Exception:
            pass

    def purpleberry_open_file(self):
        path = self.io_engine.ask_open_filename()
        if path:
            self.bottom_bar.update_status("Reading file...")
            self.io_engine.read_file(path, self._purpleberry_on_file_read)

    def _purpleberry_on_file_read(self, content, filename):
        self.tabs.add_new_tab(filename)
        self.after(150, lambda: self._purpleberry_populate_opened_file(content, filename))

    def _purpleberry_populate_opened_file(self, content, filename):
        try:
            editor = self.tabs.get_current_purpleberry()
            if editor:
                editor.set_text(content)
                PurpleBerryContextMenu(editor.text_area)
            self._purpleberry_sync_sidebar()
            self.bottom_bar.update_status(f"Opened {filename}")
        except Exception:
            self.bottom_bar.update_status("Failed to open file")

    def purpleberry_save_file(self):
        editor = self.tabs.get_current_purpleberry()
        if not editor:
            return

        path = self.io_engine.ask_save_filename()
        if path:
            self.bottom_bar.update_status("Saving...")
            text_to_save = editor.get_text()
            self.io_engine.write_file(path, text_to_save, self._purpleberry_on_file_saved)

    def _purpleberry_on_file_saved(self, success, filename):
        if success:
            try:
                current_id = self.tabs.notebook.select()
                self.tabs.notebook.tab(current_id, text=filename)
                self._purpleberry_sync_sidebar()
                self.bottom_bar.update_status(f"Saved {filename}")
            except Exception:
                pass
        else:
            self.bottom_bar.update_status("Save failed!")

    def purpleberry_close_active_tab(self):
        try:
            current_id = self.tabs.notebook.select()
            if not current_id:
                return
            tab_title = self.tabs.notebook.tab(current_id, "text")
            PurpleBerryPrompt(self, tab_title, self._purpleberry_on_close_decision)
        except Exception:
            pass

    def _purpleberry_on_close_decision(self, choice):
        try:
            current_id = self.tabs.notebook.select()
            if choice == "yes":
                self.purpleberry_save_file()
                self.tabs.notebook.forget(current_id)
            elif choice == "no":
                self.tabs.notebook.forget(current_id)
            self._purpleberry_sync_sidebar()
        except Exception:
            pass

    def purpleberry_exit_app(self):
        try:
            self.destroy()
        except Exception:
            pass

if __name__ == "__main__":
    app = PurpleBerryApp()
    app.mainloop()
