from Addresses import screen_x, screen_y, screen_width, screen_height, coordinates_x, coordinates_y
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox,
    QGridLayout, QPushButton, QListWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os

from Functions.GeneralFunctions import manage_profile
from Settings.SettingsThread import SettingsThread


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.settings_thread = None

        # Load Icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Settings")
        self.setFixedSize(350, 340)

        # --- Status label at the bottom (for messages, instructions, and showing coordinates)
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # List Widget for profiles
        self.profile_listWidget = QListWidget(self)

        # Line Edit for profile name
        self.profile_lineEdit = QLineEdit(self)

        # Main layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize sections
        self.set_environment()
        self.set_tools()
        self.profileList()

        # Finally, add the status label in row=2 (bottom)
        self.layout.addWidget(self.status_label, 2, 0, 1, 2)

        for file in os.listdir("Save/Settings"):
            if file.endswith(".json"):
                self.profile_listWidget.addItem(file.split('.')[0])

    def set_environment(self) -> None:
        """
        GroupBox for environment settings, like setting character position or loot screen area.
        """
        groupbox = QGroupBox("Environment", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        set_character_pos_button = QPushButton("Set Character", self)
        set_loot_screen_button = QPushButton("Set Loot Area", self)

        # Button functions
        set_character_pos_button.clicked.connect(lambda: self.startSet_thread(0))
        set_loot_screen_button.clicked.connect(lambda: self.startSet_thread(-1))

        groupbox_layout.addWidget(set_character_pos_button)
        groupbox_layout.addWidget(set_loot_screen_button)

        self.layout.addWidget(groupbox, 0, 0)

    def set_tools(self) -> None:
        """
        GroupBox for setting backpack/tools coordinates (rope, shovel, runes, etc.).
        """
        groupbox = QGroupBox("Tools", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        item_bp_button = QPushButton("1 Backpack", self)
        item_bp1_button = QPushButton("2 Backpack", self)
        item_bp2_button = QPushButton("3 Backpack", self)
        item_bp3_button = QPushButton("4 Backpack", self)
        rune1_button = QPushButton("First Rune", self)
        health_button = QPushButton("Health", self)
        mana_button = QPushButton("Mana", self)
        rune2_button = QPushButton("Second Rune", self)
        rope_button = QPushButton("Rope", self)
        shovel_button = QPushButton("Shovel", self)

        # Button -> coordinate index mapping
        item_bp_button.clicked.connect(lambda: self.startSet_thread(1))
        item_bp1_button.clicked.connect(lambda: self.startSet_thread(2))
        item_bp2_button.clicked.connect(lambda: self.startSet_thread(3))
        item_bp3_button.clicked.connect(lambda: self.startSet_thread(4))
        health_button.clicked.connect(lambda: self.startSet_thread(5))
        mana_button.clicked.connect(lambda: self.startSet_thread(11))
        rune1_button.clicked.connect(lambda: self.startSet_thread(6))
        rune2_button.clicked.connect(lambda: self.startSet_thread(8))
        shovel_button.clicked.connect(lambda: self.startSet_thread(9))
        rope_button.clicked.connect(lambda: self.startSet_thread(10))

        # Layout arrangement
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)

        layout1.addWidget(item_bp_button)
        layout1.addWidget(item_bp1_button)

        layout2.addWidget(item_bp2_button)
        layout2.addWidget(item_bp3_button)

        layout3.addWidget(health_button)
        layout3.addWidget(mana_button)

        layout4.addWidget(rune1_button)
        layout4.addWidget(rune2_button)

        layout5.addWidget(rope_button)
        layout5.addWidget(shovel_button)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)

        self.layout.addWidget(groupbox, 0, 1, 2, 1)

    def profileList(self) -> None:
        """
        GroupBox for saving and loading settings from JSON profiles.
        """
        groupbox = QGroupBox("Save && Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        save_button = QPushButton("Save", self)
        load_button = QPushButton("Load", self)

        save_button.clicked.connect(self.save_profile)
        load_button.clicked.connect(self.load_profile)

        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.profile_lineEdit)
        layout2.addWidget(save_button)
        layout2.addWidget(load_button)

        groupbox_layout.addWidget(self.profile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)

        self.layout.addWidget(groupbox, 1, 0)

    def save_profile(self) -> None:
        profile_name = self.profile_lineEdit.text().strip()
        if not profile_name:
            return
        screen_data = {
            "screenX": screen_x[0],
            "screenY": screen_y[0],
            "screenWidth": screen_width[0],
            "screenHeight": screen_height[0],
            "X": coordinates_x,
            "Y": coordinates_y
        }
        data_to_save = {"screen_data": screen_data}

        if manage_profile("save", "Save/Settings", profile_name, data_to_save):
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.status_label.setText(f"Profile '{profile_name}' has been saved!")
            existing_names = [
                self.profile_listWidget.item(i).text()
                for i in range(self.profile_listWidget.count())
            ]
            if profile_name not in existing_names:
                self.profile_listWidget.addItem(profile_name)

    def load_profile(self) -> None:
        profile_name = self.profile_listWidget.currentItem()
        if not profile_name:
            self.profile_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list to load.")
            return
        else:
            self.profile_listWidget.setStyleSheet("")

        profile_name = profile_name.text()
        filename = f"Save/Settings/{profile_name}.json"
        with open(filename, "r") as f:
            loaded_data = json.load(f)

        settings_data = loaded_data.get("screen_data", {})
        screen_x[0] = settings_data.get("screenX", 0)
        screen_y[0] = settings_data.get("screenY", 0)
        screen_width[0] = settings_data.get("screenWidth", 0)
        screen_height[0] = settings_data.get("screenHeight", 0)

        bp_data_x = settings_data.get("X", [0] * len(coordinates_x))
        bp_data_y = settings_data.get("Y", [0] * len(coordinates_y))

        for i in range(len(coordinates_x)):
            coordinates_x[i] = bp_data_x[i]
            coordinates_y[i] = bp_data_y[i]

        self.profile_lineEdit.clear()
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' loaded successfully!")

    def startSet_thread(self, index) -> None:
        self.settings_thread = SettingsThread(index, self.status_label)
        self.settings_thread.start()
