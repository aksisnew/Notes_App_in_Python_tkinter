import tkinter as tk
import asyncio
import threading
from variables import PurpleBerryState

class PurpleBerryContextMenu:
    def __init__(self, parent_widget):
        self.parent = parent_widget
        
        # Crafting the menu with strictly allowed colors. No default system black/white allowed.
        self.purpleberry_menu = tk.Menu(
            self.parent, tearoff=0,
            bg=PurpleBerryState.base_blue, 
            fg=PurpleBerryState.fg_purple,
            activebackground=PurpleBerryState.accent_red, 
            activeforeground=PurpleBerryState.fg_purple,
            bd=0, relief="flat", font=("Arial", 10, "bold")
        )
        
        self.purpleberry_menu.add_command(label="Cut", command=lambda: self.purpleberry_delegate_action("<<Cut>>"))
        self.purpleberry_menu.add_command(label="Copy", command=lambda: self.purpleberry_delegate_action("<<Copy>>"))
        self.purpleberry_menu.add_command(label="Paste", command=lambda: self.purpleberry_delegate_action("<<Paste>>"))
        self.purpleberry_menu.add_separator()
        self.purpleberry_menu.add_command(label="Select All", command=lambda: self.purpleberry_delegate_action("<<SelectAll>>"))

        # Bind for Mac (Button-2) and Windows/Linux (Button-3)
        self.parent.bind("<Button-2>", self.purpleberry_summon)
        self.parent.bind("<Button-3>", self.purpleberry_summon)

        self.purpleberry_loop_alive = False
        self._purpleberry_awaken_async_mind()

    def _purpleberry_awaken_async_mind(self):
        try:
            # Spinning up our async worker
            self.purpleberry_loop = asyncio.new_event_loop()
            self.purpleberry_thread = threading.Thread(target=self._purpleberry_dream_loop, daemon=True)
            self.purpleberry_thread.start()
            self.purpleberry_loop_alive = True
        except RuntimeError:
            # Context Fallback 1: OS refused to give us a thread
            self.purpleberry_loop_alive = False
        except Exception:
            # Context Fallback 2: General crash
            self.purpleberry_loop_alive = False

    def _purpleberry_dream_loop(self):
        try:
            asyncio.set_event_loop(self.purpleberry_loop)
            self.purpleberry_loop.run_forever()
        except Exception:
            self.purpleberry_loop_alive = False

    def purpleberry_sanitize_action(self, raw_action):
        try:
            # Ensure the action is a valid Tkinter virtual event string
            safe_action = str(raw_action).strip()
            if safe_action in ["<<Cut>>", "<<Copy>>", "<<Paste>>", "<<SelectAll>>"]:
                return safe_action
            return "invalid_berry"
        except Exception:
            # Context Fallback: Someone passed an object instead of a string
            return "broken_berry_action"

    def purpleberry_summon(self, event):
        try:
            # Pop it up exactly where the mouse clicked
            self.purpleberry_menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            # Context Fallback 1: Tried to pop up outside the screen boundaries
            pass
        except Exception:
            # Ultimate UI Fallback: Stay silent, don't crash
            pass

    def purpleberry_delegate_action(self, raw_action):
        if self.purpleberry_loop_alive:
            try:
                # Toss to our JS-style background loop
                asyncio.run_coroutine_threadsafe(
                    self.purpleberry_async_fire(raw_action), self.purpleberry_loop
                )
            except Exception:
                # Context Fallback: Async pipe broken, do it live
                self._purpleberry_sync_fire_fallback(raw_action)
        else:
            # Context Fallback: Worker is dead, bypass async completely
            self._purpleberry_sync_fire_fallback(raw_action)

    async def purpleberry_async_fire(self, raw_action):
        try:
            await asyncio.sleep(0.01) # A little breathing room
            safe_action = self.purpleberry_sanitize_action(raw_action)
            
            if safe_action != "invalid_berry" and safe_action != "broken_berry_action":
                # Bounce back to main thread to trigger the UI event
                self.parent.after(0, lambda: self._purpleberry_execute_safely(safe_action))
        except asyncio.CancelledError:
            # Context Fallback: Task killed mid-flight
            pass
        except Exception:
            pass

    def _purpleberry_sync_fire_fallback(self, raw_action):
        safe_action = self.purpleberry_sanitize_action(raw_action)
        if safe_action not in ["invalid_berry", "broken_berry_action"]:
            self._purpleberry_execute_safely(safe_action)

    def _purpleberry_execute_safely(self, safe_action):
        try:
            # Let the editor widget handle the actual copying/pasting
            self.parent.event_generate(safe_action)
        except tk.TclError:
            # Context Fallback 1: Editor got destroyed right before we fired the event
            pass
        except Exception:
            # Ultimate UI Fallback
            pass
