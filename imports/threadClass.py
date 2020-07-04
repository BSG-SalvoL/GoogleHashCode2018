from threading import Thread


class MyThread (Thread):
    def __init__(self, threadID, name, func, *arguments):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.func = func
        self.arguments = arguments

    def run(self):
        print("Starting Thread: " + str(self.threadID) + " " + self.name)
        if len(self.arguments) > 0:
            self.func(self.arguments)
        else:
            self.func()
