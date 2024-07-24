import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit,
                             QListWidget, QHBoxLayout, QListWidgetItem, QColorDialog, QFontDialog, QMenuBar, QMenu)
from PyQt6.QtGui import QColor, QPalette, QFont, QAction
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
import speech_recognition as sr
from packaging.version import Version

# Цвета для стиля Neumorphism
BACKGROUND_COLOR = QColor(40, 40, 40)
SHADOW_COLOR_DARK = QColor(25, 25, 25)
SHADOW_COLOR_LIGHT = QColor(55, 55, 55)
ACCENT_COLOR = QColor(255, 178, 127)  # Peach color

# Основные стили
def get_neumorphism_style():
    return f"""
    QWidget {{
        background-color: rgba({BACKGROUND_COLOR.red()}, {BACKGROUND_COLOR.green()}, {BACKGROUND_COLOR.blue()}, 200);
        border-radius: 15px;
        color: white;
    }}
    QLineEdit, QTextEdit, QListWidget, QPushButton {{
        background-color: rgba({BACKGROUND_COLOR.red()}, {BACKGROUND_COLOR.green()}, {BACKGROUND_COLOR.blue()}, 200);
        border-radius: 15px;
        padding: 10px;
        color: white;
        border: none;
        box-shadow: 10px 10px 20px rgba({SHADOW_COLOR_DARK.red()}, {SHADOW_COLOR_DARK.green()}, {SHADOW_COLOR_DARK.blue()}, 100), 
                    -10px -10px 20px rgba({SHADOW_COLOR_LIGHT.red()}, {SHADOW_COLOR_LIGHT.green()}, {SHADOW_COLOR_LIGHT.blue()}, 100);
    }}
    QLineEdit {{
        border: 1px solid rgb({ACCENT_COLOR.red()}, {ACCENT_COLOR.green()}, {ACCENT_COLOR.blue()});
    }}
    QTextEdit {{
        border: 1px solid rgb({ACCENT_COLOR.red()}, {ACCENT_COLOR.green()}, {ACCENT_COLOR.blue()});
    }}
    QPushButton {{
        border: 1px solid rgb({ACCENT_COLOR.red()}, {ACCENT_COLOR.green()}, {ACCENT_COLOR.blue()});
        transition: all 0.3s ease;
    }}
    QPushButton:pressed {{
        box-shadow: inset 10px 10px 20px rgb({SHADOW_COLOR_DARK.red()}, {SHADOW_COLOR_DARK.green()}, {SHADOW_COLOR_DARK.blue()}), 
                    inset -10px -10px 20px rgb({SHADOW_COLOR_LIGHT.red()}, {SHADOW_COLOR_LIGHT.green()}, {SHADOW_COLOR_LIGHT.blue()});
    }}
    QListWidget {{
        border: 1px solid rgb({ACCENT_COLOR.red()}, {ACCENT_COLOR.green()}, {ACCENT_COLOR.blue()});
    }}
    """

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Neumorphism Notes App')
        self.setGeometry(100, 100, 600, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.notes_list = QListWidget(self)
        self.notes_list.itemClicked.connect(self.load_note)
        self.layout.addWidget(self.notes_list, 1)
        
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_layout)
        self.layout.addWidget(self.right_widget, 2)
        
        self.note_title = QLineEdit(self)
        self.note_title.setPlaceholderText("Введите заголовок заметки")
        self.right_layout.addWidget(self.note_title)
        
        self.note_text = QTextEdit(self)
        self.note_text.setPlaceholderText("Введите текст заметки")
        self.right_layout.addWidget(self.note_text)
        
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_note)
        self.right_layout.addWidget(self.save_button)
        
        self.voice_button = QPushButton("Голосовой ввод", self)
        self.voice_button.clicked.connect(self.voice_input)
        self.right_layout.addWidget(self.voice_button)

        self.load_saved_notes()

        # Установка стилей
        self.apply_styles()

        # Установка прозрачности окна
        self.setWindowOpacity(0.9)  # Устанавливаем 90% прозрачности окна

        # Анимация появления элементов
        self.animate_widgets()

        # Создание меню
        self.create_menu()

    def apply_styles(self):
        self.setStyleSheet(get_neumorphism_style())
        # Установка цветовой палитры
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, BACKGROUND_COLOR)
        palette.setColor(QPalette.ColorRole.Base, BACKGROUND_COLOR)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

    def save_note(self):
        title = self.note_title.text()
        text = self.note_text.toPlainText()
        if title:
            with open(f'{title}.txt', 'w', encoding='utf-8') as file:
                file.write(text)
            self.note_title.clear()
            self.note_text.clear()
            self.load_saved_notes()

    def load_saved_notes(self):
        self.notes_list.clear()
        for file_name in os.listdir('.'):
            if file_name.endswith('.txt'):
                item = QListWidgetItem(file_name[:-4])
                self.notes_list.addItem(item)
    
    def load_note(self, item):
        title = item.text()
        with open(f'{title}.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.note_title.setText(title)
        self.note_text.setText(text)

    def animate_widgets(self):
        for widget in [self.notes_list, self.note_title, self.note_text, self.save_button, self.voice_button]:
            anim = QPropertyAnimation(widget, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(QRect(widget.x(), widget.y(), 0, 0))
            anim.setEndValue(widget.geometry())
            anim.start()

    def create_menu(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        
        # Меню "Настройки"
        settings_menu = QMenu('Настройки', self)
        menubar.addMenu(settings_menu)

        # Выбор цвета текста
        color_action = QAction('Выбрать цвет текста', self)
        color_action.triggered.connect(self.choose_text_color)
        settings_menu.addAction(color_action)

        # Выбор шрифта текста
        font_action = QAction('Выбрать шрифт текста', self)
        font_action.triggered.connect(self.choose_text_font)
        settings_menu.addAction(font_action)

    def choose_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.note_text.setTextColor(color)

    def choose_text_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.note_text.setFont(font)

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Скажите что-нибудь...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Вы сказали: " + text)
            self.note_text.append(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition не смог распознать речь")
        except sr.RequestError as e:
            print("Не удалось запросить результаты у Google Speech Recognition; {0}".format(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = NotesApp()
    main_win.show()
    sys.exit(app.exec())
