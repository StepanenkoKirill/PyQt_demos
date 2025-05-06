from PyQt5 import QtCore, Qt, QtWidgets, QtGui
import sys, traceback, time

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(object)
    finish = QtCore.pyqtSignal()
    callback_progress = QtCore.pyqtSignal(int)
    error = QtCore.pyqtSignal(tuple)


class Worker(QtCore.QRunnable):
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['callback_progress'] = self.signals.callback_progress


    @QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exc, val = sys.exc_info()[:2]
            self.signals.error.emit(exc, val, traceback.format_exc())

        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finish.emit()


class Window(QtWidgets.QMainWindow):
    '''
    The important thing is that you should make the QThreadpool object
    beforehand, i.e. if you create pool with main window simultaneously
    this won't work.
    '''
    def __init__(self, thread_pool):
        super(Window, self).__init__()
        self.centWidget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.counter = 0
        self.lbl1 = QtWidgets.QLabel("Progress bar widget")
        self.lbl1.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        self.prog_bar = QtWidgets.QProgressBar()
        self.prog_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.prog_bar.setMinimum(0)
        self.prog_bar.setMaximum(100)
        self.prog_bar.setToolTip("Shows progress of another thread")
        self.l = QtWidgets.QLabel("Start")
        self.main_layout.addWidget(self.lbl1)
        self.main_layout.addWidget(self.l)
        self.main_layout.addWidget(self.prog_bar)
        self.centWidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centWidget)
        self.btn_ex = QtWidgets.QPushButton("Exit")
        self.btn_ex.clicked.connect(QtWidgets.QApplication.quit)

        self.main_layout.addWidget(self.btn_ex)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        w = Worker(self.function_to_operate)
        w.signals.error.connect(self.error_handler)
        w.signals.result.connect(self.result_handler)
        w.signals.callback_progress.connect(self.progress_handler)
        w.signals.finish.connect(self.finish_handler)
        thread_pool.start(w)


    def function_to_operate(self, callback_progress):
        n = 5
        for i in range(n):
            time.sleep(2)
            callback_progress.emit(int(100*(i + 1)/n))

    def error_handler(self, *args):
        print(args)

    def result_handler(self, arg):
        self.lbl1.setText("Done")

    def finish_handler(self):
        print("Thread completed")

    def progress_handler(self, val):
        self.prog_bar.setValue(val)


    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pool = QtCore.QThreadPool()
    win = Window(thread_pool=pool)
    win.show()
    app.exec()
