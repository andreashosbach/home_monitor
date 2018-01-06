from threading import Timer
def show():
    Timer(2.0, show).start()
    print("Hello")
    
    
show()
