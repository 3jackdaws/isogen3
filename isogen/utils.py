import threading

BACKGROUND_THREAD = None

TASK_QUEUE = []

def queue_task(target, *args, **kwargs):
    global TASK_QUEUE, BACKGROUND_THREAD
    thread = threading.Thread(target=wrap_task(target), args=args, kwargs=kwargs)
    thread.setDaemon(True)
    TASK_QUEUE.append(thread)
    if BACKGROUND_THREAD is None:
        print("pop")
        BACKGROUND_THREAD = TASK_QUEUE.pop()
        BACKGROUND_THREAD.start()

def wrap_task(task):
    global BACKGROUND_THREAD
    def wrapper(*args, **kwargs):
        task(*args, **kwargs)
        if len(TASK_QUEUE) > 0:
            BACKGROUND_THREAD = TASK_QUEUE.pop()
            BACKGROUND_THREAD.start()
        else:
            BACKGROUND_THREAD = None
    return wrapper


def test_print(func, text):
    print(text)
    func()

