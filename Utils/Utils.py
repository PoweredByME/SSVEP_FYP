import threading;

# creating a decorator for threading a function.
def thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs);
        thread.start();
        return thread;
    return wrapper;

def Print(stringToPrint):
    print(stringToPrint);

