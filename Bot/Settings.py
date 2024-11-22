import win32gui

from Addresses import icon_image, screen_x, screen_y, screen_width, screen_height, coordinates_x, coordinates_y
import Addresses
import base64
import json
import time
from threading import Thread
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox,
    QGridLayout, QPushButton, QListWidget
)
from PyQt5.QtGui import QIcon, QPixmap
import win32api
from win32con import VK_LBUTTON
import os


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super(SettingsTab, self).__init__(parent)

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Settings")
        self.setFixedSize(350, 300)

        # Labels
        self.tools_label = QLabel("Set", self)
        self.screen_label = QLabel("Set", self)

        self.tools_label.setFixedHeight(20)
        self.screen_label.setFixedHeight(20)

        # List Widgets
        self.settings_profile_list_widget = QListWidget(self)

        # Line Edits
        self.settings_line_edit = QLineEdit(self)

        # Layouts
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize
        self.set_tools()
        self.set_environment()
        self.save_load_settings()

    def set_tools(self) -> None:
        groupbox = QGroupBox("Tools", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        gold_bp_button = QPushButton("1 Backpack", self)
        item_bp1_button = QPushButton("2 Backpack", self)
        item_bp2_button = QPushButton("3 Backpack", self)
        item_bp3_button = QPushButton("4 Backpack", self)
        hmm_bp_button = QPushButton("HMM", self)
        uh_bp_button = QPushButton("UH", self)
        sd_bp_button = QPushButton("SD", self)
        gfb_bp_button = QPushButton("GFB", self)
        rope_button = QPushButton("Rope", self)
        shovel_button = QPushButton("Shovel", self)

        # Button functions
        gold_bp_button.clicked.connect(lambda: self.set_coordinates(1))
        item_bp1_button.clicked.connect(lambda: self.set_coordinates(2))
        item_bp2_button.clicked.connect(lambda: self.set_coordinates(3))
        item_bp3_button.clicked.connect(lambda: self.set_coordinates(4))
        uh_bp_button.clicked.connect(lambda: self.set_coordinates(5))
        hmm_bp_button.clicked.connect(lambda: self.set_coordinates(6))
        gfb_bp_button.clicked.connect(lambda: self.set_coordinates(7))
        sd_bp_button.clicked.connect(lambda: self.set_coordinates(8))
        shovel_button.clicked.connect(lambda: self.set_coordinates(9))
        rope_button.clicked.connect(lambda: self.set_coordinates(10))

        # Layouts
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.tools_label)
        layout1.addWidget(gold_bp_button)
        layout1.addWidget(item_bp1_button)
        layout2.addWidget(item_bp2_button)
        layout2.addWidget(item_bp3_button)
        layout3.addWidget(uh_bp_button)
        layout3.addWidget(hmm_bp_button)
        layout4.addWidget(sd_bp_button)
        layout4.addWidget(gfb_bp_button)
        layout5.addWidget(rope_button)
        layout5.addWidget(shovel_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)
        self.layout.addWidget(groupbox, 0, 1, 2, 1)

    def save_load_settings(self) -> None:
        groupbox = QGroupBox("Save && Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        save_settings_button = QPushButton("Save", self)
        load_settings_button = QPushButton("Load", self)

        # Button functions
        save_settings_button.clicked.connect(self.save_settings)
        load_settings_button.clicked.connect(self.load_settings)

        # Populate list widget
        for file in os.listdir("Settings"):
            self.settings_profile_list_widget.addItem(f"{file.split('.')[0]}")

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.settings_line_edit)
        layout2.addWidget(save_settings_button)
        layout2.addWidget(load_settings_button)

        # Add Layouts
        groupbox_layout.addWidget(self.settings_profile_list_widget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 0)

    def set_environment(self) -> None:
        groupbox = QGroupBox("Environment", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        set_character_pos_button = QPushButton("Set Character", self)
        set_loot_screen_button = QPushButton("Set Loot", self)

        # Button functions
        set_character_pos_button.clicked.connect(lambda: self.set_coordinates(0))
        set_loot_screen_button.clicked.connect(lambda: self.set_screen(0))

        # Layouts
        layout = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout.addWidget(self.screen_label)
        layout1.addWidget(set_character_pos_button)
        layout2.addWidget(set_loot_screen_button)

        # Add Layouts
        groupbox_layout.addLayout(layout)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 0)

    def set_screen(self, index):
        thread = Thread(target=self.set_screen_thread, args=(index,))
        thread.daemon = True
        thread.start()

    def set_coordinates(self, index):
        thread = Thread(target=self.set_coordinates_thread, args=(index,))
        thread.daemon = True
        thread.start()

    def set_screen_thread(self, index):
        self.screen_label.setStyleSheet("color: red")
        while True:
            screen_x[index], screen_y[index] = win32api.GetCursorPos()
            self.screen_label.setText(f"X = {screen_x[index]} | Y = {screen_y[index]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.screen_label.setStyleSheet("color: blue")
                break
        time.sleep(0.1)
        while True:
            screen_width[index], screen_height[index] = win32api.GetCursorPos()
            self.screen_label.setText(f"X = {screen_width[index]} | Y = {screen_height[index]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                self.screen_label.setStyleSheet("color: black")
                self.screen_label.setText("Set")
                screen_x[index], screen_y[index] = win32gui.ScreenToClient(Addresses.game, (screen_x[index], screen_y[index]))
                screen_width[index], screen_height[index] = win32gui.ScreenToClient(Addresses.game, (screen_width[index], screen_height[index]))
                return

    def set_coordinates_thread(self, index):
        if index == 0:
            self.screen_label.setStyleSheet("color: red")
        else:
            self.tools_label.setStyleSheet("color: red")
        while True:
            coordinates_x[index], coordinates_y[index] = win32api.GetCursorPos()
            if index == 0:
                self.screen_label.setText(f"X = {coordinates_x[index]} | Y = {coordinates_y[index]}")
            else:
                self.tools_label.setText(f"X = {coordinates_x[index]} | Y = {coordinates_y[index]}")
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                coordinates_x[index], coordinates_y[index] = win32gui.ScreenToClient(Addresses.game, (coordinates_x[index], coordinates_y[index]))
                if index == 0:
                    self.screen_label.setText("Set")
                    self.screen_label.setStyleSheet("color: black")
                else:
                    self.tools_label.setText("Set")
                    self.tools_label.setStyleSheet("color: black")
                return

    def save_settings(self) -> None:
        settings_name = self.settings_line_edit.text()
        for index in range(self.settings_profile_list_widget.count()):
            if settings_name.upper() == self.settings_profile_list_widget.item(index).text().upper():
                return
        if settings_name:
            screen_data = {
                "screenX": screen_x[0],
                "screenY": screen_y[0],
                "screenWidth": screen_width[0],
                "screenHeight": screen_height[0],
                "bpX": coordinates_x,
                "bpY": coordinates_y
            }
            settings_data = {
                "screen_data": screen_data
            }
            with open(f"Settings/{settings_name}.json", "w") as f:
                json.dump(settings_data, f, indent=4)
            self.settings_profile_list_widget.addItem(settings_name)
            self.settings_line_edit.clear()

    def load_settings(self) -> None:
        settings_name = self.settings_profile_list_widget.currentItem().text()
        if settings_name:
            with open(f"Settings/{settings_name}.json", "r") as f:
                settings_list = json.load(f)
            settings_data = settings_list.get("screen_data", {})
            screen_x[0] = settings_data.get("screenX")
            screen_y[0] = settings_data.get("screenY")
            screen_width[0] = settings_data.get("screenWidth")
            screen_height[0] = settings_data.get("screenHeight")
            bp_data_x = settings_data.get("bpX", [0] * 11)
            bp_data_y = settings_data.get("bpY", [0] * 11)
            for i in range(len(coordinates_x)):
                coordinates_x[i] = bp_data_x[i]
                coordinates_y[i] = bp_data_y[i]
        self.tools_label.setStyleSheet("color: green")
        self.screen_label.setStyleSheet("color: green")
        self.screen_label.setText("Loaded")
        self.tools_label.setText("Loaded")
