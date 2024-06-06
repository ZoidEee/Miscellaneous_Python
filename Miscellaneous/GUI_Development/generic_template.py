import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QMenuBar, QLabel, QComboBox


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
