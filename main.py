import sys
from datetime import date, datetime, timedelta
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QPushButton,
                               QVBoxLayout,
                               QLabel)


class MyWidget(QWidget):
    MSEC_IN_MINUT = 60_000
    def __init__(self):
        super().__init__()

        self.setStyleSheet(self.loadStyleSheets( 'stylesheets.scss' ))

        self.startTime = None
        self.updateTimer = QTimer(self)

        self.isWork = False
        self.workTime: int = 25
        self.pauseTime: int = 5

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)


        self.label = QLabel("00:00")
        self.labelT = QLabel("Lets do some tasks")

        self.startBtn = QPushButton("Start pomodoro")

        self.__layout = QVBoxLayout(self)

        self.__layout.addWidget(self.labelT)
        self.__layout.addWidget(self.label)
        self.__layout.addWidget(self.startBtn)

        self.startBtn.clicked.connect(self.btnCalback)

        self.timer.timeout.connect(self.togglePause)

        self.updateTimer.timeout.connect(self.updateLabel)

        self.resize(400, 200)
        self.show()

    def loadStyleSheets(self, path: str):
        with open(path, 'r') as file:
            return ''.join(file.readlines()).replace('\n', '')

    def btnCalback(self):
        if self.isWork:
            self.stop()
        else:
            self.start()

    def startState(self):
        self.isWork = False
        self.startBtn.setText("Start")
        self.labelT.setText("Lets do some tasks")
        self.label.setText("00:00")
        self.timer.stop()
        self.updateTimer.stop()

    def start(self):
        self.labelT.setText("Work time")
        self.startBtn.setText("Stop")
        self.startTimers(self.workTime)
        self.isWork = True

    def stop(self):
        self.startState()
        self.timer.stop()
        self.updateTimer.stop()

    def pause(self):
        self.labelT.setText("Pause time")
        self.startBtn.setText('Start')
        self.startTimers(self.pauseTime)
        self.isWork = False

    def togglePause(self):
        if self.isWork:
            self.pause()
        else:
            self.start()

    def startTimers(self , time: int):
        self.startTime = datetime.now()
        self.timer.start(time * self.MSEC_IN_MINUT)
        self.updateTimer.start(1000)

    def updateLabel(self):
        timedelta = datetime.now() - self.startTime
        timedelta += datetime.min

        self.label.setText(timedelta.strftime("%M:%S"))

if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()

    sys.exit(app.exec())

