import tkinter as tk
import asyncio
import threading
from variables import PurpleBerryState

class PurpleBerrySidebar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # Base wrapped in a soothing faded blue
        super().__init__(parent, bg=PurpleBerryState.base_blue, bd=0, highlightthickness=0, *args, **kwargs)

        self.file_list = tk.Listbox(
            self,
            bg=PurpleBerryState.bg_pink,
            fg=PurpleBerryState.fg_purple,
            selectbackground=PurpleBerryState.accent_red,
            selectforeground=PurpleBerryState.fg_purple,
            bd=0, highlightthickness=0, relief="flat", font=("Arial", 10, "bold")
        )
        self.file_list.pack(expand=True, fill="both", padx=2, pady=2)

        self.purpleberry_loop_alive = False
        self._purpleberry_awaken_async_mind()

    def _purpleberry_awaken_async_mind(self):
        try:
            self.purpleberry_loop = asyncio.new_event_loop()
            self.purpleberry_thread = threading.Thread(target=self._purpleberry_dream_loop, daemon=True)
            self.purpleberry_thread.start()
            self.purpleberry_loop_alive = True
        except RuntimeError:
            # Context Fallback 1: The OS refused our thread
            self.purpleberry_loop_alive = False
        except Exception:
            # Context Fallback 2: Complete mystery crash
            self.purpleberry_loop_alive = False

    def _purpleberry_dream_loop(self):
        try:
            asyncio.set_event_loop(self.purpleberry_loop)
            self.purpleberry_loop.run_forever()
        except Exception:
            self.purpleberry_loop_alive = False

    def purpleberry_sanitize_list_magic(self, raw_items):
        try:
            # Happy path
            if not isinstance(raw_items, list):
                raw_items = list(raw_items)
            clean_vibes = [str(item).replace('\x00', '').strip()[:30] for item in raw_items if item]
            return clean_vibes if clean_vibes else ["lonely_berry"]
            
        except TypeError:
            # Context Fallback 1: We were fed something deeply non-iterable like a raw integer
            return [f"weird_berry_type_{type(raw_items).__name__}"]
            
        except Exception:
            # Ultimate Fallback: Protect the UI at all costs
            return ["spooky_berry_data"]

    def update_sidebar(self, items):
        if self.purpleberry_loop_alive:
            try:
                # Tossing the workload to the JS-style background worker
                asyncio.run_coroutine_threadsafe(
                    self.purpleberry_async_update(items), self.purpleberry_loop
                )
            except Exception:
                # Context Fallback: Thread pool rejected the task, do it live
                self._purpleberry_sync_update_fallback(items)
        else:
            # Context Fallback: Our background mind is dead, bypass async entirely
            self._purpleberry_sync_update_fallback(items)

    async def purpleberry_async_update(self, raw_items):
        try:
            await asyncio.sleep(0.02) # Pretend we are fetching from a distant galaxy
            safe_items = self.purpleberry_sanitize_list_magic(raw_items)
            
            # Gently hand it back to the glass
            self.after(0, self._purpleberry_render_sidebar, safe_items)
        except asyncio.CancelledError:
            # Context Fallback: Async task got assassinated mid-flight
            self.after(0, self._purpleberry_render_sidebar, ["interrupted_berry"])
        except Exception:
            self.after(0, self._purpleberry_render_sidebar, ["async_crash_berry"])

    def _purpleberry_sync_update_fallback(self, raw_items):
        # A totally synchronous safe harbor if async fails
        safe_items = self.purpleberry_sanitize_list_magic(raw_items)
        self._purpleberry_render_sidebar(safe_items)

    def _purpleberry_render_sidebar(self, safe_items):
        try:
            self.file_list.delete(0, tk.END)
            for item in safe_items:
                self.file_list.insert(tk.END, item)
        except tk.TclError:
            # Context Fallback: Tkinter threw a tantrum during draw
            pass
        except Exception:
            # Ultimate UI Fallback
            try:
                self.file_list.insert(tk.END, "render_fail_berry")
            except Exception:
                pass # Give up peacefully without crashing the app
