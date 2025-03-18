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
        self.medivia_button = QPushButton('Medivia', self)
        self.tibiaScape_button = QPushButton('TibiaScape', self)
        self.miracle_button = QPushButton('Mircale', self)
        self.treasura_button = QPushButton('Treasura', self)
        self.dura_button = QPushButton('Dura', self)
        self.giveria_button = QPushButton('Giveria', self)
        # Buttons Functions
        self.medivia_button.clicked.connect(self.load_medivia_button)
        self.tibiaScape_button.clicked.connect(self.load_tibiaScape_button)
        self.miracle_button.clicked.connect(self.load_miracle_button)
        self.treasura_button.clicked.connect(self.load_treasura_button)
        self.dura_button.clicked.connect(self.load_dura_button)
        self.giveria_button.clicked.connect(self.load_giveria_button)

        # Add widgets to layout
        self.layout.addWidget(self.medivia_button)
        self.layout.addWidget(self.tibiaScape_button)
        self.layout.addWidget(self.miracle_button)
        self.layout.addWidget(self.treasura_button)
        self.layout.addWidget(self.dura_button)
        self.layout.addWidget(self.giveria_button)

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

    def load_treasura_button(self) -> None:
        Addresses.load_treasura()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()

    def load_dura_button(self) -> None:
        Addresses.load_dura()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()

    def load_giveria_button(self) -> None:
        Addresses.load_giveria()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()



