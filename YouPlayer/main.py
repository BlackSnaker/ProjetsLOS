import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QPushButton, QLineEdit, QSlider, QLabel, 
                             QHBoxLayout, QFileDialog, QGraphicsDropShadowEffect)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPalette, QColor

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Glassmorphism Video Player")
        self.setGeometry(100, 100, 800, 600)
        
        # Set background color without blur effect
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255, 90))
        self.setPalette(palette)
        
        # Glassmorphism effect for widgets
        def apply_glassmorphism(widget):
            widget.setAutoFillBackground(True)
            widget.setStyleSheet("background: rgba(255, 255, 255, 0.3); border-radius: 15px;")
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 80))
            shadow.setOffset(0, 0)
            widget.setGraphicsEffect(shadow)
        
        # Video player setup
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        
        # Audio output
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        
        # Control buttons
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_video)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)
        
        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.open_file)
        
        apply_glassmorphism(self.play_button)
        apply_glassmorphism(self.pause_button)
        apply_glassmorphism(self.stop_button)
        apply_glassmorphism(self.open_button)
        
        # Slider for video position
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        
        apply_glassmorphism(self.position_slider)
        
        # Slider for volume control
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)  # Устанавливаем диапазон громкости от 0 до 100
        self.volume_slider.setValue(int(self.audio_output.volume() * 100))  # Преобразуем float в int
        self.volume_slider.valueChanged.connect(self.set_volume)
        
        apply_glassmorphism(self.volume_slider)
        
        # Search bar for YouTube
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search YouTube...")
        self.search_bar.returnPressed.connect(self.search_video)
        
        apply_glassmorphism(self.search_bar)
        
        # Layout setup
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.open_button)
        
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume"))
        volume_layout.addWidget(self.volume_slider)
        
        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.video_widget)
        layout.addWidget(self.position_slider)
        layout.addLayout(control_layout)
        layout.addLayout(volume_layout)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        
    def play_video(self):
        self.media_player.play()
        
    def pause_video(self):
        self.media_player.pause()
        
    def stop_video(self):
        self.media_player.stop()
        
    def set_position(self, position):
        self.media_player.setPosition(position)
        
    def update_position(self, position):
        self.position_slider.setValue(position)
        
    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)
        
    def set_volume(self, volume):
        self.audio_output.setVolume(volume / 100)  # Преобразуем обратно в float
        
    def search_video(self):
        search_text = self.search_bar.text()
        # Implement YouTube search logic here
        print(f"Searching for: {search_text}")
        
    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Video")
        if file_path:
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.play_video()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
