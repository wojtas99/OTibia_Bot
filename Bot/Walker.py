import random
import base64
import time
import json
import os
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QListWidget, QLineEdit, QTextEdit, QCheckBox, QComboBox, QVBoxLayout,
    QHBoxLayout, QGroupBox, QPushButton, QListWidgetItem, QLabel, QGridLayout
)
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator

import Addresses
from Addresses import icon_image, walker_Lock, coordinates_x, coordinates_y
from Functions import read_my_wpt, delete_item
from MemoryFunctions import read_memory_address
from KeyboardFunctions import walk
from MouseFunctions import left_click, right_click


class WalkerTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)
            ) else QIcon()
        )

        # Set Title and Size
        self.setWindowTitle("Walker")
        self.setFixedSize(350, 400)  # Increased size to fit the status label

        # --- Status label at the bottom (behaves like a "status bar")
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Widgets
        self.waypoint_list_widget = QListWidget(self)
        self.waypoint_profile_list_widget = QListWidget(self)
        self.waypoint_profile_line_edit = QLineEdit(self)
        self.action_waypoint_text_edit = QTextEdit(self)
        self.record_cave_bot_checkbox = QCheckBox("Auto Recording", self)
        self.start_cave_bot_checkbox = QCheckBox("Start Walker", self)
        self.waypoint_option_combobox = QComboBox(self)

        # Main Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize UI
        self.save_load_waypoints()
        self.waypoint_list()
        self.add_waypoints()
        self.start_walker()

        # Finally add the status label (we'll place it at the bottom row)
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

    def save_load_waypoints(self) -> None:
        groupbox = QGroupBox("Save && Load")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        save_waypoint_profile_button = QPushButton("Save")
        save_waypoint_profile_button.clicked.connect(self.save_waypoint_profile)

        load_waypoint_profile_button = QPushButton("Load")
        load_waypoint_profile_button.clicked.connect(self.load_waypoint_profile)

        # Populate list with existing profiles
        # (assuming "Waypoints" folder already exists)
        for file in os.listdir("Waypoints"):
            if file.endswith(".json"):
                self.waypoint_profile_list_widget.addItem(file.split(".")[0])

        # Layouts
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.waypoint_profile_line_edit)
        layout2.addWidget(save_waypoint_profile_button)
        layout2.addWidget(load_waypoint_profile_button)

        groupbox_layout.addWidget(self.waypoint_profile_list_widget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def waypoint_list(self) -> None:
        groupbox = QGroupBox("Waypoints")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        clear_waypoint_list_button = QPushButton("Clear List", self)
        clear_waypoint_list_button.clicked.connect(self.clear_waypoint_list)

        # Double-click to delete
        self.waypoint_list_widget.itemDoubleClicked.connect(
            lambda item: delete_item(self.waypoint_list_widget, item)
        )

        layout1 = QHBoxLayout()
        layout1.addWidget(clear_waypoint_list_button)

        groupbox_layout.addWidget(self.waypoint_list_widget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 0, 0)

    def add_waypoints(self) -> None:
        groupbox = QGroupBox("Add Waypoints")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        directions = [
            "Center", "North", "South", "East", "West",
            "North-East", "North-West", "South-East", "South-West"
        ]
        self.waypoint_option_combobox.addItems(directions)

        stand_waypoint_button = QPushButton("Stand", self)
        rope_waypoint_button = QPushButton("Rope", self)
        shovel_waypoint_button = QPushButton("Shovel", self)
        ladder_waypoint_button = QPushButton("Ladder", self)
        action_waypoint_button = QPushButton("Action", self)
        label_waypoint_button = QPushButton("Label", self)

        # Connect to add_waypoint with different indexes
        stand_waypoint_button.clicked.connect(lambda: self.add_waypoint(0))
        rope_waypoint_button.clicked.connect(lambda: self.add_waypoint(1))
        shovel_waypoint_button.clicked.connect(lambda: self.add_waypoint(2))
        ladder_waypoint_button.clicked.connect(lambda: self.add_waypoint(3))
        action_waypoint_button.clicked.connect(lambda: self.add_waypoint(4))
        label_waypoint_button.clicked.connect(lambda: self.add_waypoint(5))

        self.action_waypoint_text_edit.setFixedHeight(50)

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        layout1.addWidget(self.waypoint_option_combobox)
        layout2.addWidget(stand_waypoint_button)
        layout2.addWidget(action_waypoint_button)
        layout2.addWidget(label_waypoint_button)
        layout3.addWidget(rope_waypoint_button)
        layout3.addWidget(shovel_waypoint_button)
        layout3.addWidget(ladder_waypoint_button)
        layout4.addWidget(self.action_waypoint_text_edit)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1, 2, 1)

    def start_walker(self) -> None:
        groupbox = QGroupBox("Start")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        self.start_cave_bot_checkbox.stateChanged.connect(self.start_walker_thread)
        self.record_cave_bot_checkbox.stateChanged.connect(self.start_record_thread)

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout1.addWidget(self.start_cave_bot_checkbox)
        layout2.addWidget(self.record_cave_bot_checkbox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 1)

    def save_waypoint_profile(self) -> None:
        """
        Save the current list of waypoints to a JSON file, but first validate
        that the profile name is not empty. If empty, highlight in red and
        display an error in the status label.
        """
        # Clear previous styles/messages
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.waypoint_profile_line_edit.setStyleSheet("")

        waypoint_profile_name = self.waypoint_profile_line_edit.text().strip()
        if not waypoint_profile_name:
            # Highlight the line edit in red
            self.waypoint_profile_line_edit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a profile name before saving.")
            return

        # If valid, proceed with saving
        waypoint_list = [
            {
                "name": self.waypoint_list_widget.item(i).text(),
                "data": self.waypoint_list_widget.item(i).data(Qt.UserRole)
            }
            for i in range(self.waypoint_list_widget.count())
        ]

        os.makedirs("Waypoints", exist_ok=True)  # Just to ensure directory exists
        with open(f"Waypoints/{waypoint_profile_name}.json", "w") as f:
            json.dump(waypoint_list, f, indent=4)

        # Optionally, add it to the profile list if not already there
        existing_names = [
            self.waypoint_profile_list_widget.item(i).text()
            for i in range(self.waypoint_profile_list_widget.count())
        ]
        if waypoint_profile_name not in existing_names:
            self.waypoint_profile_list_widget.addItem(waypoint_profile_name)

        self.waypoint_profile_line_edit.clear()

        # Show success
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Waypoints saved successfully!")

    def load_waypoint_profile(self) -> None:
        """
        Loads a selected waypoint profile from JSON, if any item is selected in the list.
        Otherwise, highlight the list and show an error message.
        """
        # Clear previous styles/messages
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.waypoint_profile_list_widget.setStyleSheet("")

        current_item = self.waypoint_profile_list_widget.currentItem()
        if not current_item:
            # Highlight the list widget if nothing is selected
            self.waypoint_profile_list_widget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list to load.")
            return

        waypoint_profile_name = current_item.text()
        filename = f"Waypoints/{waypoint_profile_name}.json"
        if not os.path.exists(filename):
            self.waypoint_profile_list_widget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText(f"No file found for profile: {waypoint_profile_name}")
            return

        with open(filename, "r") as f:
            waypoint_list = json.load(f)
            self.waypoint_list_widget.clear()
            for entry in waypoint_list:
                waypoint = QListWidgetItem(entry["name"])
                waypoint.setData(Qt.UserRole, entry["data"])
                self.waypoint_list_widget.addItem(waypoint)

        # Show success
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{waypoint_profile_name}' loaded successfully.")

    def add_waypoint(self, index):
        """
        Adds a single waypoint to the list, using the current (X, Y, Z).
        If it's an Action or Label waypoint, we also check that the text
        field is not empty before adding.
        """
        x, y, z = read_my_wpt()

        waypoint_data = {
            "X": x,
            "Y": y,
            "Z": z,
            "Action": index
        }

        # Clear any previous error messages
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.action_waypoint_text_edit.setStyleSheet("")

        if index == 0:  # Stand
            waypoint_data["Direction"] = self.waypoint_option_combobox.currentIndex()
            waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')

        elif index == 1:  # Rope
            waypoint_data["Direction"] = self.waypoint_option_combobox.currentIndex()
            waypoint = QListWidgetItem(f'Rope: {x} {y} {z}')

        elif index == 2:  # Shovel
            waypoint_data["Direction"] = self.waypoint_option_combobox.currentIndex()
            waypoint = QListWidgetItem(f'Shovel: {x} {y} {z}')

        elif index == 3:  # Ladder
            waypoint_data["Direction"] = self.waypoint_option_combobox.currentIndex()
            waypoint = QListWidgetItem(f'Ladder: {x} {y} {z}')

        elif index == 4:  # Action
            action_text = self.action_waypoint_text_edit.toPlainText().strip()
            if not action_text:
                # If empty, highlight and show error
                self.action_waypoint_text_edit.setStyleSheet("border: 2px solid red;")
                self.status_label.setText("Please enter an Action text.")
                return

            waypoint_data["Direction"] = action_text
            waypoint = QListWidgetItem(f'Action: {x} {y} {z}')
            self.action_waypoint_text_edit.clear()

        elif index == 5:  # Label
            label_name = self.action_waypoint_text_edit.toPlainText().strip()
            if not label_name:
                # If empty, highlight and show error
                self.action_waypoint_text_edit.setStyleSheet("border: 2px solid red;")
                self.status_label.setText("Please enter a Label text.")
                return

            waypoint_data["Direction"] = label_name
            waypoint = QListWidgetItem(f'{label_name}: {x} {y} {z}')
            self.action_waypoint_text_edit.clear()

        # If we got here, we successfully created a waypoint
        waypoint.setData(Qt.UserRole, waypoint_data)
        self.waypoint_list_widget.addItem(waypoint)

        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Waypoint added successfully!")

    def delete_waypoint(self) -> None:
        self.waypoint_list_widget.takeItem(self.waypoint_list_widget.currentRow())

    def clear_waypoint_list(self) -> None:
        self.waypoint_list_widget.clear()
        self.status_label.setText("")  # Clear status if you want

    def start_record_thread(self) -> None:
        thread = Thread(target=self.record_waypoints)
        thread.daemon = True
        if self.record_cave_bot_checkbox.checkState() == 2:
            thread.start()

    def record_waypoints(self) -> None:
        x, y, z = read_my_wpt()

        waypoint_data = {
            "Action": 0,
            "Direction": 0,
            "X": x,
            "Y": y,
            "Z": z
        }

        waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')
        waypoint.setData(Qt.UserRole, waypoint_data)
        self.waypoint_list_widget.addItem(waypoint)

        old_x, old_y, old_z = x, y, z

        while self.record_cave_bot_checkbox.checkState():
            x, y, z = read_my_wpt()

            if (x != old_x or y != old_y) and z == old_z:
                waypoint_data = {
                    "Action": 0,
                    "Direction": 0,
                    "X": x,
                    "Y": y,
                    "Z": z
                }
                waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')
                waypoint.setData(Qt.UserRole, waypoint_data)
                self.waypoint_list_widget.addItem(waypoint)

            if z != old_z:
                if x < old_x:
                    direction = 4  # West
                elif x > old_x:
                    direction = 3  # East
                elif y > old_y:
                    direction = 2  # South
                else:
                    direction = 1  # North

                waypoint_data = {
                    "Action": 0,
                    "Direction": direction,
                    "X": x,
                    "Y": y,
                    "Z": z
                }
                waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')
                waypoint.setData(Qt.UserRole, waypoint_data)
                self.waypoint_list_widget.addItem(waypoint)

            old_x, old_y, old_z = x, y, z
            time.sleep(0.05)

    def start_walker_thread(self) -> None:
        thread = Thread(target=self.follow_waypoints)
        thread.daemon = True
        if self.start_cave_bot_checkbox.checkState() == 2:
            thread.start()

    def follow_waypoints(self):
        current_wpt = 0
        timer = 0
        while self.start_cave_bot_checkbox.checkState():
            try:
                self.waypoint_list_widget.setCurrentRow(current_wpt)
                wpt_data = self.waypoint_list_widget.item(current_wpt).data(Qt.UserRole)
                if not wpt_data:
                    print(f"Waypoint {current_wpt} is invalid.")
                    break

                x, y, z = read_my_wpt()
                if x is None or y is None or z is None:
                    time.sleep(1)
                    continue

                map_x, map_y, map_z = wpt_data['X'], wpt_data['Y'], wpt_data['Z']
                wpt_action = wpt_data['Action']
                wpt_direction = wpt_data['Direction']

                if x == map_x and y == map_y and z == map_z and wpt_action == 0:
                    current_wpt = (current_wpt + 1) % self.waypoint_list_widget.count()
                    timer = 0
                    time.sleep(0.1)
                    continue

                if not walker_Lock.locked():
                    if wpt_action == 0:
                        walk(wpt_direction, x, y, z, map_x, map_y, map_z)
                        timer += 0.01
                        time.sleep(0.01)

                    elif wpt_action == 1:
                        time.sleep(0.5)
                        timer += 0.5
                        right_click(coordinates_x[10], coordinates_y[10])
                        time.sleep(0.1)

                    elif wpt_action == 2:
                        time.sleep(0.5)
                        timer += 0.5
                        right_click(coordinates_x[9], coordinates_y[9])
                        time.sleep(0.1)

                    elif wpt_action == 3:
                        time.sleep(0.5)
                        timer += 0.5
                        right_click(coordinates_x[0], coordinates_y[0])
                        current_wpt += 1

                if timer > 5:
                    current_wpt = (current_wpt + 1) % self.waypoint_list_widget.count()
                    time.sleep(0.1)

            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

