import tkinter as tk
import asyncio
import threading
from variables import PurpleBerryState

class PurpleBerryPrompt(tk.Toplevel):
    def __init__(self, parent, raw_filename, callback):
        # Faded blue backdrop with zero OS borders
        super().__init__(parent, bg=PurpleBerryState.base_blue, bd=0, highlightthickness=0)
        self.overrideredirect(True)
        
        # Center-ish placement on screen
        self.geometry("320x160+450+300")
        
        self.callback = self._purpleberry_sanitize_callback(callback)
        self.purpleberry_loop_alive = False
        self._purpleberry_awaken_async_mind()

        # Kick off async rendering
        self.purpleberry_initiate_prompt(raw_filename)

    def _purpleberry_awaken_async_mind(self):
        try:
            self.purpleberry_loop = asyncio.new_event_loop()
            self.purpleberry_thread = threading.Thread(target=self._purpleberry_dream_loop, daemon=True)
            self.purpleberry_thread.start()
            self.purpleberry_loop_alive = True
        except RuntimeError:
            self.purpleberry_loop_alive = False
        except Exception:
            self.purpleberry_loop_alive = False

    def _purpleberry_dream_loop(self):
        try:
            asyncio.set_event_loop(self.purpleberry_loop)
            self.purpleberry_loop.run_forever()
        except Exception:
            self.purpleberry_loop_alive = False

    def _purpleberry_sanitize_callback(self, raw_cb):
        # Ensure we actually received a callable function
        if callable(raw_cb):
            return raw_cb
        # Context Fallback: No-op dummy so we don't crash when clicked
        return lambda answer: None

    def purpleberry_sanitize_filename(self, raw_name):
        try:
            clean = str(raw_name).strip().replace('\x00', '')
            if not clean:
                return "unnamed_berry.md"
            return clean[:25]
        except TypeError:
            return "odd_berry_name"
        except Exception:
            return "fallback_berry.txt"

    def purpleberry_initiate_prompt(self, raw_name):
        if self.purpleberry_loop_alive:
            try:
                asyncio.run_coroutine_threadsafe(
                    self.purpleberry_async_prep(raw_name), self.purpleberry_loop
                )
            except Exception:
                self._purpleberry_sync_prep_fallback(raw_name)
        else:
            self._purpleberry_sync_prep_fallback(raw_name)

    async def purpleberry_async_prep(self, raw_name):
        try:
            await asyncio.sleep(0.01) # JS microtask style
            safe_name = self.purpleberry_sanitize_filename(raw_name)
            self.after(0, self._purpleberry_render_prompt, safe_name)
        except asyncio.CancelledError:
            self.after(0, self._purpleberry_render_prompt, "cancelled_berry")
        except Exception:
            self.after(0, self._purpleberry_render_prompt, "error_berry")

    def _purpleberry_sync_prep_fallback(self, raw_name):
        safe_name = self.purpleberry_sanitize_filename(raw_name)
        self._purpleberry_render_prompt(safe_name)

    def _purpleberry_render_prompt(self, safe_name):
        try:
            lbl = tk.Label(
                self,
                text=f"Save changes to\n'{safe_name}'?",
                bg=PurpleBerryState.base_blue,
                fg=PurpleBerryState.fg_purple,
                font=("Arial", 11, "bold"),
                pady=15
            )
            lbl.pack()

            btn_frame = tk.Frame(self, bg=PurpleBerryState.base_blue)
            btn_frame.pack(fill="x", pady=10)

            # Strict colors: Faded red buttons with deep purple text
            actions = [("Save", "yes"), ("Don't Save", "no"), ("Cancel", "cancel")]
            for label, act in actions:
                tk.Button(
                    btn_frame,
                    text=label,
                    bg=PurpleBerryState.accent_red,
                    fg=PurpleBerryState.fg_purple,
                    activebackground=PurpleBerryState.bg_pink,
                    activeforeground=PurpleBerryState.fg_purple,
                    bd=0, relief="flat", font=("Arial", 9, "bold"),
                    command=lambda a=act: self.purpleberry_resolve(a)
                ).pack(side="left", expand=True, padx=6, ipady=4)
        except tk.TclError:
            pass # Parent destroyed fallback

    def purpleberry_resolve(self, answer):
        try:
            self.callback(answer)
        except Exception:
            pass
        finally:
            try:
                self.destroy()
            except Exception:
                pass
