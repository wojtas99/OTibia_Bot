from Addresses import icon_image, coordinates_x, coordinates_y
import win32gui
import base64
import time
from threading import Thread
import win32api
import win32con

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QListWidget, QComboBox, QPushButton, QListWidgetItem,
    QLabel, QCheckBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from Functions.GeneralFunctions import delete_item
from Functions.MouseFunctions import right_click, left_click
from Functions.MemoryFunctions import *

class SmartHotkeysTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)) else QIcon()
        )

        # Set Title and Size
        self.setWindowTitle("Smart Hotkeys")
        self.setFixedSize(300, 200)  # Increased to fit the status label and checkbox

        self.X = 0
        self.Y = 0

        # --- Status label at the bottom
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # Main layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # List Widgets
        self.smart_hotkeys_list_widget = QListWidget(self)
        self.smart_hotkeys_list_widget.setFixedHeight(60)
        # Double-click to delete item
        self.smart_hotkeys_list_widget.itemDoubleClicked.connect(
            lambda item: delete_item(self.smart_hotkeys_list_widget, item)
        )

        # Combo Boxes
        self.rune_option_combobox = QComboBox(self)
        self.rune_option_combobox.addItems(["With Crosshair", "On Target", "On Yourself"])

        self.hotkey_option_combobox = QComboBox(self)
        for i in range(1, 13):
            self.hotkey_option_combobox.addItem(f"F{i}")

        # Buttons
        self.coordinates_button = QPushButton("Coordinates", self)
        add_smart_hotkey_button = QPushButton("Add", self)

        # Checkbox: Start Smart Hotkeys
        self.start_hotkeys_checkbox = QCheckBox("Start Smart Hotkeys", self)

        # Button functions
        add_smart_hotkey_button.clicked.connect(self.add_smart_hotkey)
        self.coordinates_button.clicked.connect(self.set_coordinates)

        # Checkbox function
        self.start_hotkeys_checkbox.stateChanged.connect(self.start_smart_hotkeys)

        # Add Widgets to Layout
        self.layout.addWidget(self.smart_hotkeys_list_widget, 0, 0, 1, 3)
        self.layout.addWidget(self.rune_option_combobox, 1, 0)
        self.layout.addWidget(self.hotkey_option_combobox, 1, 1)
        self.layout.addWidget(self.coordinates_button, 1, 2)
        self.layout.addWidget(add_smart_hotkey_button, 2, 2)

        # Place the checkbox in row 2, col 0..1
        self.layout.addWidget(self.start_hotkeys_checkbox, 2, 0, 1, 2)

        # Finally, add the status label in row 3 (spanning all columns)
        self.layout.addWidget(self.status_label, 3, 0, 1, 3)

    def add_smart_hotkey(self):
        """
        Adds a new smart hotkey with selected hotkey, option, and coordinates,
        highlighting errors and displaying status messages inline.
        """
        # Clear previous status/message styles
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.coordinates_button.setStyleSheet("")

        # Check if coordinates were set (default 0,0 might be invalid)
        if self.X == 0 and self.Y == 0:
            self.coordinates_button.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please set coordinates before adding a hotkey.")
            return

        # If valid, proceed
        smart_hotkey_data = {
            "Hotkey": self.hotkey_option_combobox.currentText(),
            "Option": self.rune_option_combobox.currentText(),
            "X": self.X,
            "Y": self.Y
        }
        hotkey_item = QListWidgetItem(smart_hotkey_data["Hotkey"])
        hotkey_item.setData(Qt.UserRole, smart_hotkey_data)
        self.smart_hotkeys_list_widget.addItem(hotkey_item)

        # Show success in green
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Smart hotkey added successfully!")

    def set_coordinates(self):
        """
        Starts the thread to capture and set the current mouse coordinates.
        """
        self.status_label.setText("")
        self.coordinates_button.setStyleSheet("color: red; font-weight: bold;")
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
            # If the left mouse button is pressed, finalize coordinates
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:
                self.coordinates_button.setStyleSheet("")
                self.coordinates_button.setText('Coordinates')
                return
            time.sleep(0.05)

    def start_smart_hotkeys(self):
        """
        Called when the 'Start Smart Hotkeys' checkbox is toggled.
        If checked, start the thread. If unchecked, the thread loop will end.
        """
        if self.start_hotkeys_checkbox.checkState() == 2:
            thread = Thread(target=self.smart_hotkeys_thread)
            thread.daemon = True
            thread.start()

    def smart_hotkeys_thread(self):
        """
        Thread that listens for hotkey presses and triggers corresponding actions.
        Runs in an infinite loop to detect asynchronous key presses, but only
        while the checkbox is checked.
        """
        while self.start_hotkeys_checkbox.checkState() == 2:
            for index in range(self.smart_hotkeys_list_widget.count()):
                hotkey_data = self.smart_hotkeys_list_widget.item(index).data(Qt.UserRole)
                # Hotkey "F1..F12" => VK codes for F1..F12 = 112..123
                # Parse the number from "F1" => "1" => code = 111 + 1 = 112
                hotkey_number = int(hotkey_data['Hotkey'][1:])
                vk_code = 111 + hotkey_number  # F1 => 112, F2 => 113, etc.

                # Check if that key was just pressed
                if win32api.GetAsyncKeyState(vk_code) & 1:
                    # Right-click the stored coordinates
                    right_click(hotkey_data['X'], hotkey_data['Y'])

                    if hotkey_data['Option'] == 'On Target':
                        target_id = read_memory_address(Addresses.attack_address, 0, 2)
                        if target_id:
                            # If there's a target, left click on it
                            target_x, target_y, target_name, target_hp = read_target_info()
                            x, y, z = read_my_wpt()
                            dx = (target_x - x) * 75
                            dy = (target_y - y) * 75
                            left_click(coordinates_x[0] + dx, coordinates_y[0] + dy)
                    elif hotkey_data['Option'] == 'On Yourself':
                        # After right-click, left-click your own character
                        left_click(coordinates_x[0], coordinates_y[0])
            time.sleep(0.05)
