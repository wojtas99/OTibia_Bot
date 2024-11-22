import random

import Addresses
from Addresses import icon_image, lock, coordinates_x, coordinates_y
import base64
from PyQt5.QtCore import Qt
import json
import time
from threading import Thread
from PyQt5.QtWidgets import (
    QWidget, QListWidget, QLineEdit, QTextEdit, QCheckBox, QComboBox, QVBoxLayout,
    QHBoxLayout, QGroupBox, QPushButton, QListWidgetItem, QLabel, QGridLayout
)
from PyQt5.QtGui import QIcon, QPixmap

from Functions import read_my_wpt
from MemoryFunctions import read_memory_address
from KeyboardFunctions import walk
from MouseFunctions import left_click
from MouseFunctions import right_click
import os


class WalkerTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Walker")
        self.setFixedSize(350, 350)

        # Widgets
        self.waypoint_list_widget = QListWidget(self)
        self.waypoint_profile_list_widget = QListWidget(self)
        self.waypoint_profile_line_edit = QLineEdit(self)
        self.action_waypoint_text_edit = QTextEdit(self)
        self.record_cave_bot_checkbox = QCheckBox("Auto Recording", self)
        self.start_cave_bot_checkbox = QCheckBox("Start Walker", self)
        self.waypoint_option_combobox = QComboBox(self)

        # Layouts
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize UI components
        self.save_load_waypoints()
        self.waypoint_list()
        self.add_waypoints()
        self.start_walker()

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
        for file in os.listdir("Waypoints"):
            self.waypoint_profile_list_widget.addItem(f"{file.split('.')[0]}")

        # Layouts
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        # Add Widgets
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.waypoint_profile_line_edit)
        layout2.addWidget(save_waypoint_profile_button)
        layout2.addWidget(load_waypoint_profile_button)

        # Add Layouts
        groupbox_layout.addWidget(self.waypoint_profile_list_widget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def waypoint_list(self) -> None:
        groupbox = QGroupBox("Waypoints")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        delete_waypoint_button = QPushButton("Del", self)
        delete_waypoint_button.clicked.connect(self.delete_waypoint)

        clear_waypoint_list_button = QPushButton("Clear", self)
        clear_waypoint_list_button.clicked.connect(self.clear_waypoint_list)

        # Layouts
        layout1 = QHBoxLayout()
        layout1.addWidget(delete_waypoint_button)
        layout1.addWidget(clear_waypoint_list_button)

        # Add Layouts
        groupbox_layout.addWidget(self.waypoint_list_widget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 0, 0, 1, 1)

    def add_waypoints(self) -> None:
        groupbox = QGroupBox("Add Waypoints")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Combo Box options
        directions = [
            "Center", "North", "South", "East", "West",
            "North-East", "North-West", "South-East", "South-West"
        ]
        self.waypoint_option_combobox.addItems(directions)

        # Buttons
        stand_waypoint_button = QPushButton("Stand", self)
        rope_waypoint_button = QPushButton("Rope", self)
        shovel_waypoint_button = QPushButton("Shovel", self)
        ladder_waypoint_button = QPushButton("Ladder", self)
        action_waypoint_button = QPushButton("Action", self)
        label_waypoint_button = QPushButton("Label", self)

        # Button Functions
        stand_waypoint_button.clicked.connect(lambda: self.add_waypoint(0))
        rope_waypoint_button.clicked.connect(lambda: self.add_waypoint(1))
        shovel_waypoint_button.clicked.connect(lambda: self.add_waypoint(2))
        ladder_waypoint_button.clicked.connect(lambda: self.add_waypoint(3))
        action_waypoint_button.clicked.connect(lambda: self.add_waypoint(4))
        label_waypoint_button.clicked.connect(lambda: self.add_waypoint(5))

        # Line Edit
        self.action_waypoint_text_edit.setFixedHeight(50)

        # Layouts
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        # Add Widgets
        layout1.addWidget(self.waypoint_option_combobox)
        layout2.addWidget(stand_waypoint_button)
        layout2.addWidget(action_waypoint_button)
        layout2.addWidget(label_waypoint_button)
        layout3.addWidget(rope_waypoint_button)
        layout3.addWidget(shovel_waypoint_button)
        layout3.addWidget(ladder_waypoint_button)
        layout4.addWidget(self.action_waypoint_text_edit)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1, 2, 1)

    def start_walker(self) -> None:
        groupbox = QGroupBox("Start")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Check Boxes
        self.start_cave_bot_checkbox.stateChanged.connect(self.start_walker_thread)
        self.record_cave_bot_checkbox.stateChanged.connect(self.start_record_thread)

        # Layouts
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        # Add Widgets
        layout1.addWidget(self.start_cave_bot_checkbox)
        layout2.addWidget(self.record_cave_bot_checkbox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 1)

    def save_waypoint_profile(self) -> None:
        waypoint_profile_name = self.waypoint_profile_line_edit.text()

        if waypoint_profile_name:
            waypoint_list = [
                {"name": self.waypoint_list_widget.item(i).text(),
                 "data": self.waypoint_list_widget.item(i).data(Qt.UserRole)}
                for i in range(self.waypoint_list_widget.count())
            ]

            # Save the waypoints to a JSON file
            with open(f"Waypoints/{waypoint_profile_name}.json", "w") as f:
                json.dump(waypoint_list, f, indent=4)

            self.waypoint_profile_list_widget.addItem(waypoint_profile_name)
            self.waypoint_profile_line_edit.clear()

    def load_waypoint_profile(self) -> None:
        waypoint_profile_name = self.waypoint_profile_list_widget.currentItem().text()
        if waypoint_profile_name:
            with open(f"Waypoints/{waypoint_profile_name}.json", "r") as f:
                waypoint_list = json.load(f)
                self.waypoint_list_widget.clear()
                for entry in waypoint_list:
                    waypoint = QListWidgetItem(entry["name"])
                    waypoint.setData(Qt.UserRole, entry["data"])
                    self.waypoint_list_widget.addItem(waypoint)

    # Add Waypoints
    def add_waypoint(self, index):
        x, y, z = read_my_wpt()

        waypoint_data = {
            "X": x,
            "Y": y,
            "Z": z,
            "Action": index
        }

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
            action_text = self.action_waypoint_text_edit.toPlainText()
            if action_text:
                waypoint_data["Direction"] = action_text
                waypoint = QListWidgetItem(f'Action: {x} {y} {z}')
                self.action_waypoint_text_edit.clear()

        elif index == 5:  # Label
            label_name = self.action_waypoint_text_edit.toPlainText()
            if label_name:
                waypoint_data["Direction"] = label_name
                waypoint = QListWidgetItem(f'{label_name}: {x} {y} {z}')
                self.action_waypoint_text_edit.clear()

        waypoint.setData(Qt.UserRole, waypoint_data)
        self.waypoint_list_widget.addItem(waypoint)

    def delete_waypoint(self) -> None:
        self.waypoint_list_widget.takeItem(self.waypoint_list_widget.currentRow())

    def clear_waypoint_list(self) -> None:
        self.waypoint_list_widget.clear()

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

        old_x = x
        old_y = y
        old_z = z

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

            old_x = x
            old_y = y
            old_z = z

    def start_walker_thread(self) -> None:
        thread = Thread(target=self.follow_waypoints)
        thread.daemon = True
        if self.start_cave_bot_checkbox.checkState() == 2:
            thread.start()

    def follow_waypoints(self) -> None:
        current_wpt = self.waypoint_list_widget.currentRow()
        if current_wpt == -1:
            current_wpt = 0
        timer = 0
        while self.start_cave_bot_checkbox.checkState():
            self.waypoint_list_widget.setCurrentRow(current_wpt)
            wpt_data = self.waypoint_list_widget.item(current_wpt).data(Qt.UserRole)
            wpt_action = wpt_data['Action']
            wpt_direction = wpt_data['Direction']
            map_x = wpt_data['X']
            map_y = wpt_data['Y']
            map_z = wpt_data['Z']
            x, y, z = read_my_wpt()
            if x == map_x and y == map_y and z == map_z and wpt_action == 0:
                timer = 0
                current_wpt += 1
                if current_wpt == self.waypoint_list_widget.count():
                    current_wpt = 0
                time.sleep(0.1)
                continue
            if not lock.locked():
                timer += 0.1
                if wpt_action == 0:
                    walk(wpt_direction, x, y, z, map_x, map_y, map_z)
                    time.sleep(0.01)
                elif wpt_action == 3:
                    time.sleep(0.5)
                    right_click(coordinates_x[0], coordinates_y[0])  # Click On Ladder
                    current_wpt += 1
            if timer > 5:  # Search for the nearest waypoint
                for index in range(self.waypoint_list_widget.count()):
                    self.waypoint_list_widget.setCurrentRow(index)
                    wpt_data = self.waypoint_list_widget.item(index).data(Qt.UserRole)
                    map_x = wpt_data['X']
                    map_y = wpt_data['Y']
                    map_z = wpt_data['Z']
                    time.sleep(0.05)
                    if z == map_z and abs(map_x - x) < 4 and abs(map_y - y) < 4:
                        current_wpt = index
                        left_click(coordinates_x[0] + (map_x - x) * 75, coordinates_y[0] + (map_y - y) * 75)
                        time.sleep(2)
                    x, y, z = read_my_wpt()
                    if x == map_x and y == map_y and z == map_z:
                        break
