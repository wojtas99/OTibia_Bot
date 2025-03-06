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
        self.setFixedSize(300, 150)

        # Layout
        self.layout = QGridLayout(self)

        # Buttons
        self.medivia_button = QPushButton('Medivia', self)
        self.tibiScape_button = QPushButton('TibiaScape', self)
        # Buttons Functions
        self.medivia_button.clicked.connect(self.load_medivia_button)
        self.tibiScape_button.clicked.connect(self.load_tibiaScape_button)

        # Add widgets to layout
        self.layout.addWidget(self.medivia_button)
        self.layout.addWidget(self.tibiScape_button)

    def load_medivia_button(self) -> None:
        Addresses.load_medivia()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()

    def load_tibiaScape_button(self) -> None:
        Addresses.load_tibiaScape()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()


