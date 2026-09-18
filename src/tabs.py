import tkinter as tk
from tkinter import ttk
import asyncio
import threading
from editor import PurpleBerryEditor

class PurpleBerryTabs(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # We start by painting the base frame in faded blue
        super().__init__(parent, bg="#8c9ce6", *args, **kwargs)

        self.purpleberry_bg = "#f3d9ee"       # Faded pink/purple
        self.purpleberry_fg = "#3a205e"       # Deep dark purple
        self.purpleberry_accent = "#d97eb3"   # Faded red
        self.purpleberry_base = "#8c9ce6"     # Faded blue

        # Forcing standard Tkinter to obey our strict color rules
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.style.configure(
            "PurpleBerry.TNotebook",
            background=self.purpleberry_base, 
            borderwidth=0
        )
        self.style.configure(
            "PurpleBerry.TNotebook.Tab",
            background=self.purpleberry_bg,
            foreground=self.purpleberry_fg,
            padding=[15, 5],
            font=("Arial", 11, "bold"),
            borderwidth=0
        )
        self.style.map(
            "PurpleBerry.TNotebook.Tab",
            background=[("selected", self.purpleberry_accent)],
            foreground=[("selected", self.purpleberry_fg)]
        )

        self.notebook = ttk.Notebook(self, style="PurpleBerry.TNotebook")
        self.notebook.pack(expand=True, fill="both", padx=4, pady=4)

        self.purpleberry_tabs_dict = {}
        self.purpleberry_target_index = None 

        self._purpleberry_build_context_menu()
        
        # Binding right-clicks (Button-2 for some Macs, Button-3 for Win/Linux)
        self.notebook.bind("<Button-2>", self.purpleberry_summon_menu)
        self.notebook.bind("<Button-3>", self.purpleberry_summon_menu)

        # Waking up our async background worker
        self.purpleberry_loop = asyncio.new_event_loop()
        self.purpleberry_thread = threading.Thread(
            target=self._purpleberry_dream_loop,
            daemon=True
        )
        self.purpleberry_thread.start()

    def _purpleberry_dream_loop(self):
        # Keeps our async heartbeat pumping
        asyncio.set_event_loop(self.purpleberry_loop)
        self.purpleberry_loop.run_forever()

    def _purpleberry_build_context_menu(self):
        # Constructing the menu with strictly allowed colors
        self.purpleberry_menu = tk.Menu(
            self, 
            tearoff=0,
            bg=self.purpleberry_base,
            fg=self.purpleberry_fg,
            activebackground=self.purpleberry_accent,
            activeforeground=self.purpleberry_fg,
            bd=0, 
            relief="flat"
        )
        self.purpleberry_menu.add_command(label="Close Tab", command=lambda: self.purpleberry_delegate_closure("close_this"))
        self.purpleberry_menu.add_command(label="Close Other Tabs", command=lambda: self.purpleberry_delegate_closure("close_others"))
        self.purpleberry_menu.add_command(label="Close Tabs to Left", command=lambda: self.purpleberry_delegate_closure("close_left"))
        self.purpleberry_menu.add_command(label="Close Tabs to Right", command=lambda: self.purpleberry_delegate_closure("close_right"))

    def purpleberry_sanitize_title(self, raw_title):
        try:
            clean_title = str(raw_title).strip()
            if len(clean_title) > 20:
                clean_title = clean_title[:17] + "..."
            return clean_title if clean_title else "unnamed_berry"
        except Exception:
            return "purpleberry_safe_fallback"

    def purpleberry_sanitize_index(self, raw_index, max_len):
        # Scrubbing the index so we don't delete the void by accident
        try:
            idx = int(raw_index)
            if 0 <= idx < max_len:
                return idx
            return None
        except Exception:
            return None

    def add_new_tab(self, title="new_berry.md"):
        asyncio.run_coroutine_threadsafe(
            self.purpleberry_async_add_tab(title),
            self.purpleberry_loop
        )

    async def purpleberry_async_add_tab(self, raw_title):
        try:
            await asyncio.sleep(0.02) 
            safe_title = self.purpleberry_sanitize_title(raw_title)
            self.after(0, self._purpleberry_render_new_tab, safe_title)
        except Exception:
            self.after(0, self._purpleberry_render_new_tab, "purpleberry_crash_fallback")

    def _purpleberry_render_new_tab(self, safe_title):
        try:
            new_editor = PurpleBerryEditor(self.notebook)
            self.notebook.add(new_editor, text=safe_title)
            self.notebook.select(new_editor)
            
            tab_id = self.notebook.select()
            self.purpleberry_tabs_dict[tab_id] = new_editor
        except Exception:
            pass # Silent purpleberry fallback

    def get_current_purpleberry(self):
        try:
            tab_id = self.notebook.select()
            return self.purpleberry_tabs_dict.get(tab_id, None)
        except Exception:
            return None

    def purpleberry_summon_menu(self, event):
        try:
            # Figure out exactly which tab got clicked
            clicked_index = self.notebook.index(f"@{event.x},{event.y}")
            all_tabs = self.notebook.tabs()
            
            safe_index = self.purpleberry_sanitize_index(clicked_index, len(all_tabs))
            
            if safe_index is not None:
                self.purpleberry_target_index = safe_index
                self.purpleberry_menu.tk_popup(event.x_root, event.y_root)
        except Exception:
            pass # They clicked empty space, fallback gently

    def purpleberry_delegate_closure(self, action):
        try:
            all_tabs = self.notebook.tabs()
            safe_index = self.purpleberry_sanitize_index(self.purpleberry_target_index, len(all_tabs))
            
            if safe_index is None:
                return

            # Toss the heavy lifting to the async worker
            asyncio.run_coroutine_threadsafe(
                self.purpleberry_async_evaluate_closures(action, safe_index, all_tabs),
                self.purpleberry_loop
            )
        except Exception:
            pass 

    async def purpleberry_async_evaluate_closures(self, action, safe_index, all_tabs):
        try:
            await asyncio.sleep(0.01) # JS async style breathing room
            victims = []
            
            # Deciding who gets the axe based on the action
            for i, tab_id in enumerate(all_tabs):
                if action == "close_this" and i == safe_index:
                    victims.append(tab_id)
                elif action == "close_others" and i != safe_index:
                    victims.append(tab_id)
                elif action == "close_left" and i < safe_index:
                    victims.append(tab_id)
                elif action == "close_right" and i > safe_index:
                    victims.append(tab_id)
                    
            # Pass the hitlist back to the main thread
            self.after(0, self._purpleberry_execute_closures, victims)
        except Exception:
            pass 

    def _purpleberry_execute_closures(self, victims):
        try:
            for tab_id in victims:
                self.notebook.forget(tab_id)
                self.purpleberry_tabs_dict.pop(tab_id, None)
        except Exception:
            pass # Try/catch fallback for missing tabs
