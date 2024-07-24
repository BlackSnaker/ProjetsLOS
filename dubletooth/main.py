import sys
import asyncio
import subprocess
from PyQt6 import QtWidgets, QtCore, QtGui
from bleak import BleakScanner, BleakClient

class BluetoothHeadsetConnector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Подключение наушников по Bluetooth')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border-radius: 20px;
                padding: 20px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
                color: white;
            }
            QPushButton {
                background-color: #3E3E3E;
                border: 2px solid #5E5E5E;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                color: white;
                box-shadow: 5px 5px 15px #121212, -5px -5px 15px #2A2A2A;
            }
            QPushButton:hover {
                background-color: #4E4E4E;
                border: 2px solid #6E6E6E;
            }
            QTabWidget::pane {
                border: none;
                background-color: #2E2E2E;
            }
            QTabBar::tab {
                background: #3E3E3E;
                border: 2px solid #5E5E5E;
                border-radius: 15px;
                padding: 10px;
                margin: 2px;
                color: white;
                font-size: 16px;
                box-shadow: 5px 5px 15px #121212, -5px -5px 15px #2A2A2A;
            }
            QTabBar::tab:selected {
                background: #4E4E4E;
                border: 2px solid #6E6E6E;
            }
        """)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.device1_name = None
        self.device1_address = None
        self.device1_battery = None
        self.device2_name = None
        self.device2_address = None
        self.device2_battery = None
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()

        self.tab_widget.addTab(self.tab1, "Устройства")
        self.tab_widget.addTab(self.tab2, "Уровень заряда")
        self.tab_widget.addTab(self.tab3, "Настройки")

        self.create_device_tab()
        self.create_battery_tab()
        self.create_settings_tab()

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def create_device_tab(self):
        layout = QtWidgets.QVBoxLayout()

        self.device1_frame = QtWidgets.QFrame()
        self.device1_frame.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border: 2px solid #5E5E5E;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                box-shadow: 5px 5px 15px #121212, -5px -5px 15px #2A2A2A;
            }
        """)
        self.device1_layout = QtWidgets.QVBoxLayout()
        self.device1_label = QtWidgets.QLabel('Наушники 1: не подключены')
        self.device1_layout.addWidget(self.device1_label)
        self.device1_frame.setLayout(self.device1_layout)
        layout.addWidget(self.device1_frame)

        self.device2_frame = QtWidgets.QFrame()
        self.device2_frame.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border: 2px solid #5E5E5E;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                box-shadow: 5px 5px 15px #121212, -5px -5px 15px #2A2A2A;
            }
        """)
        self.device2_layout = QtWidgets.QVBoxLayout()
        self.device2_label = QtWidgets.QLabel('Наушники 2: не подключены')
        self.device2_layout.addWidget(self.device2_label)
        self.device2_frame.setLayout(self.device2_layout)
        layout.addWidget(self.device2_frame)

        btn_frame = QtWidgets.QHBoxLayout()

        self.scan_button = QtWidgets.QPushButton('Сканировать устройства')
        self.scan_button.clicked.connect(self.open_device_scanner)
        btn_frame.addWidget(self.scan_button)

        layout.addLayout(btn_frame)
        self.tab1.setLayout(layout)

    def create_battery_tab(self):
        layout = QtWidgets.QVBoxLayout()

        self.battery_button1 = QtWidgets.QPushButton('Уровень заряда наушников 1')
        self.battery_button1.clicked.connect(lambda: self.open_battery_window(1))
        layout.addWidget(self.battery_button1)

        self.battery_button2 = QtWidgets.QPushButton('Уровень заряда наушников 2')
        self.battery_button2.clicked.connect(lambda: self.open_battery_window(2))
        layout.addWidget(self.battery_button2)

        self.tab2.setLayout(layout)

    def create_settings_tab(self):
        layout = QtWidgets.QVBoxLayout()

        self.settings_label = QtWidgets.QLabel('Настройки')
        self.settings_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.settings_label)

        self.tab3.setLayout(layout)

    def open_device_scanner(self):
        self.device_scanner = DeviceScanner(self.loop)
        self.device_scanner.device_selected.connect(self.connect_device)
        self.device_scanner.show()

    def open_battery_window(self, headset_number):
        if headset_number == 1:
            device_name, device_address = self.device1_name, self.device1_address
        else:
            device_name, device_address = self.device2_name, self.device2_address

        if device_address:
            self.battery_window = BatteryLevelWindow(device_name, device_address, self.loop)
            self.battery_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Устройство не подключено", f"Наушники {headset_number} не подключены.")

    def connect_device(self, device):
        try:
            self.loop.run_until_complete(self.connect(device.address, device.name))
            self.setup_virtual_audio_sink()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться к {device.address}: {e}")

    async def connect(self, address, name):
        async with BleakClient(address) as client:
            connected = await client.is_connected()
            if connected:
                battery_level = await self.get_battery_level(client)
                if not self.device1_address:
                    self.device1_name, self.device1_address, self.device1_battery = name, address, battery_level
                    self.device1_label.setText(f'Наушники 1: {name} - {battery_level}%')
                else:
                    self.device2_name, self.device2_address, self.device2_battery = name, address, battery_level
                    self.device2_label.setText(f'Наушники 2: {name} - {battery_level}%')

                await client.disconnect()
            else:
                raise Exception("Не удалось подключиться к устройству")

    async def get_battery_level(self, client):
        battery_level = 0
        try:
            battery_level = await client.read_gatt_char("00002a19-0000-1000-8000-00805f9b34fb")
            return battery_level[0]
        except Exception as e:
            print(f"Не удалось получить уровень заряда: {e}")
        return battery_level

    def setup_virtual_audio_sink(self):
        try:
            subprocess.run(['pactl', 'load-module', 'module-loopback', 'latency_msec=1'], check=True)
            subprocess.run(['pavucontrol'], check=True)
            QtWidgets.QMessageBox.information(self, "Настройка звука", "Пожалуйста, используйте pavucontrol для настройки звука на оба устройства.")
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка настройки звука", f"Не удалось настроить звук: {e}")

class DeviceScanner(QtWidgets.QWidget):
    device_selected = QtCore.pyqtSignal(object)

    def __init__(self, loop):
        super().__init__()
        self.loop = loop
        self.devices = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Сканирование устройств')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border-radius: 20px;
                padding: 20px;
            }
            QLabel {
                color: white;
                font-size: 18px;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #3E3E3E;
                border: 2px solid #5E5E5E;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                color: white;
                box-shadow: 5px 5px 15px #121212, -5px -5px 15px #2A2A2A;
            }
            QPushButton:hover {
                background-color: #4E4E4E;
                border: 2px solid #6E6E6E;
            }
            QListWidget {
                background-color: #2E2E2E;
                border: 2px solid #5E5E5E;
                border-radius: 15px;
                padding: 20px;
                color: white;
                font-size: 16px;
                box-shadow: 5px 5px 15px #121212, -5px -5px 15px #2A2A2A;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Найденные устройства:')
        layout.addWidget(self.label)

        self.list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.list_widget)

        self.scan_button = QtWidgets.QPushButton('Начать сканирование')
        self.scan_button.clicked.connect(self.scan_devices)
        layout.addWidget(self.scan_button)

        self.setLayout(layout)

    def scan_devices(self):
        self.list_widget.clear()
        self.devices = self.loop.run_until_complete(BleakScanner.discover())
        for device in self.devices:
            self.list_widget.addItem(f'{device.name} - {device.address}')
        self.list_widget.itemDoubleClicked.connect(self.device_selected_handler)

    def device_selected_handler(self, item):
        address = item.text().split(' - ')[-1]
        for device in self.devices:
            if device.address == address:
                self.device_selected.emit(device)
                self.close()

class BatteryLevelWindow(QtWidgets.QWidget):
    def __init__(self, device_name, device_address, loop):
        super().__init__()
        self.device_name = device_name
        self.device_address = device_address
        self.loop = loop
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Уровень заряда: {self.device_name}')
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border-radius: 20px;
                padding: 20px;
            }
            QLabel {
                color: white;
                font-size: 18px;
                margin-bottom: 20px;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        self.battery_label = QtWidgets.QLabel('Уровень заряда: неизвестно')
        layout.addWidget(self.battery_label)

        self.setLayout(layout)
        self.check_battery_level()

    def check_battery_level(self):
        async def get_battery_level():
            async with BleakClient(self.device_address) as client:
                battery_level = await client.read_gatt_char("00002a19-0000-1000-8000-00805f9b34fb")
                return battery_level[0]

        try:
            battery_level = self.loop.run_until_complete(get_battery_level())
            self.battery_label.setText(f'Уровень заряда: {battery_level}%')
        except Exception as e:
            self.battery_label.setText('Уровень заряда: неизвестно')
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось получить уровень заряда: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BluetoothHeadsetConnector()
    window.show()
    sys.exit(app.exec())
