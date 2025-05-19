from PyQt5.QtCore import QProcess, QTextCodec
from PyQt5.QtWidgets import *
import sys, re

re_pattern = re.compile("[a-zA-Z]+:\s(\d+)%")
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.p = None
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.prog_bar = QProgressBar()
        self.prog_bar.setRange(0, 100)
        self.btn_start = QPushButton("&Execute")
        self.btn_start.pressed.connect(self.start_process)

        self.widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.prog_bar)
        self.vLayout.addWidget(self.text)
        self.vLayout.addWidget(self.btn_start)
        self.widget.setLayout(self.vLayout)
        self.setCentralWidget(self.widget)

    def start_process(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardError.connect(self.stderr_handler)
            self.p.readyReadStandardOutput.connect(self.stdout_handler)
            self.p.stateChanged.connect(self.state_handler)
            self.p.finished.connect(self.process_finish_handler)
            dist = r"D:\QtPrograms\stabilisation_gui_(v2)\venv\Scripts\python.exe"
            self.p.start("python", ["External.py"])

    def message(self, text):
        self.text.appendPlainText(text)

    def stderr_handler(self):
        s = self.p.readAllStandardError()
        codec = QTextCodec.codecForName("utf8")
        err = codec.toUnicode(s)
        self.message(err)
        st = re_pattern.search(err)
        number = st.group(1)
        self.prog_bar.setValue(int(number))

    def stdout_handler(self):
        s = self.p.readAllStandardOutput()
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

    def process_finish_handler(self):
        self.message("Process finished")
        self.p = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())