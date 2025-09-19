import os
import json
from Functions.GeneralFunctions import delete_item, manage_profile
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout,
    QGroupBox, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QListWidgetItem
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from Target.TargetLootThread import TargetThread, LootThread


class TargetLootTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.loot_thread = None
        self.target_thread = None

        # Load Icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Targeting")
        self.setFixedSize(350, 450)

        # --- Status "bar" label at the bottom
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # Check Boxes
        self.startLoot_checkBox = QCheckBox("Looting", self)
        self.startLoot_checkBox.stateChanged.connect(self.start_loot_thread)
        self.startTarget_checkBox = QCheckBox("Targeting", self)
        self.startTarget_checkBox.stateChanged.connect(self.start_target_thread)

        # Combo Boxes
        self.attackDist_comboBox = QComboBox(self)
        self.attackDist_comboBox.addItems(["All", "1", "2", "3", "4", "5", "6", "7"])
        self.stance_comboBox = QComboBox(self)
        self.stance_comboBox.addItems(["Do Nothing", "Chase", "Diagonal", "Chase-Diagonal"])
        self.attackKey_comboBox = QComboBox(self)
        self.attackKey_comboBox.addItems(f'F{i}' for i in range(1, 10))

        # Line Edits
        self.profile_lineEdit = QLineEdit(self)
        self.targetName_lineEdit = QLineEdit(self)
        self.itemName_lineEdit = QLineEdit(self)
        self.lootOption_lineEdit = QLineEdit(self)
        self.lootOption_lineEdit.setFixedWidth(20)
        self.lootOption_lineEdit.setMaxLength(2)

        # List Widgets
        self.profile_listWidget = QListWidget(self)
        self.targetList_listWidget = QListWidget(self)
        self.targetList_listWidget.setFixedSize(150, 150)
        self.lootList_listWidget = QListWidget(self)

        # Main Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize UI components
        self.targetList()
        self.profileList()
        self.lootList()

        # Finally, add the status label at the bottom
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

    def targetList(self) -> None:
        groupbox = QGroupBox("Targeting", self)
        groupbox_layout = QHBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        clearTargetList_button = QPushButton("Clear List", self)
        addTarget_button = QPushButton("Add", self)

        # Button Functions
        clearTargetList_button.clicked.connect(self.clearTarget_list)
        addTarget_button.clicked.connect(self.add_target)

        # Double-click to delete
        self.targetList_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.targetList_listWidget, item)
        )

        # Layouts
        groupbox2_layout = QVBoxLayout(self)
        layout1 = QVBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)
        layout6 = QHBoxLayout(self)

        layout1.addWidget(self.targetList_listWidget)
        layout1.addWidget(clearTargetList_button)

        layout2.addWidget(self.targetName_lineEdit)
        layout2.addWidget(addTarget_button)

        layout3.addWidget(QLabel("Stance:", self))
        layout3.addWidget(self.stance_comboBox)

        layout4.addWidget(self.startTarget_checkBox)
        layout4.addWidget(self.startLoot_checkBox)

        layout5.addWidget(QLabel("Dist:", self))
        layout5.addWidget(self.attackDist_comboBox)

        layout6.addWidget(QLabel("Attack Key:", self))
        layout6.addWidget(self.attackKey_comboBox)

        self.targetName_lineEdit.setPlaceholderText("Orc, * - All Monsters")

        groupbox2_layout.addLayout(layout2)
        groupbox2_layout.addLayout(layout5)
        groupbox2_layout.addLayout(layout3)
        groupbox2_layout.addLayout(layout4)
        groupbox2_layout.addLayout(layout6)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(groupbox2_layout)
        self.layout.addWidget(groupbox, 0, 0, 1, 2)

    def profileList(self) -> None:
        groupbox = QGroupBox("Save && Load", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        save_target_loot_button = QPushButton("Save", self)
        load_target_loot_button = QPushButton("Load", self)

        # Button functions
        save_target_loot_button.clicked.connect(self.save_profile)
        load_target_loot_button.clicked.connect(self.load_profile)

        # Populate the profile list with existing files
        for file in os.listdir("Save/Targeting"):
            if file.endswith(".json"):
                self.profile_listWidget.addItem(file.split('.')[0])

        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.profile_lineEdit)
        layout2.addWidget(save_target_loot_button)
        layout2.addWidget(load_target_loot_button)

        groupbox_layout.addWidget(self.profile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def lootList(self) -> None:
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

        for index in range(self.lootList_listWidget.count()):
            if item_name.upper() == self.lootList_listWidget.item(index).text().upper():
                return

        item_data = {
            "Name": self.itemName_lineEdit.text(),
            "Loot": int(self.lootOption_lineEdit.text())
        }

        item = QListWidgetItem(item_name)
        item.setData(Qt.UserRole, item_data)
        self.lootList_listWidget.addItem(item)

        # Show success
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"'{self.itemName_lineEdit.text()}' has been added successfully!")

        # Clear fields
        self.lootOption_lineEdit.clear()
        self.itemName_lineEdit.clear()

    def add_target(self) -> None:
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.targetName_lineEdit.setStyleSheet("")

        monster_name = self.targetName_lineEdit.text().strip()
        if not monster_name:
            self.targetName_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a monster name.")
            return

        for index in range(self.targetList_listWidget.count()):
            existing_name = self.targetList_listWidget.item(index).text().split(' | ')[0].upper()
            if monster_name.upper() == existing_name:
                return

        target_data = {
            "Name": monster_name,
            "Dist": self.attackDist_comboBox.currentIndex(),
            "Stance": self.stance_comboBox.currentIndex(),
        }

        monster = QListWidgetItem(monster_name)
        monster.setData(Qt.UserRole, target_data)
        self.targetList_listWidget.addItem(monster)

        # Clear field
        self.targetName_lineEdit.clear()
        self.attackDist_comboBox.setCurrentIndex(0)
        self.stance_comboBox.setCurrentIndex(0)

        # Success message
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Target '{monster_name}' has been added!")

    def clearTarget_list(self) -> None:
        self.targetList_listWidget.clear()
        self.status_label.setText("")  # optional

    def save_profile(self) -> None:
        profile_name = self.profile_lineEdit.text().strip()
        if not profile_name:
            return
        target_list = [
            self.targetList_listWidget.item(i).data(Qt.UserRole)
            for i in range(self.targetList_listWidget.count())
        ]
        loot_list = [
            self.lootList_listWidget.item(i).data(Qt.UserRole)
            for i in range(self.lootList_listWidget.count())
        ]
        data_to_save = {
            "targets": target_list,
            "loot": loot_list
        }

        if manage_profile("save", "Save/Targeting", profile_name, data_to_save):
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.status_label.setText(f"Profile '{profile_name}' has been saved!")
            existing_names = [
                self.profile_listWidget.item(i).text()
                for i in range(self.profile_listWidget.count())
            ]
            if profile_name not in existing_names:
                self.profile_listWidget.addItem(profile_name)
            self.profile_lineEdit.clear()

    def load_profile(self) -> None:
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.profile_listWidget.setStyleSheet("")

        profile_name = self.profile_listWidget.currentItem()
        if not profile_name:
            self.profile_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list.")
            return
        else:
            self.profile_listWidget.setStyleSheet("")
        profile_name = profile_name.text()
        filename = f"Save/Targeting/{profile_name}.json"
        self.targetList_listWidget.clear()
        self.lootList_listWidget.clear()
        with open(filename, "r") as f:
            loaded_data = json.load(f)
        for target_data in loaded_data.get("targets", []):
            target_item = QListWidgetItem(target_data['Name'])
            target_item.setData(Qt.UserRole, target_data)
            self.targetList_listWidget.addItem(target_item)
        for loot_data in loaded_data.get("loot", []):
            loot_item = QListWidgetItem(loot_data['Name'])
            loot_item.setData(Qt.UserRole, loot_data)
            self.lootList_listWidget.addItem(loot_item)

    def start_target_thread(self, state) -> None:
        if self.loot_thread:
            self.loot_thread.update_states(state)
        if state == Qt.Checked:
            targets = [
                self.targetList_listWidget.item(i).data(Qt.UserRole)
                for i in range(self.targetList_listWidget.count())
            ]
            self.target_thread = TargetThread(targets, self.startLoot_checkBox.checkState(), self.attackKey_comboBox.currentIndex())
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

