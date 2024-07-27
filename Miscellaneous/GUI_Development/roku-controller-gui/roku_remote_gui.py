import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QMenuBar, QLabel, QComboBox, QPushButton, QVBoxLayout, QTextEdit
)
from PyQt6.QtCore import QThread, pyqtSignal
from roku_remote_logic import RokuController

class ScanThread(QThread):
    finished = pyqtSignal(list)

    def run(self):
        controller = RokuController()
        controller.scan_network()
        self.finished.emit(controller.devices)

class RokuControllerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.roku_controller = RokuController()
        self.current_device = None
        self.initialize_ui()
        self.setup_main_window()

    def initialize_ui(self):
        self.setWindowTitle('Roku Controller')
        self.setFixedSize(400, 600)

    def setup_main_window(self):
        self.create_actions()
        self.setup_menu_bar()
        main_layout = QVBoxLayout()

        device_layout = QGridLayout()
        device_label = QLabel("Select Roku Device:")
        self.device_combo = QComboBox()
        self.scan_button = QPushButton("Scan for Devices")
        self.scan_button.clicked.connect(self.start_scan)
        device_layout.addWidget(device_label, 0, 0)
        device_layout.addWidget(self.device_combo, 0, 1)
        device_layout.addWidget(self.scan_button, 1, 0, 1, 2)
        main_layout.addLayout(device_layout)

        button_layout = QGridLayout()
        self.btn_power = QPushButton("Power")
        self.btn_home = QPushButton("Home")
        self.btn_up = QPushButton("Up")
        self.btn_left = QPushButton("Left")
        self.btn_ok = QPushButton("OK")
        self.btn_right = QPushButton("Right")
        self.btn_back = QPushButton("Back")
        self.btn_down = QPushButton("Down")
        self.btn_volume_up = QPushButton("Vol+")
        self.btn_volume_down = QPushButton("Vol-")
        self.btn_mute = QPushButton("Mute")
        self.btn_play_pause = QPushButton("Play/Pause")
        self.btn_youtube = QPushButton("YouTube")
        self.btn_disney = QPushButton("Disney+")
        self.btn_netflix = QPushButton("Netflix")
        self.btn_list_apps = QPushButton("List Apps")

        self.btn_power.clicked.connect(self.power_pressed)
        self.btn_home.clicked.connect(self.home_pressed)
        self.btn_up.clicked.connect(self.up_pressed)
        self.btn_left.clicked.connect(self.left_pressed)
        self.btn_ok.clicked.connect(self.ok_pressed)
        self.btn_right.clicked.connect(self.right_pressed)
        self.btn_back.clicked.connect(self.back_pressed)
        self.btn_down.clicked.connect(self.down_pressed)
        self.btn_volume_up.clicked.connect(self.volume_up_pressed)
        self.btn_volume_down.clicked.connect(self.volume_down_pressed)
        self.btn_mute.clicked.connect(self.mute_pressed)
        self.btn_play_pause.clicked.connect(self.play_pause_pressed)
        self.btn_youtube.clicked.connect(self.launch_youtube)
        self.btn_disney.clicked.connect(self.launch_disney)
        self.btn_netflix.clicked.connect(self.launch_netflix)
        self.btn_list_apps.clicked.connect(self.list_apps)

        button_layout.addWidget(self.btn_home, 1, 0)
        button_layout.addWidget(self.btn_up, 1, 1)
        button_layout.addWidget(self.btn_back, 1, 2)
        button_layout.addWidget(self.btn_left, 2, 0)
        button_layout.addWidget(self.btn_ok, 2, 1)
        button_layout.addWidget(self.btn_right, 2, 2)
        button_layout.addWidget(self.btn_down, 3, 1)
        button_layout.addWidget(self.btn_play_pause, 3, 2)
        button_layout.addWidget(self.btn_volume_up, 3, 0)
        button_layout.addWidget(self.btn_volume_down, 4, 0)
        button_layout.addWidget(self.btn_mute, 4, 2)
        button_layout.addWidget(self.btn_power, 4, 1)
        button_layout.addWidget(self.btn_youtube, 5, 0)
        button_layout.addWidget(self.btn_netflix, 5, 1)
        button_layout.addWidget(self.btn_disney, 5, 2)
        button_layout.addWidget(self.btn_list_apps, 6, 1)
        main_layout.addLayout(button_layout)

        self.display_window = QTextEdit()
        self.display_window.setReadOnly(True)
        main_layout.addWidget(self.display_window)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_menu_bar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        file_menu = menubar.addMenu("File")
        file_menu.addSeparator()
        file_menu.addAction(self.minimize_action)
        file_menu.addAction(self.exit_action)

    def create_actions(self):
        self.exit_action = QAction(QIcon(), "Exit", self)
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)
        self.minimize_action = QAction(QIcon(), "Minimize", self)
        self.minimize_action.setStatusTip("Minimize the application")
        self.minimize_action.triggered.connect(self.showMinimized)

    def start_scan(self):
        self.scan_button.setEnabled(False)
        self.scan_button.setText("Scanning...")
        self.scan_thread = ScanThread()
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.start()
        self.display_window.append("Scanning for Roku devices...")

    def scan_finished(self, devices):
        self.device_combo.clear()
        for device in devices:
            self.device_combo.addItem(f"{device['name']} ({device['ip']})")
        if not devices:
            self.device_combo.addItem("No devices found")
        self.scan_button.setEnabled(True)
        self.scan_button.setText("Scan for Devices")
        self.roku_controller.devices = devices
        self.display_window.append(f"Found {len(devices)} Roku device(s)")

    def get_current_device(self):
        if self.device_combo.currentIndex() >= 0:
            return self.roku_controller.devices[self.device_combo.currentIndex()]
        return None

    def send_command(self, command, is_launch=False):
        device = self.get_current_device()
        if device:
            self.display_window.append(f"Sending command: {command}")
            if is_launch:
                response = self.roku_controller._send_command(device['ip'], f"launch/{command}")
            else:
                response = self.roku_controller._send_command(device['ip'], f"keypress/{command}")
            self.display_window.append(f"Response: {response}")
        else:
            self.display_window.append("No device selected")
    def list_apps(self):
        device = self.get_current_device()
        if device:
            self.display_window.append("Listing installed apps...")
            response = self.roku_controller.list_apps(device['ip'])
            self.display_window.append(response)
        else:
            self.display_window.append("No device selected")

    def power_pressed(self):
        self.send_command("Power")

    def home_pressed(self):
        self.send_command("Home")

    def up_pressed(self):
        self.send_command("Up")

    def left_pressed(self):
        self.send_command("Left")

    def ok_pressed(self):
        self.send_command("Select")

    def right_pressed(self):
        self.send_command("Right")

    def back_pressed(self):
        self.send_command("Back")

    def down_pressed(self):
        self.send_command("Down")

    def volume_up_pressed(self):
        self.send_command("VolumeUp")

    def volume_down_pressed(self):
        self.send_command("VolumeDown")

    def mute_pressed(self):
        self.send_command("VolumeMute")

    def play_pause_pressed(self):
        self.send_command("Play")

    def launch_youtube(self):
        self.send_command("837", is_launch=True)

    def launch_disney(self):
        self.send_command("291097", is_launch=True)

    def launch_netflix(self):
        self.send_command("12", is_launch=True)

def main():
    app = QApplication(sys.argv)
    window = RokuControllerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()