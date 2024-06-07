import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QMenuBar, QLabel, QComboBox, QLineEdit


class Demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.setupMainWindow()

    def initializeUI(self):
        self.setWindowTitle('Demo')
        self.setFixedSize(600, 400)

    def setupMainWindow(self):
        self.createActions()  # Create actions before setting up the menu bar
        self.setupMenuBar()  # Call setupMenuBar to create and add to layout

        core_layout = QGridLayout()




        email_providers = ['Gmail', 'Outlook', 'Yahoo']

        email_provider_head_l = QLabel('Email Provider Settings')

        email_provider_cb_l = QLabel('Email Provider:')
        email_provider_cb = QComboBox()
        email_provider_cb.addItems(email_providers)

        email_login_l = QLabel('Login Email:')
        email_login_le = QLineEdit()
        email_login_le.setPlaceholderText("JohnDoe@gmail.com")
        email_login_le.setFixedWidth(175)

        email_pass_l = QLabel('Email Password:')
        email_pass_le = QLineEdit()
        email_pass_le.setFixedWidth(175)

        email_recip_l = QLabel('Recipients Email:')
        email_recip_le = QLineEdit()
        email_recip_le.setFixedWidth(175)

        crypto_settings_head_l = QLabel('Cryptocurrency Settings')






        core_layout.addWidget(email_provider_head_l, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        core_layout.addWidget(crypto_settings_head_l, 0, 3, 1, 2, Qt.AlignmentFlag.AlignCenter)


        core_layout.addWidget(email_provider_cb_l, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        core_layout.addWidget(email_provider_cb, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        core_layout.addWidget(email_login_l, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        core_layout.addWidget(email_login_le, 2, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)

        core_layout.addWidget(email_pass_l, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        core_layout.addWidget(email_pass_le, 3, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)


        core_layout.addWidget(email_recip_l, 4, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        core_layout.addWidget(email_recip_le, 4, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)


        wid = QWidget()
        wid.setLayout(core_layout)
        self.setCentralWidget(wid)

    def setupMenuBar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        # Create File menu and add actions
        file_menu = menubar.addMenu("File")
        file_menu.addSeparator()  # Add a separator line
        file_menu.addAction(self.minimize_action)
        file_menu.addAction(self.exit_action)

        # Create Edit menu and add actions
        edit_menu = menubar.addMenu("Edit")

    def createActions(self):
        # File actions
        self.exit_action = QAction(QIcon(), "Exit", self)
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)

        self.minimize_action = QAction(QIcon(), "Minimize", self)
        self.minimize_action.setStatusTip("Minimize the application")
        self.minimize_action.triggered.connect(self.showMinimized)


def main():
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
