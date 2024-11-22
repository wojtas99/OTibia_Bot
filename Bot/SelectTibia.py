import Addresses
import base64
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QPushButton
)
from PyQt5.QtGui import QIcon, QPixmap
from Addresses import icon_image
from MainWindow import MainWindowTab


class SelectTibiaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window = None

        # Set window icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())
        self.setWindowTitle("EasyBot Select Client")
        self.setFixedSize(300, 150)

        # Layout
        self.layout = QGridLayout(self)

        # Buttons
        self.altaron_button = QPushButton('Altaron', self)
        self.wad_button = QPushButton('We Are Dragons', self)
        self.medivia_button = QPushButton('Medivia', self)
        self.realera_button = QPushButton('Realera', self)
        # Buttons Functions
        self.wad_button.clicked.connect(self.load_wad_button)
        self.medivia_button.clicked.connect(self.load_medivia_button)
        self.altaron_button.clicked.connect(self.load_altaron_button)
        self.realera_button.clicked.connect(self.load_realera_button)

        # Add widgets to layout
        self.layout.addWidget(self.altaron_button)
        self.layout.addWidget(self.wad_button)
        self.layout.addWidget(self.medivia_button)
        self.layout.addWidget(self.realera_button)

    def load_wad_button(self) -> None:
        Addresses.load_wad()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()

    def load_medivia_button(self) -> None:
        Addresses.load_medivia()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()

    def load_altaron_button(self) -> None:
        Addresses.load_altaron()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()

    def load_realera_button(self) -> None:
        Addresses.load_realera()
        self.close()
        self.main_window = MainWindowTab()
        self.main_window.show()



