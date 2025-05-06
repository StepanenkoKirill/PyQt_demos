from PyQt5 import QtCore

class Worker(QtCore.QRunnable):
    def __init__(self, list1, index1, index2):
        self.start = index1
        self.stop = index2
        self.list = list1
        self.sum = 0
        super(Worker, self).__init__()

    def run(self) -> None:
        try:
            if (self.start >= 0) and (self.stop >= self.start):
                print(self.list[self.start:self.stop+1])
                self.sum = self.summ()
            else:
                print("Incorrect indexes")
        except Exception as e:
            print(str(e))

    def summ(self):
        return sum(self.list[self.start:self.stop+1])


pool = QtCore.QThreadPool()
print(f"max threads - {pool.maxThreadCount()}, active threads - {pool.activeThreadCount()}")
l = [0, 2, 3, 11, 22, 124, 0, 9]
w1 = Worker(l, 0, 2)
w2 = Worker(l, 3, 5)
w3 = Worker(l, 6, 7)
workers = [w1, w2, w3]
for w in workers:
    print(f"max threads - {pool.maxThreadCount()}, active threads - {pool.activeThreadCount()}")
    pool.start(w)
pool.waitForDone(100)
print(f"The final sum - {w1.sum + w2.sum + w3.sum}")
print(f"max threads - {pool.maxThreadCount()}, active threads - {pool.activeThreadCount()}")





