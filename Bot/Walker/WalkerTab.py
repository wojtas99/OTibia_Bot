import base64
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QListWidget, QLineEdit, QTextEdit, QCheckBox, QComboBox, QVBoxLayout,
    QHBoxLayout, QGroupBox, QPushButton, QListWidgetItem, QLabel, QGridLayout
)
from PyQt5.QtGui import QIcon, QPixmap

from Addresses import icon_image
from Functions.GeneralFunctions import delete_item, manage_profile
from Functions.MemoryFunctions import *
from Walker.WalkerThread import WalkerThread, RecordThread


class WalkerTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.record_thread = None
        self.walker_thread = None
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
        for file in os.listdir("Save/Waypoints"):
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
            "North-East", "North-West", "South-East", "South-West", "Lure"
        ]
        self.waypoint_option_combobox.addItems(directions)

        stand_waypoint_button = QPushButton("Stand", self)
        stand_waypoint_button.setFixedWidth(40)
        rope_waypoint_button = QPushButton("Rope", self)
        rope_waypoint_button.setFixedWidth(40)
        shovel_waypoint_button = QPushButton("Shovel", self)
        shovel_waypoint_button.setFixedWidth(40)
        ladder_waypoint_button = QPushButton("Ladder", self)
        ladder_waypoint_button.setFixedWidth(40)
        action_waypoint_button = QPushButton("Action", self)
        action_waypoint_button.setFixedWidth(40)
        label_waypoint_button = QPushButton("Label", self)
        label_waypoint_button.setFixedWidth(40)

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
        Zapis profilu waypointów przy użyciu funkcji manage_profile.
        """
        # Czyszczenie poprzednich komunikatów/obwiedzin
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.waypoint_profile_line_edit.setStyleSheet("")

        profile_name = self.waypoint_profile_line_edit.text().strip()
        if not profile_name:
            self.waypoint_profile_line_edit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Podaj nazwę profilu przed zapisaniem.")
            return

        # Przygotowanie danych do zapisu: lista waypointów, gdzie każdy wpis to słownik z nazwą i danymi
        waypoint_list = []
        for i in range(self.waypoint_list_widget.count()):
            item = self.waypoint_list_widget.item(i)
            waypoint_list.append({
                "name": item.text(),
                "data": item.data(Qt.UserRole)
            })

        if manage_profile("save", "Save/Waypoints", profile_name, waypoint_list):
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.status_label.setText("Profil zapisany pomyślnie!")
            self.waypoint_profile_line_edit.clear()

            # Dodaj profil do listy, jeśli jeszcze nie istnieje
            existing_names = [
                self.waypoint_profile_list_widget.item(i).text()
                for i in range(self.waypoint_profile_list_widget.count())
            ]
            if profile_name not in existing_names:
                self.waypoint_profile_list_widget.addItem(profile_name)
        else:
            self.status_label.setText("Błąd przy zapisie profilu.")
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
        filename = f"Save/Waypoints/{waypoint_profile_name}.json"
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

    def start_record_thread(self, state):
        if state == Qt.Checked:
            self.record_thread = RecordThread(self.waypoint_option_combobox)
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
                    self.waypoint_list_widget.item(i).data(Qt.UserRole)
                    for i in range(self.waypoint_list_widget.count())
                ]
                self.walker_thread = WalkerThread(waypoints)
                self.walker_thread.index_update.connect(self.update_waypointList)
                self.walker_thread.start()
        else:
            if self.walker_thread:
                self.walker_thread.stop()
                self.walker_thread = None

    def update_waypointList(self, option, waypoint):
        """
        Update the current waypoint in the UI.
        """
        if option == 0:
            self.waypoint_list_widget.setCurrentRow(int(waypoint))
        elif option == 1:
            self.waypoint_list_widget.addItem(waypoint)
