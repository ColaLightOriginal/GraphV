class Queue:

    def __init__(self):
        self.queue = []

    def add(self,item):
        self.queue.append(item)

    def remove(self):
        if bool(self.queue) is True:
            val = self.queue[0]
            self.queue.pop(0)
            return val

    def checkNull(self):
        if not self.queue:
            return True

    def printQueue(self):
        for i in self.queue:
            print i
