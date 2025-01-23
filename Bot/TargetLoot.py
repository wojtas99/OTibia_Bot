
from Addresses import icon_image
import base64
import os
import json
from Functions import delete_item
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout,
    QGroupBox, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from TargetLootThread import TargetThread, LootThread


class TargetLootTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.loot_thread = None
        self.target_thread = None

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon()
        )

        # Set Title and Size
        self.setWindowTitle("Targeting")
        self.setFixedSize(350, 450)  # Increased to fit the status label

        # --- Status "bar" label at the bottom
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # Check Boxes
        self.startLoot_checkBox = QCheckBox("Start Looting", self)
        self.startTarget_checkBox = QCheckBox("Start Targeting", self)
        self.chase_checkBox = QCheckBox("Chase", self)
        self.startSkin_checkBox = QCheckBox("Skin", self)

        # Combo Boxes
        self.attackDist_comboBox = QComboBox(self)

        # Line Edits
        self.targetLootProfile_lineEdit = QLineEdit(self)
        self.targetName_lineEdit = QLineEdit(self)
        self.itemName_lineEdit = QLineEdit(self)
        self.lootOption_lineEdit = QLineEdit(self)
        self.lootOption_lineEdit.setFixedWidth(20)
        self.lootOption_lineEdit.setMaxLength(2)

        # List Widgets
        self.targetLootProfile_listWidget = QListWidget(self)
        self.targetList_listWidget = QListWidget(self)
        self.targetList_listWidget.setFixedHeight(150)
        self.lootList_listWidget = QListWidget(self)

        # Main Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize UI components
        self.target_list()
        self.save_load_target_loot()
        self.set_target()
        self.loot_list()
        self.target_loot()

        # Finally, add the status label at the bottom
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

    def target_list(self) -> None:
        groupbox = QGroupBox("Target List", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        clear_targets_button = QPushButton("Clear List", self)
        clear_targets_button.clicked.connect(self.clear_targets_list)

        # Double-click to delete
        self.targetList_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.targetList_listWidget, item)
        )

        layout1 = QHBoxLayout()
        layout1.addWidget(clear_targets_button)

        groupbox_layout.addWidget(self.targetList_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 0, 0, 2, 1)

    def save_load_target_loot(self) -> None:
        groupbox = QGroupBox("Save && Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        save_target_loot_button = QPushButton("Save", self)
        load_target_loot_button = QPushButton("Load", self)

        # Button functions
        save_target_loot_button.clicked.connect(self.save_target_loot)
        load_target_loot_button.clicked.connect(self.load_target_loot)

        # Populate the profile list with existing files
        if not os.path.exists("Targeting"):
            os.makedirs("Targeting")
        if not os.path.exists("Looting"):
            os.makedirs("Looting")

        for file in os.listdir("Targeting"):
            if file.endswith(".json"):
                self.targetLootProfile_listWidget.addItem(file.split('.')[0])

        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.targetLootProfile_lineEdit)
        layout2.addWidget(save_target_loot_button)
        layout2.addWidget(load_target_loot_button)

        groupbox_layout.addWidget(self.targetLootProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def set_target(self) -> None:
        groupbox = QGroupBox("Define Target", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button
        add_target_button = QPushButton("Add", self)
        add_target_button.setFixedWidth(50)
        add_target_button.clicked.connect(self.add_target)

        # ComboBox
        self.attackDist_comboBox.addItems(["All", "1", "2", "3", "4", "5"])

        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(self.targetName_lineEdit)
        layout1.addWidget(add_target_button)
        layout2.addWidget(QLabel("Attack Distance:", self))
        layout2.addWidget(self.attackDist_comboBox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 1, 1, 1)

    def target_loot(self) -> None:
        groupbox = QGroupBox("Start", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        self.startTarget_checkBox.stateChanged.connect(self.start_target_thread)
        self.startLoot_checkBox.stateChanged.connect(self.start_loot_thread)

        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(self.startLoot_checkBox)
        layout1.addWidget(self.chase_checkBox)
        layout2.addWidget(self.startTarget_checkBox)
        layout2.addWidget(self.startSkin_checkBox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 1, 1, 1)

    def loot_list(self) -> None:
        groupbox = QGroupBox("Loot List", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button
        add_item_button = QPushButton("Add", self)
        add_item_button.setFixedWidth(40)
        add_item_button.clicked.connect(self.add_item)

        # Double-click to delete
        self.lootList_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.lootList_listWidget, item)
        )

        layout1 = QHBoxLayout(self)
        layout1.addWidget(self.itemName_lineEdit)
        layout1.addWidget(self.lootOption_lineEdit)
        layout1.addWidget(add_item_button)

        groupbox_layout.addWidget(self.lootList_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 2, 1)

    def add_item(self) -> None:
        """
        Adds an item to the lootList_listWidget, but checks if the fields
        (item name, loot container) are not empty.
        """
        # Reset styles and clear the status label
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.itemName_lineEdit.setStyleSheet("")
        self.lootOption_lineEdit.setStyleSheet("")

        item_name = self.itemName_lineEdit.text().strip()
        loot_container = self.lootOption_lineEdit.text().strip()

        if not item_name:
            self.itemName_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter an item name.")
            return

        if not loot_container:
            self.lootOption_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a loot container number.")
            return

        # If item already exists in the list, do nothing
        for index in range(self.lootList_listWidget.count()):
            if item_name.upper() == self.lootList_listWidget.item(index).text().upper():
                return

        # Valid. Add to the list
        try:
            item_data = {"Loot": int(loot_container)}
        except ValueError:
            # If the loot_container is not a valid integer
            self.lootOption_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Loot container must be a number.")
            return

        item = QListWidgetItem(item_name)
        item.setData(Qt.UserRole, item_data)
        self.lootList_listWidget.addItem(item)

        # Clear fields
        self.itemName_lineEdit.clear()
        self.lootOption_lineEdit.clear()

        # Show success
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Item added successfully!")

    def add_target(self) -> None:
        """
        Adds a monster to the targetList_listWidget, but checks if the
        monster name is not empty.
        """
        # Reset styles and clear status
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.targetName_lineEdit.setStyleSheet("")

        monster_name = self.targetName_lineEdit.text().strip()
        if not monster_name:
            self.targetName_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a monster name.")
            return

        # Check if monster already exists in the list
        for index in range(self.targetList_listWidget.count()):
            existing_name = self.targetList_listWidget.item(index).text().split(' | ')[0].upper()
            if monster_name.upper() == existing_name:
                return

        # Distance data
        monster_data = {"Distance": self.attackDist_comboBox.currentText()}
        if monster_data['Distance'] == 'All':
            monster_data['Distance'] = 0

        monster = QListWidgetItem(monster_name)
        monster.setData(Qt.UserRole, monster_data)
        self.targetList_listWidget.addItem(monster)

        # Clear field
        self.targetName_lineEdit.clear()
        self.attackDist_comboBox.setCurrentIndex(0)

        # Success message
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Target added successfully!")

    def delete_target(self) -> None:
        selected_monster = self.targetList_listWidget.currentItem()
        if selected_monster:
            self.targetList_listWidget.takeItem(self.targetList_listWidget.row(selected_monster))

    def clear_targets_list(self) -> None:
        self.targetList_listWidget.clear()
        self.status_label.setText("")  # optional

    def save_target_loot(self) -> None:
        """
        Saves the current targets and loot items to JSON,
        but checks if profile name is not empty and there's at least 1 target in the list.
        """
        # Reset status/styles
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.targetLootProfile_lineEdit.setStyleSheet("")

        target_loot_name = self.targetLootProfile_lineEdit.text().strip()
        if not target_loot_name:
            self.targetLootProfile_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a profile name before saving.")
            return

        if self.targetList_listWidget.count() == 0:
            self.status_label.setText("Cannot save: no targets added.")
            return

        # If valid, save
        target_list = [
            {
                "name": self.targetList_listWidget.item(i).text(),
                "data": self.targetList_listWidget.item(i).data(Qt.UserRole)
            }
            for i in range(self.targetList_listWidget.count())
        ]
        looting_list = [
            {
                "name": self.lootList_listWidget.item(i).text(),
                "data": self.lootList_listWidget.item(i).data(Qt.UserRole)
            }
            for i in range(self.lootList_listWidget.count())
        ]

        # Ensure directories exist
        os.makedirs("Targeting", exist_ok=True)
        os.makedirs("Looting", exist_ok=True)

        with open(f"Targeting/{target_loot_name}.json", "w") as f:
            json.dump(target_list, f, indent=4)
        with open(f"Looting/{target_loot_name}.json", "w") as f:
            json.dump(looting_list, f, indent=4)

        # Add to the list widget if not already there
        existing_names = [
            self.targetLootProfile_listWidget.item(i).text().upper()
            for i in range(self.targetLootProfile_listWidget.count())
        ]
        if target_loot_name.upper() not in existing_names:
            self.targetLootProfile_listWidget.addItem(target_loot_name)

        self.targetLootProfile_lineEdit.clear()

        # Success
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Profile saved successfully!")

    def load_target_loot(self) -> None:
        """
        Loads a selected target/loot profile, or highlights if none is selected.
        """
        # Reset status/styles
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.targetLootProfile_listWidget.setStyleSheet("")

        current_item = self.targetLootProfile_listWidget.currentItem()
        if not current_item:
            # Highlight list if nothing selected
            self.targetLootProfile_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list.")
            return

        profile_name = current_item.text()
        target_filename = f"Targeting/{profile_name}.json"
        loot_filename = f"Looting/{profile_name}.json"

        if not os.path.exists(target_filename) or not os.path.exists(loot_filename):
            self.targetLootProfile_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText(f"No files found for profile '{profile_name}'.")
            return

        # Load target data
        with open(target_filename, "r") as f:
            target_list = json.load(f)
            self.targetList_listWidget.clear()
            for entry in target_list:
                target = QListWidgetItem(entry["name"])
                target.setData(Qt.UserRole, entry["data"])
                self.targetList_listWidget.addItem(target)

        # Load loot data
        with open(loot_filename, "r") as f:
            loot_list = json.load(f)
            self.lootList_listWidget.clear()
            for entry in loot_list:
                item = QListWidgetItem(entry["name"])
                item.setData(Qt.UserRole, entry["data"])
                self.lootList_listWidget.addItem(item)

        # Success
        self.targetLootProfile_lineEdit.setStyleSheet("")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' loaded successfully.")

    def start_target_thread(self, state) -> None:
        if self.loot_thread:
            self.loot_thread.update_states(self.startTarget_checkBox)
        if state == Qt.Checked:
            self.target_thread = TargetThread(self.targetList_listWidget, self.startLoot_checkBox.checkState(), self.startSkin_checkBox.checkState())
            self.target_thread.start()
        else:
            if self.target_thread:
                self.target_thread.stop()
                self.target_thread = None

    def start_loot_thread(self, state) -> None:
        if self.target_thread:
            self.target_thread.update_states(0, state)
        if state == Qt.Checked:
            self.loot_thread = LootThread(self.lootList_listWidget, self.startTarget_checkBox.checkState())
            self.loot_thread.start()
        else:
            if self.loot_thread:
                self.loot_thread.stop()
                self.loot_thread = None

