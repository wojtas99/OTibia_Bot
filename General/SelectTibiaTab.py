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
        self.tibiaScape_button = QPushButton('TibiaScape', self)
        self.miracle_button = QPushButton('Mircale', self)
        # Buttons Functions
        self.medivia_button.clicked.connect(self.load_medivia_button)
        self.tibiaScape_button.clicked.connect(self.load_tibiaScape_button)
        self.miracle_button.clicked.connect(self.load_miracle_button)

        # Add widgets to layout
        self.layout.addWidget(self.medivia_button)
        self.layout.addWidget(self.tibiaScape_button)
        self.layout.addWidget(self.miracle_button)

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

    def load_miracle_button(self) -> None:
        Addresses.load_miracle()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()


