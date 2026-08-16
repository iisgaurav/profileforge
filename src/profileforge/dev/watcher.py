import threading
from pathlib import Path

from colorama import Fore, Style
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from profileforge.dev.events import livereload_bus
from profileforge.dev.rebuild import rebuild_incremental


class DebouncedRebuilder(FileSystemEventHandler):
    def __init__(self, debounce_seconds=1.0):
        self.debounce_seconds = debounce_seconds
        self._timer = None
        self._lock = threading.Lock()
        self._modified_files = set()

    def on_modified(self, event):
        if event.is_directory:
            return

        path = event.src_path
        # Only care about .py and .yaml files
        if not (path.endswith(".py") or path.endswith(".yaml")):
            return

        with self._lock:
            self._modified_files.add(path)

            if self._timer is not None:
                self._timer.cancel()

            self._timer = threading.Timer(self.debounce_seconds, self._trigger_rebuild)
            self._timer.start()

    def _trigger_rebuild(self):
        with self._lock:
            files = list(self._modified_files)
            self._modified_files.clear()

        if not files:
            return

        print(
            f"\n{Fore.YELLOW}» Detected changes in {len(files)} file(s){Style.RESET_ALL}"
        )

        # Trigger incremental rebuild
        rebuild_incremental(files)

        # Notify browser to reload
        livereload_bus.publish("RELOAD")


def start_watcher(watch_dirs: list[str]) -> Observer:
    observer = Observer()
    handler = DebouncedRebuilder(debounce_seconds=1.0)

    watched_paths = []
    for d in watch_dirs:
        p = Path(d).resolve()
        if p.exists():
            observer.schedule(handler, str(p), recursive=True)
            watched_paths.append(str(p))

    observer.start()
    return observer, watched_paths
