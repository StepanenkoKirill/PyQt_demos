import sys

from PyQt5 import QtWidgets, QtCore

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.btn1 = QtWidgets.QPushButton("Push me")
        self.btn2 = QtWidgets.QPushButton("You'll pay for this!")

        self.hlay = QtWidgets.QHBoxLayout()
        self.hlay.addWidget(self.btn1)
        self.hlay.addWidget(self.btn2)
        self.vlay = QtWidgets.QVBoxLayout()
        self.vlay.addLayout(self.hlay)
        self.setLayout(self.vlay)
        self.subproc = QtCore.QProcess()
        self.btn1.clicked.connect(self.StartSubprocess)
        self.btn2.clicked.connect(self.EndSubprocess)
        self.subproc.finished.connect(self.EndSubprocess)


    def StartSubprocess(self):
        s = r"python D:\QtPrograms\PyQt5_demos\QProcess_1\subprocess.py"
        self.subproc.start(s)
        self.subproc.readyRead.connect(self.ReadInfo)

    def EndSubprocess(self):
        if self.subproc.isOpen():
            self.subproc.kill()
        print("Subprocess finished")

    def ReadInfo(self):
        codec = QtCore.QTextCodec.codecForName("Windows-1251")
        out = self.subproc.readAll()
        decode_out = codec.toUnicode(out)
        print(decode_out)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
