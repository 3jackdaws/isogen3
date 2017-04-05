import threading
import time

TASK_QUEUE = []

class MemCache:
    internal = {}
    def __getattr__(self, item):
        return self.internal[item]

    def __setattr__(self, key, value):
        self.internal[key] = value
        return self.internal[key]

cache = MemCache()

def async_run(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.setDaemon(True)
    thread.start()

def async_defer(target, wait_for=1, *args, **kwargs):
    def wrap(*args, **kwargs):
        time.sleep(wait_for)
        target(*args, **kwargs)
    async_run(wrap, args, kwargs)


def test_print(func, text):
    print(text)
    func()

