import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QMenuBar, QLabel, QComboBox, QPushButton, QVBoxLayout, QTextEdit, QLineEdit
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
        self.start_scan()

    def initialize_ui(self):
        self.setWindowTitle('Roku Controller')
        self.setFixedSize(400, 650)  # Increased height to accommodate new buttons

    def setup_main_window(self):
        self.create_actions()
        self.setup_menu_bar()
        main_layout = QVBoxLayout()
        device_layout = QGridLayout()

        self.device_combo = QComboBox()
        self.device_combo.setPlaceholderText("Select Roku Device")
        self.scan_button = QPushButton("Scan for Devices")
        self.scan_button.clicked.connect(self.start_scan)

        device_layout.addWidget(self.device_combo, 0, 1, 1, 1)
        device_layout.addWidget(self.scan_button, 0, 2, 1, 1)
        main_layout.addLayout(device_layout)

        # Create a grid layout for the buttons
        button_layout = QGridLayout()

        # Define a list of tuples, each containing a button label and its corresponding method
        buttons = [
            ("Power", self.power_pressed),
            ("Up", self.up_pressed),
            ("Home", self.home_pressed),
            ("Left", self.left_pressed),
            ("OK", self.ok_pressed),
            ("Right", self.right_pressed),
            ("Back", self.back_pressed),
            ("Down", self.down_pressed),
            ("Mute", self.mute_pressed),
            ("Vol +", self.volume_up_pressed),
            ("Vol -", self.volume_down_pressed),
            ("Play/Pause", self.play_pause_pressed),
            ("YouTube", self.launch_youtube),
            ("Disney+", self.launch_disney),
            ("Netflix", self.launch_netflix),
        ]

        # Generate a list of grid positions for a 8x3 grid
        positions = [(i, j) for i in range(8) for j in range(3)]

        # Iterate over the positions and buttons simultaneously
        for position, (name, method) in zip(positions, buttons):
            # Create a button with the given name
            button = QPushButton(name)
            # Connect the button's click event to its corresponding method
            button.clicked.connect(method)
            # Add the button to the grid layout at the specified position
            # The * operator unpacks the position tuple into separate arguments
            button_layout.addWidget(button, *position)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search query and press Enter")
        self.search_input.returnPressed.connect(self.process_search)

        button_layout.addWidget(self.search_input, 8, 0, 1, 3)

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

    def send_command(self, command, is_launch=False, ):
        device = self.get_current_device()
        if device:
            self.display_window.append(f"Sending command: {command}")
            if is_launch:
                response = self.roku_controller._send_command(device['ip'], f"launch/{command}")
            elif command.startswith("Lit_"):
                search_query = command[4:]  # Remove "Lit_" prefix
                response = self.roku_controller._send_command(device['ip'], f"search/browse?keyword={search_query}")
            else:
                response = self.roku_controller._send_command(device['ip'], f"keypress/{command}")
            self.display_window.append(f"Response: {response}")
        else:
            self.display_window.append("No device selected")


    def process_search(self):
        query = self.search_input.text()
        if query:
            self.send_command(f"Lit_{query}")
            self.search_input.clear()
        else:
            self.display_window.append("Please enter a search query")

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
