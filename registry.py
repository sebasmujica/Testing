import threading

class Registry:
    def __init__(self):
        self._clients = {}
        self._lock = threading.Lock()

    @property
    def count(self):
        with self._lock:
            return len(self._clients)

    def add(self, client, nick):
        with self._lock:
            self._clients[client] = nick

    def remove(self, client):
        with self._lock:
            nick = self._clients[client]
            del self._clients[client]
            return nick

    def peers(self, sender):
        with self._lock:
            return [c for c in self._clients.keys() if c is not sender]
