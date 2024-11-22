import Addresses
from Addresses import icon_image, coordinates_x, coordinates_y
import win32gui
import base64
import time
from threading import Thread
import win32api
import win32con
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QListWidget, QComboBox, QPushButton, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from Functions import read_my_wpt, read_target_info
from MouseFunctions import right_click, left_click
from MemoryFunctions import read_memory_address


class SmartHotkeysTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Smart Hotkeys")
        self.setFixedSize(300, 80)

        self.X = 0
        self.Y = 0

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # List Widgets
        self.smart_hotkeys_list_widget = QListWidget(self)
        self.smart_hotkeys_list_widget.setFixedHeight(60)

        # Combo Boxes
        self.rune_option_combobox = QComboBox(self)
        self.rune_option_combobox.addItems(["With Crosshair", "On Target", "On Yourself"])

        self.hotkey_option_combobox = QComboBox(self)
        for i in range(1, 13):
            self.hotkey_option_combobox.addItem(f"F{i}")

        # Buttons
        self.coordinates_button = QPushButton("Coordinates", self)
        add_smart_hotkey_button = QPushButton("Add", self)

        # Button functions
        add_smart_hotkey_button.clicked.connect(self.add_smart_hotkey)
        self.coordinates_button.clicked.connect(self.set_coordinates)

        # Add Widgets to Layout
        self.layout.addWidget(self.smart_hotkeys_list_widget, 0, 0)
        self.layout.addWidget(self.rune_option_combobox, 0, 1)
        self.layout.addWidget(self.hotkey_option_combobox, 0, 2)
        self.layout.addWidget(self.coordinates_button, 1, 1)
        self.layout.addWidget(add_smart_hotkey_button, 1, 2)

    def add_smart_hotkey(self):
        """
        Adds a new smart hotkey with selected hotkey, option, and coordinates.
        """
        smart_hotkey_data = {
            "Hotkey": self.hotkey_option_combobox.currentText(),
            "Option": self.rune_option_combobox.currentText(),
            "X": self.X,
            "Y": self.Y
        }
        hotkey = QListWidgetItem(self.hotkey_option_combobox.currentText())
        hotkey.setData(Qt.UserRole, smart_hotkey_data)
        self.smart_hotkeys_list_widget.addItem(hotkey)

        thread = Thread(target=self.smart_hotkeys_thread)
        thread.daemon = True
        thread.start()

    def set_coordinates(self):
        """
        Starts the thread to capture and set the current mouse coordinates.
        """
        self.coordinates_button.setStyleSheet("color: red")
        thread = Thread(target=self.set_coordinates_thread)
        thread.daemon = True
        thread.start()

    def set_coordinates_thread(self):
        """
        Captures mouse coordinates when the left mouse button is clicked.
        """
        while True:
            self.X, self.Y = win32gui.ScreenToClient(Addresses.game, win32api.GetCursorPos())
            self.coordinates_button.setText(f'{self.X} {self.Y}')
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:
                self.coordinates_button.setStyleSheet("color: black")
                self.coordinates_button.setText('Coordinates')
                return

    def smart_hotkeys_thread(self):
        """
        Thread that listens for hotkey presses and triggers corresponding actions.
        """
        while True:
            for index in range(self.smart_hotkeys_list_widget.count()):
                hotkey = self.smart_hotkeys_list_widget.item(index).data(Qt.UserRole)
                if win32api.GetAsyncKeyState(111 + int(hotkey['Hotkey'][1:])) & 1:
                    if hotkey['Option'] == 'With Crosshair':
                        right_click(hotkey['X'], hotkey['Y'])
                    elif hotkey['Option'] == 'On Target':
                        right_click(hotkey['X'], hotkey['Y'])
                        target_id = read_memory_address(Addresses.attack_address, 0, 2)
                        if target_id:
                            target_x, target_y, target_name, target_hp = read_target_info()
                            x, y, z = read_my_wpt()
                            x = target_x - x
                            y = target_y - y
                            x = x * 75
                            y = y * 75
                            left_click(x + coordinates_x[0], y + coordinates_y[0])
                    else:
                        right_click(hotkey['X'], hotkey['Y'])
                        left_click(coordinates_x[0], coordinates_y[0])
            time.sleep(0.05)
