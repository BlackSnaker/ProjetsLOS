import sys
import sounddevice as sd
import numpy as np
import aubio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QComboBox, QPushButton, QHBoxLayout, QRadioButton, QButtonGroup,
    QProgressBar, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject

class AudioProcessor(QObject):
    note_detected = pyqtSignal(str, float)

    def __init__(self):
        super().__init__()
        self.pitch_detector = aubio.pitch("default", 2048, 2048 // 2, 44100)
        self.pitch_detector.set_unit("Hz")
        self.pitch_detector.set_silence(-40)

    def process_audio(self, indata, frames, time, status):
        if status:
            print(status)

        samples = np.frombuffer(indata, dtype=np.float32)
        pitch = self.pitch_detector(samples)[0]
        detected_note = self.freq_to_note(pitch)

        if detected_note:
            self.note_detected.emit(detected_note, pitch)

    def freq_to_note(self, freq):
        A4 = 440.0
        C0 = A4 * pow(2, -4.75)
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        if freq > 0:
            h = round(12 * np.log2(freq / C0))
            octave = h // 12
            n = h % 12
            note = note_names[n] + str(octave)
            return note
        return None

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Привет")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.title_label = QLabel("Готов настроиться?")
        self.title_label.setFont(QFont('Roboto', 32))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        QTimer.singleShot(2000, self.update_text)

    def update_text(self):
        self.title_label.setText("Поехали!!")
        QTimer.singleShot(1000, self.start_main_window)

    def start_main_window(self):
        self.main_window = GuitarTuner()
        self.main_window.show()
        self.close()

class GuitarTuner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TuneMe")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.title_label = QLabel("Настройся")
        self.title_label.setFont(QFont('Roboto', 32))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.create_separator()

        self.guitar_type_label = QLabel("Выбери тип гитары:")
        self.guitar_type_label.setFont(QFont('Roboto', 16))
        self.layout.addWidget(self.guitar_type_label)

        self.guitar_type_combo = QComboBox()
        self.guitar_type_combo.addItems(["Акустика", "Электро", "Бас"])
        self.guitar_type_combo.setFont(QFont('Roboto', 14))
        self.layout.addWidget(self.guitar_type_combo)

        self.tuning_label = QLabel("Выбери строй:")
        self.tuning_label.setFont(QFont('Roboto', 16))
        self.layout.addWidget(self.tuning_label)

        self.tuning_combo = QComboBox()
        self.tuning_combo.addItems(["Standard", "Drop D", "DADGAD", "Open G"])
        self.tuning_combo.setFont(QFont('Roboto', 14))
        self.layout.addWidget(self.tuning_combo)

        self.create_separator()

        self.strings_layout = QVBoxLayout()
        self.layout.addLayout(self.strings_layout)

        self.string_labels = []
        self.string_buttons = []
        self.string_bars = []
        self.button_group = QButtonGroup()

        for i in range(6):
            hbox = QHBoxLayout()
            label = QLabel(f"Струна {i+1}: Не настроена")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont('Roboto', 14))
            button = QRadioButton()
            if i == 0:
                button.setChecked(True)
            self.button_group.addButton(button, i)
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setTextVisible(False)
            bar.setFixedHeight(20)
            bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #bbb;
                    border-radius: 10px;
                    background-color: #eee;
                }
                QProgressBar::chunk {
                    border-radius: 10px;
                    background-color: #f44336;
                }
            """)
            self.string_labels.append(label)
            self.string_buttons.append(button)
            self.string_bars.append(bar)
            hbox.addWidget(button)
            hbox.addWidget(label)
            hbox.addWidget(bar)
            self.strings_layout.addLayout(hbox)

        self.create_separator()

        self.update_tuning_button = QPushButton("Обновить строй")
        self.update_tuning_button.setFont(QFont('Roboto', 14))
        self.update_tuning_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.update_tuning_button.clicked.connect(self.update_tuning)
        self.layout.addWidget(self.update_tuning_button)

        self.start_tuning_button = QPushButton("Начать настройку")
        self.start_tuning_button.setFont(QFont('Roboto', 14))
        self.start_tuning_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #007BB5;
            }
        """)
        self.start_tuning_button.clicked.connect(self.start_tuning)
        self.layout.addWidget(self.start_tuning_button)

        self.audio_processor = AudioProcessor()
        self.audio_processor.note_detected.connect(self.update_string_label)

        self.selected_tuning = ["E2", "A2", "D3", "G3", "B3", "E4"]

    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #aaa;")
        self.layout.addWidget(separator)

    def update_tuning(self):
        tuning = self.tuning_combo.currentText()

        tuning_map = {
            "Standard": ["E2", "A2", "D3", "G3", "B3", "E4"],
            "Drop D": ["D2", "A2", "D3", "G3", "B3", "E4"],
            "DADGAD": ["D2", "A2", "D3", "G3", "A3", "D4"],
            "Open G": ["D2", "G2", "D3", "G3", "B3", "D4"]
        }

        self.selected_tuning = tuning_map.get(tuning, ["E2", "A2", "D3", "G3", "B3", "E4"])

        for i, label in enumerate(self.string_labels):
            label.setText(f"Струна {i+1}: {self.selected_tuning[i]}")
            label.setStyleSheet("color: black;")
            self.string_bars[i].setValue(0)
            self.string_bars[i].setStyleSheet("""
                QProgressBar {
                    border: 1px solid #bbb;
                    border-radius: 10px;
                    background-color: #eee;
                }
                QProgressBar::chunk {
                    border-radius: 10px;
                    background-color: #f44336;
                }
            """)

    def start_tuning(self):
        self.stream = sd.InputStream(callback=self.audio_processor.process_audio, channels=1, samplerate=44100, blocksize=1024)
        self.stream.start()

    def update_string_label(self, detected_note, detected_freq):
        current_string = self.button_group.checkedId()
        expected_note = self.selected_tuning[current_string]

        if detected_note == expected_note:
            self.string_labels[current_string].setText(f"Струна {current_string + 1}: {expected_note} (Настроена)")
            self.string_labels[current_string].setStyleSheet("color: green;")
            self.string_bars[current_string].setValue(100)
            self.string_bars[current_string].setStyleSheet("""
                QProgressBar {
                    border: 1px solid #bbb;
                    border-radius: 10px;
                    background-color: #eee;
                }
                QProgressBar::chunk {
                    border-radius: 10px;
                    background-color: #4CAF50;
                }
            """)
        else:
            freq_diff = abs(self.note_to_freq(expected_note) - detected_freq)
            if freq_diff < 1:
                self.string_labels[current_string].setText(f"Струна {current_string + 1}: {expected_note} (Почти настроена: {detected_note})")
                self.string_labels[current_string].setStyleSheet("color: yellow;")
                self.string_bars[current_string].setValue(66)
                self.string_bars[current_string].setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #bbb;
                        border-radius: 10px;
                        background-color: #eee;
                    }
                    QProgressBar::chunk {
                        border-radius: 10px;
                        background-color: #FFEB3B;
                    }
                """)
            else:
                self.string_labels[current_string].setText(f"Струна {current_string + 1}: {expected_note} (В настройке: {detected_note})")
                self.string_labels[current_string].setStyleSheet("color: red;")
                self.string_bars[current_string].setValue(33)
                self.string_bars[current_string].setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #bbb;
                        border-radius: 10px;
                        background-color: #eee;
                    }
                    QProgressBar::chunk {
                        border-radius: 10px;
                        background-color: #f44336;
                    }
                """)

    def note_to_freq(self, note):
        A4 = 440.0
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = int(note[-1])
        key_number = note_names.index(note[:-1])
        key_number = key_number + (octave * 12)
        if key_number >= 49:
            freq = A4 * 2.0**((key_number - 49) / 12.0)
        else:
            freq = A4 / 2.0**((49 - key_number) / 12.0)
        return freq

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec())
