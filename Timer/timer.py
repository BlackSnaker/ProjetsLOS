import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTimeEdit, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QPalette, QPainterPath, QPainter, QBrush, QFont, QLinearGradient
from PyQt6.QtCore import Qt, QTimer, QTime, QRectF, QPropertyAnimation, QEasingCurve
from playsound import playsound
import subprocess

class NeumorphismButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #E0E5EC;
                border-radius: 20px;
                padding: 15px;
                color: #333333;
                font-size: 18px;
                border: none;
                box-shadow: 10px 10px 20px #bebebe, -10px -10px 20px #ffffff;
            }
            QPushButton:hover {
                background-color: #D3DAE6;
            }
            QPushButton:pressed {
                background-color: #BFC9D8;
            }
        """)
        self.setFixedSize(200, 50)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)

    def enterEvent(self, event):
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())

        # Background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#E0E5EC"))
        gradient.setColorAt(1, QColor("#D3DAE6"))
        background_path = QPainterPath()
        background_path.addRoundedRect(rect.adjusted(-5, -5, 5, 5), 20, 20)
        painter.fillPath(background_path, QBrush(gradient))

        super().paintEvent(event)

class NeumorphismLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #E0E5EC;
                border-radius: 20px;
                padding: 15px;
                color: #333333;
                font-size: 18px;
                box-shadow: 10px 10px 20px #bebebe, -10px -10px 20px #ffffff;
            }
        """)
        self.setFixedSize(250, 50)
        self.setFont(QFont("Arial", 16, QFont.Weight.Bold))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())

        # Background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#E0E5EC"))
        gradient.setColorAt(1, QColor("#D3DAE6"))
        background_path = QPainterPath()
        background_path.addRoundedRect(rect.adjusted(-5, -5, 5, 5), 20, 20)
        painter.fillPath(background_path, QBrush(gradient))

        super().paintEvent(event)

class NeumorphismTimeEdit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTimeEdit {
                background-color: #E0E5EC;
                border-radius: 20px;
                padding: 10px;
                color: #333333;
                font-size: 18px;
                box-shadow: inset 5px 5px 10px #bebebe, inset -5px -5px 10px #ffffff;
            }
        """)
        self.setDisplayFormat("HH:mm")
        self.setFixedSize(200, 50)
        self.setFont(QFont("Arial", 16))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())

        # Background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#E0E5EC"))
        gradient.setColorAt(1, QColor("#D3DAE6"))
        background_path = QPainterPath()
        background_path.addRoundedRect(rect.adjusted(-5, -5, 5, 5), 20, 20)
        painter.fillPath(background_path, QBrush(gradient))

        super().paintEvent(event)

class AlarmClock(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Будильник")
        self.setGeometry(100, 100, 400, 300)

        # Установка прозрачного фона
        self.setWindowOpacity(0.95)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(167, 199, 231))  # Мягкий лазурный цвет
        self.setPalette(palette)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        header = QLabel("Установите будильник", self)
        header.setStyleSheet("color: #333333; font-size: 24px; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        time_layout = QHBoxLayout()
        time_layout.addStretch(1)
        self.timeEdit = NeumorphismTimeEdit(self)
        time_layout.addWidget(self.timeEdit, alignment=Qt.AlignmentFlag.AlignCenter)
        time_layout.addStretch(1)
        layout.addLayout(time_layout)
        layout.addSpacing(20)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.setAlarmButton = NeumorphismButton("Установить будильник", self)
        button_layout.addWidget(self.setAlarmButton, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        layout.addSpacing(20)
        self.setAlarmButton.clicked.connect(self.set_alarm)

        status_layout = QHBoxLayout()
        status_layout.addStretch(1)
        self.statusLabel = NeumorphismLabel("Будильник не установлен", self)
        status_layout.addWidget(self.statusLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        status_layout.addStretch(1)
        layout.addLayout(status_layout)

        central_widget.setLayout(layout)

        # Таймер для проверки времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_alarm)

        self.show()

    def set_alarm(self):
        self.alarm_time = self.timeEdit.time()
        self.statusLabel.setText(f"Будильник установлен на {self.alarm_time.toString('HH:mm')}")
        self.timer.start(1000)

    def check_alarm(self):
        current_time = QTime.currentTime()
        if current_time.hour() == self.alarm_time.hour() and current_time.minute() == self.alarm_time.minute():
            self.timer.stop()
            self.statusLabel.setText("Будильник сработал!")
            playsound('/home/blacksnaker/NativeProgramsForLunaOS/Timer/Будильник.mp3')  
            self.show_notification()

    def show_notification(self):
        subprocess.run(['notify-send', 'Будильник', 'Будильник сработал!'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlarmClock()
    sys.exit(app.exec())
