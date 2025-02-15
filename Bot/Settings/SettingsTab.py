import win32gui
import Addresses
from Addresses import icon_image, screen_x, screen_y, screen_width, screen_height, coordinates_x, coordinates_y
import base64
import json
import time
from threading import Thread
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox,
    QGridLayout, QPushButton, QListWidget
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import win32api
from win32con import VK_LBUTTON
import os

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super(SettingsTab, self).__init__(parent)

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)) else QIcon()
        )

        # Set Title and Size
        self.setWindowTitle("Settings")
        self.setFixedSize(350, 340)

        # --- Status label at the bottom (for messages, instructions, and showing coordinates)
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # List Widget for profiles
        self.settings_profile_list_widget = QListWidget(self)

        # Line Edit for profile name
        self.settings_line_edit = QLineEdit(self)

        # Main layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize sections
        self.set_environment()
        self.set_tools()
        self.save_load_settings()

        # Finally, add the status label in row=2 (bottom)
        self.layout.addWidget(self.status_label, 2, 0, 1, 2)

    def set_environment(self) -> None:
        """
        GroupBox for environment settings, like setting character position or loot screen area.
        """
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
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(set_character_pos_button)
        layout2.addWidget(set_loot_screen_button)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)

        self.layout.addWidget(groupbox, 0, 0)

    def set_tools(self) -> None:
        """
        GroupBox for setting backpack/tools coordinates (rope, shovel, runes, etc.).
        """
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

        # Button -> coordinate index mapping
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

        # Layout arrangement
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()

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

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)

        self.layout.addWidget(groupbox, 0, 1, 2, 1)

    def save_load_settings(self) -> None:
        """
        GroupBox for saving and loading settings from JSON profiles.
        """
        groupbox = QGroupBox("Save && Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        save_settings_button = QPushButton("Save", self)
        load_settings_button = QPushButton("Load", self)

        save_settings_button.clicked.connect(self.save_settings)
        load_settings_button.clicked.connect(self.load_settings)

        for file in os.listdir("Save/Settings"):
            if file.endswith(".json"):
                self.settings_profile_list_widget.addItem(file.split('.')[0])

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.settings_line_edit)
        layout2.addWidget(save_settings_button)
        layout2.addWidget(load_settings_button)

        groupbox_layout.addWidget(self.settings_profile_list_widget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)

        self.layout.addWidget(groupbox, 1, 0)

    def set_screen(self, index: int):
        """
        Start a thread to capture two clicks for defining a rectangle (top-left, bottom-right).
        This rectangle is for a 'loot' area or similar.
        """
        thread = Thread(target=self.set_screen_thread, args=(index,))
        thread.daemon = True
        thread.start()

    def set_coordinates(self, index: int):
        """
        Start a thread to capture a single coordinate (character position or a tool slot).
        """
        thread = Thread(target=self.set_coordinates_thread, args=(index,))
        thread.daemon = True
        thread.start()

    def set_screen_thread(self, index: int):
        """
        Capture top-left coordinate on first click,
        then bottom-right coordinate on second click,
        storing them in screen_x/y and screen_width/height.
        """
        # First corner
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")

        while True:
            # Show current cursor position
            cur_x, cur_y = win32api.GetCursorPos()
            self.status_label.setText(
                f"Top-left X={cur_x}  Y={cur_y}"
            )
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                # Mark top-left done
                screen_x[index], screen_y[index] = cur_x, cur_y
                break

        time.sleep(0.2)
        # Second corner
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        while True:
            # Show current cursor position
            cur_x, cur_y = win32api.GetCursorPos()
            self.status_label.setText(
                f"Bottom-right X={cur_x}  Y={cur_y}"
            )
            time.sleep(0.05)
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                # Mark bottom-right done
                screen_width[index], screen_height[index] = cur_x, cur_y
                # Convert to client coords
                screen_x[index], screen_y[index] = win32gui.ScreenToClient(
                    Addresses.game, (screen_x[index], screen_y[index])
                )
                screen_width[index], screen_height[index] = win32gui.ScreenToClient(
                    Addresses.game, (screen_width[index], screen_height[index])
                )
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.status_label.setText("Screen area set successfully!")
                return

    def set_coordinates_thread(self, index: int):
        """
        Capture a single coordinate, e.g., the character position (index=0)
        or a tool slot (index > 0).
        """
        if index == 0:
            self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: blue; font-weight: bold;")

        while True:
            # Show current cursor position
            cur_x, cur_y = win32api.GetCursorPos()
            self.status_label.setText(
                f"Current: X={cur_x}  Y={cur_y}"
            )
            time.sleep(0.05)

            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                # Convert to client coords
                coordinates_x[index], coordinates_y[index] = win32gui.ScreenToClient(
                    Addresses.game, (cur_x, cur_y)
                )
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.status_label.setText(f"Coordinates set at X={coordinates_x[index]}, Y={coordinates_y[index]}")
                return

    def save_settings(self) -> None:
        """
        Save the current screen and tool coordinates to a JSON file,
        using the name from settings_line_edit. Show errors/success in status_label.
        """
        # Reset status
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.settings_line_edit.setStyleSheet("")

        settings_name = self.settings_line_edit.text().strip()
        if not settings_name:
            # If empty, highlight and display error
            self.settings_line_edit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a profile name before saving.")
            return

        # Check if name already in list
        existing_names = [
            self.settings_profile_list_widget.item(i).text().upper()
            for i in range(self.settings_profile_list_widget.count())
        ]
        if settings_name.upper() in existing_names:
            self.status_label.setText("Profile name already exists, choose a different one.")
            return

        screen_data = {
            "screenX": screen_x[0],
            "screenY": screen_y[0],
            "screenWidth": screen_width[0],
            "screenHeight": screen_height[0],
            "bpX": coordinates_x,
            "bpY": coordinates_y
        }
        settings_data = {"screen_data": screen_data}

        os.makedirs("", exist_ok=True)
        with open(f"Save/Settings/{settings_name}.json", "w") as f:
            json.dump(settings_data, f, indent=4)

        self.settings_profile_list_widget.addItem(settings_name)
        self.settings_line_edit.clear()

        # Success
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Settings '{settings_name}' saved successfully!")

    def load_settings(self) -> None:
        """
        Load a profile from the list. If none selected, highlight list; otherwise load and show success.
        """
        # Clear status
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.settings_profile_list_widget.setStyleSheet("")

        current_item = self.settings_profile_list_widget.currentItem()
        if not current_item:
            self.settings_profile_list_widget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list to load.")
            return

        settings_name = current_item.text()
        filename = f"Save/Settings/{settings_name}.json"
        if not os.path.exists(filename):
            self.settings_profile_list_widget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText(f"No file found for profile '{settings_name}'.")
            return

        with open(filename, "r") as f:
            settings_list = json.load(f)
        settings_data = settings_list.get("screen_data", {})

        screen_x[0] = settings_data.get("screenX", 0)
        screen_y[0] = settings_data.get("screenY", 0)
        screen_width[0] = settings_data.get("screenWidth", 0)
        screen_height[0] = settings_data.get("screenHeight", 0)

        bp_data_x = settings_data.get("bpX", [0]*len(coordinates_x))
        bp_data_y = settings_data.get("bpY", [0]*len(coordinates_y))

        for i in range(len(coordinates_x)):
            coordinates_x[i] = bp_data_x[i]
            coordinates_y[i] = bp_data_y[i]

        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Settings '{settings_name}' loaded successfully!")
