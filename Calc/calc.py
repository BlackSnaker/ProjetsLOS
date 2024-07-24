import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QPlainTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memory = 0  # Добавляем переменную для хранения памяти
        self.history = []  # Добавляем список для хранения истории вычислений
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Neumorphism Calculator')
        self.setGeometry(100, 100, 300, 600)  # Увеличиваем высоту окна
        self.setFixedSize(300, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        vbox = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont('Arial', 24))
        self.display.setStyleSheet(self.display_style())
        vbox.addWidget(self.display)

        mode_layout = QHBoxLayout()
        self.basic_btn = QPushButton("Basic")
        self.basic_btn.setFont(QFont('Arial', 12))
        self.basic_btn.clicked.connect(self.show_basic)
        self.basic_btn.setStyleSheet(self.mode_button_style())

        self.sci_btn = QPushButton("Scientific")
        self.sci_btn.setFont(QFont('Arial', 12))
        self.sci_btn.clicked.connect(self.show_scientific)
        self.sci_btn.setStyleSheet(self.mode_button_style())

        self.prog_btn = QPushButton("Programmer")
        self.prog_btn.setFont(QFont('Arial', 12))
        self.prog_btn.clicked.connect(self.show_programmer)
        self.prog_btn.setStyleSheet(self.mode_button_style())

        mode_layout.addWidget(self.basic_btn)
        mode_layout.addWidget(self.sci_btn)
        mode_layout.addWidget(self.prog_btn)
        vbox.addLayout(mode_layout)

        self.grid = QGridLayout()
        vbox.addLayout(self.grid)

        self.history_display = QPlainTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setFont(QFont('Arial', 12))
        self.history_display.setStyleSheet(self.display_style())
        vbox.addWidget(self.history_display)

        self.central_widget.setLayout(vbox)
        self.show_basic()

    def mode_button_style(self):
        return """
        QPushButton {
            font-size: 12px;
            padding: 10px;
            border-radius: 15px;
            background: #f5a97b;
            color: #fff;
            border: none;
        }
        QPushButton:pressed {
            background: #FF4500;
        }
        """

    def neumorphism_style(self):
        return """
        QPushButton {
            font-size: 18px;
            padding: 20px;
            border-radius: 30px;
            background: #FF4500;
            color: #fff;
            border: none;
            box-shadow: 10px 10px 20px #aa2f00, -10px -10px 20px #ff5e14,
                        10px -10px 20px rgba(0, 0, 0, 0.2), -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        QPushButton:pressed {
            background: #FF4500;
            box-shadow: inset 10px 10px 20px #aa2f00, inset -10px -10px 20px #ff5e14,
                        inset 10px -10px 20px rgba(0, 0, 0, 0.2), inset -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        """

    def operation_button_style(self):
        return """
        QPushButton {
            font-size: 18px;
            padding: 20px;
            border-radius: 30px;
            background: #f5deb3;
            color: #000;
            border: none;
            box-shadow: 10px 10px 20px #aa2f00, -10px -10px 20px #ff5e14,
                        10px -10px 20px rgba(0, 0, 0, 0.2), -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        QPushButton:pressed {
            background: #f5deb3;
            box-shadow: inset 10px 10px 20px #aa2f00, inset -10px -10px 20px #ff5e14,
                        inset 10px -10px 20px rgba(0, 0, 0, 0.2), inset -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        """

    def function_button_style(self):
        return """
        QPushButton {
            font-size: 18px;
            padding: 20px;
            border-radius: 30px;
            background: #ffa07a;
            color: #000;
            border: none;
            box-shadow: 10px 10px 20px #cd5c5c, -10px -10px 20px #ffa07a,
                        10px -10px 20px rgba(0, 0, 0, 0.2), -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        QPushButton:pressed {
            background: #ffa07a;
            box-shadow: inset 10px 10px 20px #cd5c5c, inset -10px -10px 20px #ffa07a,
                        inset 10px -10px 20px rgba(0, 0, 0, 0.2), inset -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        """

    def display_style(self):
        return """
        QLineEdit {
            font-size: 32px;
            padding: 15px;
            border-radius: 30px;
            background: #f5a97b;
            color: #fff;
            box-shadow: inset 10px 10px 20px #aa2f00, inset -10px -10px 20px #ff5e14,
                        inset 10px -10px 20px rgba(0, 0, 0, 0.2), inset -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        QPlainTextEdit {
            font-size: 12px;
            padding: 10px;
            border-radius: 15px;
            background: #f5a97b;
            color: #fff;
            box-shadow: inset 10px 10px 20px #aa2f00, inset -10px -10px 20px #ff5e14,
                        inset 10px -10px 20px rgba(0, 0, 0, 0.2), inset -10px 10px 20px rgba(255, 255, 255, 0.3);
        }
        """

    def show_basic(self):
        self.clear_layout(self.grid)
        buttons = [
            ('MC', 0, 0), ('MR', 0, 1), ('M+', 0, 2), ('M-', 0, 3),
            ('C', 1, 0), ('DEL', 1, 1), ('(', 1, 2), (')', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
        ]
        self.create_buttons(buttons)

    def show_scientific(self):
        self.clear_layout(self.grid)
        buttons = [
            ('MC', 0, 0), ('MR', 0, 1), ('M+', 0, 2), ('M-', 0, 3),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3),
            ('sqrt', 2, 0), ('^', 2, 1), ('(', 2, 2), (')', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('+', 6, 3),
        ]
        self.create_buttons(buttons)

    def show_programmer(self):
        self.clear_layout(self.grid)
        buttons = [
            ('MC', 0, 0), ('MR', 0, 1), ('M+', 0, 2), ('M-', 0, 3),
            ('AND', 1, 0), ('OR', 1, 1), ('XOR', 1, 2), ('NOT', 1, 3),
            ('<<', 2, 0), ('>>', 2, 1), ('(', 2, 2), (')', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('+', 6, 3),
        ]
        self.create_buttons(buttons)

    def create_buttons(self, buttons):
        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            button.setFont(QFont('Arial', 18))
            if btn_text in {'/', '*', '-', '+', '=', '^', 'sin', 'cos', 'tan', 'log', 'sqrt', 'AND', 'OR', 'XOR', 'NOT', '<<', '>>'}:
                button.setStyleSheet(self.operation_button_style())
            elif btn_text in {'C', 'DEL', '(', ')', 'MC', 'MR', 'M+', 'M-'}:
                button.setStyleSheet(self.function_button_style())
            else:
                button.setStyleSheet(self.neumorphism_style())
            button.clicked.connect(self.on_click)
            self.grid.addWidget(button, row, col)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_click(self):
        sender = self.sender()
        btn_text = sender.text()

        if btn_text == 'C':
            self.display.clear()
        elif btn_text == 'DEL':
            current_text = self.display.text()
            self.display.setText(current_text[:-1])
        elif btn_text == '=':
            try:
                result = str(eval(self.display.text()))
                self.history.append(self.display.text() + " = " + result)
                self.update_history()
                self.display.setText(result)
            except Exception as e:
                self.display.setText('Error')
        elif btn_text == 'MC':
            self.memory = 0
        elif btn_text == 'MR':
            self.display.setText(self.display.text() + str(self.memory))
        elif btn_text == 'M+':
            try:
                self.memory += eval(self.display.text())
            except Exception as e:
                pass
        elif btn_text == 'M-':
            try:
                self.memory -= eval(self.display.text())
            except Exception as e:
                pass
        else:
            self.display.setText(self.display.text() + btn_text)

    def update_history(self):
        self.history_display.setPlainText("\n".join(self.history))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
