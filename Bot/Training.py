import Addresses
from Addresses import icon_image
import base64
from PyQt5.QtCore import Qt
import random
import time
from threading import Thread
import win32api
import win32con
import win32gui
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap

from Functions import read_my_stats
from MemoryFunctions import read_pointer_address
from KeyboardFunctions import press_hotkey
from MouseFunctions import right_click
from TrainingThread import TrainingThread


class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.training_thread = None

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Training")
        self.setFixedSize(300, 200)

        # Check Boxes
        self.burn_mana_checkbox = QCheckBox("Burn Mana", self)
        self.start_fishing_checkbox = QCheckBox("Start Fishing", self)
        self.start_eat_checkbox = QCheckBox("Eat Food", self)

        # Combo Boxes
        self.hotkey_list_combobox = QComboBox(self)

        # Line Edits
        self.mp_line_edit = QLineEdit(self)

        # List Widgets
        self.burn_mana_list_widget = QListWidget(self)

        # Buttons
        self.fishing_rod_button = QPushButton("FishingRod", self)
        self.water_button = QPushButton("Water", self)
        self.add_food_button = QPushButton("Food", self)

        # Other Variables
        self.food_x = 0
        self.food_y = 0
        self.water_x = 0
        self.water_y = 0
        self.fishing_rod_x = 0
        self.fishing_rod_y = 0

        # Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize
        self.burn_mana_list()
        self.add_hotkeys()
        self.fishing()
        self.eat_food()

    def burn_mana_list(self) -> None:
        groupbox = QGroupBox("Burn Mana")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Add Layouts
        groupbox_layout.addWidget(self.burn_mana_list_widget)
        self.layout.addWidget(groupbox, 0, 0, 1, 1)

    def add_hotkeys(self) -> None:
        groupbox = QGroupBox("Hotkeys")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        add_hotkey_button = QPushButton("Add", self)

        # Button functions
        add_hotkey_button.clicked.connect(self.add_hotkey)

        # Check Boxes
        self.burn_mana_checkbox.stateChanged.connect(self.start_training_thread)

        # Combo Boxes
        for i in range(1, 11):
            self.hotkey_list_combobox.addItem(f"F{i}")

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.mp_line_edit)
        layout1.addWidget(self.hotkey_list_combobox)
        layout1.addWidget(add_hotkey_button)
        layout2.addWidget(self.burn_mana_checkbox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 1)

    def fishing(self) -> None:
        groupbox = QGroupBox("Fishing")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button functions
        self.fishing_rod_button.clicked.connect(lambda: self.set_coordinates(0))
        self.water_button.clicked.connect(lambda: self.set_coordinates(1))

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.fishing_rod_button)
        layout1.addWidget(self.water_button)
        layout2.addWidget(self.start_fishing_checkbox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 1)

    def eat_food(self) -> None:
        groupbox = QGroupBox("Food")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button functions
        self.add_food_button.clicked.connect(lambda: self.set_coordinates(2))

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.add_food_button)
        layout2.addWidget(self.start_eat_checkbox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 0)

    def add_hotkey(self) -> None:
        hotkey_name = self.hotkey_list_combobox.currentText()
        hotkey_data = {"Mana": int(self.mp_line_edit.text())}
        hotkey = QListWidgetItem(hotkey_name)
        hotkey.setData(Qt.UserRole, hotkey_data)
        self.burn_mana_list_widget.addItem(hotkey)
        self.mp_line_edit.clear()

    def set_coordinates(self, index):
        thread = Thread(target=self.set_coordinates_thread, args=(index,))
        thread.daemon = True
        thread.start()

    def set_coordinates_thread(self, index) -> None:
        while True:
            x, y = win32api.GetCursorPos()
            if index == 0:
                self.fishing_rod_button.setText(f"{x, y}")
            elif index == 1:
                self.water_button.setText(f"{x, y}")
            else:
                self.add_food_button.setText(f"{x, y}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:
                x, y = win32gui.ScreenToClient(Addresses.game, (x, y))
                if index == 0:
                    self.fishing_rod_button.setText("FishingRod")
                    self.fishing_rod_x = x
                    self.fishing_rod_y = y
                elif index == 1:
                    self.water_button.setText("Water")
                    self.water_x = x
                    self.water_y = y
                else:
                    self.add_food_button.setText("Food")
                    self.food_x = x
                    self.food_y = y
                return

    def start_training_thread(self, state) -> None:
        if state == Qt.Checked:
            if not self.training_thread:
                self.training_thread = TrainingThread(self.burn_mana_list_widget)
                self.training_thread.start()
        else:
            if self.training_thread:
                self.training_thread.stop()
                self.training_thread = None

