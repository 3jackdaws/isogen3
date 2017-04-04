import threading

def background(target, args=None, kwargs=None):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.setDaemon(True)
    thread.start()