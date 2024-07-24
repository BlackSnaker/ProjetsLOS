import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QScrollArea, QFileDialog, QPushButton, QHBoxLayout, QGraphicsBlurEffect, QMenu, QListWidget, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget

class BlurEffectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = ""
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

    def set_image(self, image_path):
        self.image_path = image_path
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(self.apply_blur_effect(pixmap))

    def apply_blur_effect(self, pixmap):
        image = pixmap.toImage()
        blurred_image = image.blurred(radius=20)  # Используем метод blurred для эффекта blur
        return QPixmap.fromImage(blurred_image)

class VideoWidget(QWidget):
    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.video_widget = QVideoWidget(self)
        self.layout.addWidget(self.video_widget)
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QUrl.fromLocalFile(self.video_path))
        self.media_player.play()

class GalleryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Галерея с эффектом Blur")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Создаем фоновый виджет с эффектом blur
        background_label = QLabel(main_widget)
        pixmap = QPixmap('path_to_background_image.jpg')
        background_label.setPixmap(pixmap)
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        background_label.setGraphicsEffect(blur_effect)
        main_layout.addWidget(background_label)

        # Создаем область прокрутки
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)
        main_layout.addWidget(scroll_area)

        # Добавляем список для фото и видео
        self.media_list = QListWidget()
        self.media_list.setIconSize(QSize(100, 100))  # Устанавливаем размер иконок
        self.media_list.setViewMode(QListWidget.IconMode)  # Устанавливаем режим отображения
        self.media_list.setResizeMode(QListWidget.AdjustSize)  # Устанавливаем автоматический размер
        scroll_area_layout.addWidget(self.media_list)

        # Добавляем кнопку для добавления медиафайлов
        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить Фото/Видео", self)
        add_button.clicked.connect(self.add_media)
        button_layout.addWidget(add_button)
        main_layout.addLayout(button_layout)

        self.layout = scroll_area_layout

        # Добавляем контекстное меню для каждого элемента
        self.media_context_menu = QMenu(self)
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.delete_media)
        self.media_context_menu.addAction(delete_action)

    def add_image(self, image_path):
        item = QListWidgetItem(QIcon(image_path), "")
        self.media_list.addItem(item)

    def add_video(self, video_path):
        item = QListWidgetItem(QIcon('path_to_video_icon.png'), "")
        self.media_list.addItem(item)

    def add_media(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать Фото или Видео", "", "Images (*.png *.xpm *.jpg);;Videos (*.mp4 *.avi *.mkv)")
        if file_path:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.add_image(file_path)
            elif file_path.lower().endswith(('.mp4', '.avi', '.mkv')):
                self.add_video(file_path)

    def show_media_context_menu(self, pos):
        widget = self.sender()
        if widget:
            self.media_context_menu.exec(widget.mapToGlobal(pos))

    def delete_media(self):
        widget = self.sender()
        if widget:
            self.layout.removeWidget(widget)
            widget.deleteLater()

def main():
    app = QApplication(sys.argv)
    window = GalleryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
