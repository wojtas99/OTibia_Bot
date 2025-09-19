import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QListWidget, QLineEdit, QTextEdit, QCheckBox, QComboBox, QVBoxLayout,
    QHBoxLayout, QGroupBox, QPushButton, QListWidgetItem, QLabel, QGridLayout
)
from PyQt5.QtGui import QIcon

from Functions.GeneralFunctions import delete_item, manage_profile
from Functions.MemoryFunctions import *
from Walker.WalkerThread import WalkerThread, RecordThread


class WalkerTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.record_thread = None
        self.walker_thread = None

        # Other Variables
        self.labels_dictionary = {}

        # Load Icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        # Set Title and Size
        self.setWindowTitle("Walker")
        self.setFixedSize(350, 400)  # Increased size to fit the status label

        # --- Status label at the bottom (behaves like a "status bar")
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Widgets
        self.waypointList_listWidget = QListWidget(self)
        self.profile_listWidget = QListWidget(self)
        self.profile_lineEdit = QLineEdit(self)
        self.record_checkBox = QCheckBox("Auto Recording", self)
        self.start_checkBox = QCheckBox("Start Walker", self)
        self.option_comboBox = QComboBox(self)
        directions = [
            "Center", "North", "South", "East", "West",
            "North-East", "North-West", "South-East", "South-West", "Lure"
        ]
        self.option_comboBox.addItems(directions)

        # Main Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize UI
        self.profileList()
        self.waypointList()
        self.start_walker()

        # Finally add the status label (we'll place it at the bottom row)
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

    def profileList(self) -> None:
        groupbox = QGroupBox("Save && Load")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_profile)

        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_profile)

        for file in os.listdir("Save/Waypoints"):
            if file.endswith(".json"):
                self.profile_listWidget.addItem(file.split(".")[0])

        # Layouts
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.profile_lineEdit)
        layout2.addWidget(save_button)
        layout2.addWidget(load_button)

        groupbox_layout.addWidget(self.profile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def waypointList(self) -> None:
        groupbox = QGroupBox("Waypoints")
        groupbox_layout = QHBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        stand_waypoint_button = QPushButton("Stand", self)
        rope_waypoint_button = QPushButton("Rope", self)
        shovel_waypoint_button = QPushButton("Shovel", self)
        ladder_waypoint_button = QPushButton("Ladder", self)
        clearWaypointList_button = QPushButton("Clear List", self)

        # Connect to add_waypoint with different indexes
        clearWaypointList_button.clicked.connect(self.clear_waypointList)
        stand_waypoint_button.clicked.connect(lambda: self.add_waypoint(0))
        rope_waypoint_button.clicked.connect(lambda: self.add_waypoint(1))
        shovel_waypoint_button.clicked.connect(lambda: self.add_waypoint(2))
        ladder_waypoint_button.clicked.connect(lambda: self.add_waypoint(3))

        # Double-click to delete
        self.waypointList_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.waypointList_listWidget, item)
        )

        # Layouts
        groupbox2_layout = QVBoxLayout(self)
        layout1 = QVBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        layout1.addWidget(self.waypointList_listWidget)
        layout1.addWidget(clearWaypointList_button)

        layout2.addWidget(self.option_comboBox)

        layout3.addWidget(stand_waypoint_button)

        layout4.addWidget(rope_waypoint_button)
        layout4.addWidget(shovel_waypoint_button)
        layout4.addWidget(ladder_waypoint_button)

        groupbox2_layout.addLayout(layout2)
        groupbox2_layout.addLayout(layout3)
        groupbox2_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(groupbox2_layout)
        self.layout.addWidget(groupbox, 0, 0, 1, 2)

    def start_walker(self) -> None:
        groupbox = QGroupBox("Start")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        self.start_checkBox.stateChanged.connect(self.start_walker_thread)
        self.record_checkBox.stateChanged.connect(self.start_record_thread)

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout1.addWidget(self.start_checkBox)
        layout2.addWidget(self.record_checkBox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 1)

    def save_profile(self) -> None:
        profile_name = self.profile_lineEdit.text().strip()
        if not profile_name:
            return
        waypoint_list = [
            self.waypointList_listWidget.item(i).data(Qt.UserRole)
            for i in range(self.waypointList_listWidget.count())
        ]
        data_to_save = {
            "waypoints": waypoint_list,
        }
        if manage_profile("save", "Save/Waypoints", profile_name, data_to_save):
            existing_names = [
                self.profile_listWidget.item(i).text()
                for i in range(self.profile_listWidget.count())
            ]
            if profile_name not in existing_names:
                self.profile_listWidget.addItem(profile_name)
            self.profile_listWidget.clear()
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.status_label.setText(f"Profile '{profile_name}' has been saved!")

    def load_profile(self) -> None:
        profile_name = self.profile_listWidget.currentItem()
        if not profile_name:
            self.profile_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list.")
            return
        else:
            self.profile_listWidget.setStyleSheet("")
        profile_name = profile_name.text()
        filename = f"Save/Waypoints/{profile_name}.json"
        with open(filename, "r") as f:
            loaded_data = json.load(f)

        self.waypointList_listWidget.clear()
        for walk_data in loaded_data.get("waypoints", []):
            index = int(walk_data['Action'])
            walk_name = "Something"
            if index == 0:  # Stand
                walk_name = f"Stand: {walk_data['X']} {walk_data['Y']} {walk_data['Z']}"
            elif index == 1:  # Rope
                walk_name = f"Rope: {walk_data['X']} {walk_data['Y']} {walk_data['Z']}"
            elif index == 2:  # Shovel
                walk_name = f"Shovel: {walk_data['X']} {walk_data['Y']} {walk_data['Z']}"
            elif index == 3:  # Ladder
                walk_name = f"Ladder: {walk_data['X']} {walk_data['Y']} {walk_data['Z']}"
            walk_item = QListWidgetItem(walk_name)
            walk_item.setData(Qt.UserRole, walk_data)
            self.waypointList_listWidget.addItem(walk_item)

        self.profile_lineEdit.clear()
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' loaded successfully!")

    def add_waypoint(self, index):
        x, y, z = read_my_wpt()

        waypoint_data = {
            "X": x,
            "Y": y,
            "Z": z,
            "Action": index
        }

        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        if index == 0:  # Stand
            waypoint_data["Direction"] = self.option_comboBox.currentIndex()
            waypoint = QListWidgetItem(f'Stand: {x} {y} {z} {self.option_comboBox.currentText()}')

        elif index == 1:  # Rope
            waypoint_data["Direction"] = self.option_comboBox.currentIndex()
            waypoint = QListWidgetItem(f'Rope: {x} {y} {z}')

        elif index == 2:  # Shovel
            waypoint_data["Direction"] = self.option_comboBox.currentIndex()
            waypoint = QListWidgetItem(f'Shovel: {x} {y} {z}')

        elif index == 3:  # Ladder
            waypoint_data["Direction"] = self.option_comboBox.currentIndex()
            waypoint = QListWidgetItem(f'Ladder: {x} {y} {z}')

        waypoint.setData(Qt.UserRole, waypoint_data)
        self.waypointList_listWidget.addItem(waypoint)
        if self.waypointList_listWidget.currentRow() == -1:
            self.waypointList_listWidget.setCurrentRow(0)
        else:
            self.waypointList_listWidget.setCurrentRow(self.waypointList_listWidget.currentRow() + 1)
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Waypoint added successfully!")

    def clear_waypointList(self) -> None:
        self.waypointList_listWidget.clear()
        self.status_label.setText("")  # Clear status if you want

    def start_record_thread(self, state):
        if state == Qt.Checked:
            self.record_thread = RecordThread(self.option_comboBox)
            self.record_thread.wpt_update.connect(self.update_waypointList)
            self.record_thread.start()
        else:
            if self.record_thread:
                self.record_thread.stop()
                self.record_thread = None

    def start_walker_thread(self, state):
        if state == Qt.Checked:
            if not self.walker_thread:
                waypoints = [
                    self.waypointList_listWidget.item(i).data(Qt.UserRole)
                    for i in range(self.waypointList_listWidget.count())
                ]
                self.walker_thread = WalkerThread(waypoints)
                self.walker_thread.index_update.connect(self.update_waypointList)
                self.walker_thread.start()
        else:
            if self.walker_thread:
                self.walker_thread.stop()
                self.walker_thread = None

    def update_waypointList(self, option, waypoint):
        if option == 0:
            self.waypointList_listWidget.setCurrentRow(int(waypoint))
        elif option == 1:
            self.waypointList_listWidget.addItem(waypoint)
