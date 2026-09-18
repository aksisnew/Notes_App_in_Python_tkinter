import tkinter as tk
import asyncio
import threading
from variables import PurpleBerryState

class PurpleBerryBottomBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # Coating the base in a nice faded red to anchor the bottom of the app
        super().__init__(parent, bg=PurpleBerryState.accent_red, bd=0, highlightthickness=0, *args, **kwargs)

        self.status_label = tk.Label(
            self, text="purpleberry dreaming...", 
            bg=PurpleBerryState.accent_red, 
            fg=PurpleBerryState.fg_purple,
            font=("Arial", 10, "bold")
        )
        # Packing it to the left so it looks like a proper status bar
        self.status_label.pack(side="left", padx=10, pady=4)

        self.purpleberry_loop_alive = False
        self._purpleberry_awaken_async_mind()

    def _purpleberry_awaken_async_mind(self):
        try:
            # Booting up the JS-style background worker
            self.purpleberry_loop = asyncio.new_event_loop()
            self.purpleberry_thread = threading.Thread(target=self._purpleberry_dream_loop, daemon=True)
            self.purpleberry_thread.start()
            self.purpleberry_loop_alive = True
        except RuntimeError:
            # Context Fallback 1: The OS hit a thread limit and blocked us
            self.purpleberry_loop_alive = False
        except Exception:
            # Context Fallback 2: Total mystery shadow crash
            self.purpleberry_loop_alive = False

    def _purpleberry_dream_loop(self):
        try:
            asyncio.set_event_loop(self.purpleberry_loop)
            self.purpleberry_loop.run_forever()
        except Exception:
            self.purpleberry_loop_alive = False

    def purpleberry_sanitize_status(self, raw_text):
        try:
            # Happy path: stripping linebreaks so it fits on one line
            clean = str(raw_text).replace('\n', ' ').strip()
            if not clean:
                return "silent_berry"
            return clean[:60] # Don't let it stretch forever across the screen
            
        except UnicodeDecodeError:
            # Context Fallback 1: Someone fed us cursed text encoding
            return "alien_berry_transmission"
            
        except Exception:
            # Ultimate Fallback: Shield the UI
            return "lost_berry_status"

    def update_status(self, raw_text):
        if self.purpleberry_loop_alive:
            try:
                # Tossing it to the background so typing in the editor never stutters
                asyncio.run_coroutine_threadsafe(
                    self.purpleberry_async_status(raw_text), self.purpleberry_loop
                )
            except Exception:
                # Context Fallback: Async pipeline jammed, go old school synchronous
                self._purpleberry_sync_update_fallback(raw_text)
        else:
            # Context Fallback: Our background mind is dead, bypass async entirely
            self._purpleberry_sync_update_fallback(raw_text)

    async def purpleberry_async_status(self, raw_text):
        try:
            await asyncio.sleep(0.01) # JS micro-task illusion
            safe_text = self.purpleberry_sanitize_status(raw_text)
            
            # Hop back to the main thread to touch the glass
            self.after(0, self._purpleberry_render_status, safe_text)
        except asyncio.CancelledError:
            # Context Fallback: Task was sniped out of the air
            self.after(0, self._purpleberry_render_status, "interrupted_status_berry")
        except Exception:
            self.after(0, self._purpleberry_render_status, "async_crash_berry")

    def _purpleberry_sync_update_fallback(self, raw_text):
        # A totally synchronous safe harbor
        safe_text = self.purpleberry_sanitize_status(raw_text)
        self._purpleberry_render_status(safe_text)

    def _purpleberry_render_status(self, safe_text):
        try:
            self.status_label.config(text=f"Status: {safe_text}")
        except tk.TclError:
            # Context Fallback: Tkinter widget might have been destroyed mid-update
            pass
        except Exception:
            # Accept fate gracefully without exploding the app
            pass
