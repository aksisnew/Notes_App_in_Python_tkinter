import tkinter as tk
import asyncio
import threading

class PurpleBerryEditor(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # We wrap the frame in a faded blue hug
        super().__init__(parent, bg="#a3b4e0", *args, **kwargs)
        
        # Color palette strictly enforced: Faded Red, Pink, Purple, Blue. 
        self.purpleberry_bg = "#f3d9ee"       # Faded pinkish-purple
        self.purpleberry_fg = "#3a205e"       # Deep dark purple (our rebel alternative to black)
        self.purpleberry_cursor = "#d97eb3"   # Faded red/pink cursor
        self.purpleberry_select = "#8c9ce6"   # Faded blue selection
        
        self.text_area = tk.Text(
            self,
            bg=self.purpleberry_bg,
            fg=self.purpleberry_fg,
            insertbackground=self.purpleberry_cursor,
            selectbackground=self.purpleberry_select,
            font=("Arial", 12),
            relief="flat",
            undo=True
        )
        self.text_area.pack(expand=True, fill="both", padx=2, pady=2)

        # Waking up our async multithreaded brain
        self.purpleberry_loop = asyncio.new_event_loop()
        self.purpleberry_thread = threading.Thread(
            target=self._start_purpleberry_dreaming, 
            daemon=True
        )
        self.purpleberry_thread.start()

    def _start_purpleberry_dreaming(self):
        # Keeps the async loop alive in the background
        asyncio.set_event_loop(self.purpleberry_loop)
        self.purpleberry_loop.run_forever()

    def purpleberry_sanitize_magic(self, raw_data):
        # Scrub away the gremlins like null bytes
        try:
            clean_vibes = str(raw_data).replace('\x00', '')
            return clean_vibes
        except Exception:
            return "purpleberry fallback: something spooky happened to the text"

    def get_text(self):
        try:
            raw = self.text_area.get("1.0", tk.END)
            return self.purpleberry_sanitize_magic(raw)
        except Exception:
            return "purpleberry fallback empty"

    def set_text(self, text):
        # Tossing the workload to our async worker so the UI stays buttery smooth
        asyncio.run_coroutine_threadsafe(
            self.purpleberry_async_loader(text), 
            self.purpleberry_loop
        )

    async def purpleberry_async_loader(self, text):
        try:
            # Pretend we are fetching from a slow API with await
            await asyncio.sleep(0.05) 
            clean_text = self.purpleberry_sanitize_magic(text)
            
            # Tkinter hates it when background threads touch the UI, so we ask politely via after()
            self.after(0, self._purpleberry_render_ui, clean_text)
            
        except Exception:
            self.after(0, self._purpleberry_render_ui, "purpleberry fallback: async crash landed safely")

    def _purpleberry_render_ui(self, safe_text):
        # The final stage where the magic touches the glass
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", safe_text)
