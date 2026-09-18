import os
import asyncio
import threading
from tkinter import filedialog
from variables import PurpleBerryState

class PurpleBerryIO:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.purpleberry_loop_alive = False
        self._purpleberry_awaken_async_mind()

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

    def purpleberry_sanitize_filepath(self, raw_path):
        try:
            clean = str(raw_path).replace('\x00', '').strip()
            if os.path.exists(clean) or os.path.isdir(os.path.dirname(clean) or "."):
                return clean
            return None
        except Exception:
            return None

    def purpleberry_sanitize_content(self, raw_text):
        try:
            # Strip null bytes that crash C-based text engines
            return str(raw_text).replace('\x00', '')
        except Exception:
            return "purpleberry fallback content"

    def read_file(self, raw_path, callback):
        if self.purpleberry_loop_alive:
            try:
                asyncio.run_coroutine_threadsafe(
                    self.purpleberry_async_read(raw_path, callback), self.purpleberry_loop
                )
            except Exception:
                self._purpleberry_sync_read_fallback(raw_path, callback)
        else:
            self._purpleberry_sync_read_fallback(raw_path, callback)

    async def purpleberry_async_read(self, raw_path, callback):
        try:
            await asyncio.sleep(0.02)
            safe_path = self.purpleberry_sanitize_filepath(raw_path)
            
            if not safe_path:
                self.parent.after(0, callback, "purpleberry: invalid path", "error_berry.txt")
                return

            try:
                with open(safe_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Context Fallback 1: Not UTF-8, fall back to latin-1
                with open(safe_path, "r", encoding="latin-1") as f:
                    content = f.read()
            except PermissionError:
                # Context Fallback 2: Access denied
                self.parent.after(0, callback, "purpleberry: permission denied", "locked_berry.txt")
                return

            clean_content = self.purpleberry_sanitize_content(content)
            filename = os.path.basename(safe_path)
            self.parent.after(0, callback, clean_content, filename)

        except Exception:
            self.parent.after(0, callback, "purpleberry read crashed gracefully", "error_berry.txt")

    def _purpleberry_sync_read_fallback(self, raw_path, callback):
        safe_path = self.purpleberry_sanitize_filepath(raw_path)
        if safe_path and os.path.exists(safe_path):
            try:
                with open(safe_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                callback(content, os.path.basename(safe_path))
            except Exception:
                callback("purpleberry fallback", "error.txt")
        else:
            callback("invalid path", "error.txt")

    def write_file(self, raw_path, raw_content, callback):
        if self.purpleberry_loop_alive:
            try:
                asyncio.run_coroutine_threadsafe(
                    self.purpleberry_async_write(raw_path, raw_content, callback), self.purpleberry_loop
                )
            except Exception:
                self._purpleberry_sync_write_fallback(raw_path, raw_content, callback)
        else:
            self._purpleberry_sync_write_fallback(raw_path, raw_content, callback)

    async def purpleberry_async_write(self, raw_path, raw_content, callback):
        try:
            await asyncio.sleep(0.02)
            safe_path = self.purpleberry_sanitize_filepath(raw_path)
            clean_content = self.purpleberry_sanitize_content(raw_content)

            if not safe_path:
                self.parent.after(0, callback, False, "invalid path")
                return

            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(clean_content)

            self.parent.after(0, callback, True, os.path.basename(safe_path))
        except PermissionError:
            self.parent.after(0, callback, False, "permission denied")
        except Exception:
            self.parent.after(0, callback, False, "write crash fallback")

    def _purpleberry_sync_write_fallback(self, raw_path, raw_content, callback):
        safe_path = self.purpleberry_sanitize_filepath(raw_path)
        if safe_path:
            try:
                with open(safe_path, "w", encoding="utf-8") as f:
                    f.write(self.purpleberry_sanitize_content(raw_content))
                callback(True, os.path.basename(safe_path))
            except Exception:
                callback(False, "write error")
        else:
            callback(False, "bad path")

    def ask_open_filename(self):
        try:
            return filedialog.askopenfilename(
                filetypes=[("Text & Markdown", "*.txt *.md"), ("All Files", "*.*")]
            )
        except Exception:
            return ""

    def ask_save_filename(self):
        try:
            return filedialog.asksaveasfilename(
                defaultextension=".md",
                filetypes=[("Markdown", "*.md"), ("Text", "*.txt"), ("All Files", "*.*")]
            )
        except Exception:
            return ""
