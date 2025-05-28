import time

from PyQt5.QtCore import QProcess, QTextCodec, QCoreApplication, QByteArray
from PyQt5.QtWidgets import *
import sys, re, os

re_pattern = re.compile("[a-zA-Z]+:\s(\d+)%")
new_proc_pattern = re.compile("Time to start process 2")
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.p = None
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.btn_start = QPushButton("&Execute")
        self.btn_start.pressed.connect(self.start_process)
        self.btn_write = QPushButton("&Write")
        self.btn_write.pressed.connect(self.write_to_the_process)

        self.widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.hLayout = QHBoxLayout()
        self.vLayout.addWidget(self.text)
        self.hLayout.addWidget(self.btn_start)
        self.hLayout.addWidget(self.btn_write)
        self.wid_btns = QWidget()
        self.wid_btns.setLayout(self.hLayout)
        self.vLayout.addWidget(self.wid_btns)
        self.widget.setLayout(self.vLayout)
        self.setCentralWidget(self.widget)

    def start_process(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardError.connect(self.stderr_handler)
            self.p.readyReadStandardOutput.connect(self.stdout_handler)
            self.p.stateChanged.connect(self.state_handler)
            self.p.finished.connect(self.process_finish_handler)
            self.p.errorOccurred.connect(self.error_handler)
            dirr = QCoreApplication.applicationFilePath()
            self.p.start(dirr, ["External.py", "Hello from master"])


    def message(self, text):
        self.text.appendPlainText(text)

    def write_to_the_process(self):
        if not (self.p is None):
            strr = b"I'm written from master\n"
            a = QByteArray(strr)
            self.p.write(a)

    def stderr_handler(self):

        self.p.setReadChannel(QProcess.ProcessChannel.StandardError)
        codec = QTextCodec.codecForName("utf8")
        s = self.p.readAll()

        err = codec.toUnicode(s)
        st = re_pattern.search(err)

    def stdout_handler(self):
        self.p.setReadChannel(QProcess.ProcessChannel.StandardOutput)
        s = self.p.readAll()
        codec = QTextCodec.codecForName("utf8")
        out = codec.toUnicode(s)
        self.message(out)

    def state_handler(self, state):
        states = {
            QProcess.ProcessState.NotRunning: "Not Running",
            QProcess.ProcessState.Starting: "Starting",
            QProcess.ProcessState.Running: "Running"
        }
        state_to_show = states[state]
        self.message(state_to_show)

    def error_handler(self, error):
        errors = {
            QProcess.ProcessError.ReadError: "ReadError",
            QProcess.ProcessError.WriteError: "WriteError",
            QProcess.ProcessError.UnknownError: "UnknownError"
        }
        error_to_show = errors[error]
        self.message(error_to_show)

    def process_finish_handler(self):
        self.message("Process finished")
        self.p = None

if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())