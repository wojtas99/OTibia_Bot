import Addresses
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton)
from PyQt5.QtGui import QIcon
from General.MainWindowTab import MainWindowTab


class SelectTibiaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window = None

        # Set window icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        self.setWindowTitle("EasyBot Select Client")
        self.setFixedWidth(300)

        # Layout
        self.layout = QGridLayout(self)

        # Buttons
        self.ots_button = QPushButton('Your Ots', self)
        # Buttons Functions
        self.ots_button.clicked.connect(self.load_tibia_button)

        # Add widgets to layout
        self.layout.addWidget(self.ots_button)

    def load_tibia_button(self) -> None:
        Addresses.load_tibia()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()


