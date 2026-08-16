import queue
import threading


class EventBus:
    def __init__(self):
        self._subscribers = []
        self._lock = threading.Lock()

    def subscribe(self) -> queue.Queue:
        q = queue.Queue()
        with self._lock:
            self._subscribers.append(q)
        return q

    def unsubscribe(self, q: queue.Queue):
        with self._lock:
            if q in self._subscribers:
                self._subscribers.remove(q)

    def publish(self, message: str):
        with self._lock:
            for q in self._subscribers:
                q.put(message)

# Global event bus for livereload signaling
livereload_bus = EventBus()
