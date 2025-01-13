import random
import base64
import time
import json
import os
from threading import Thread
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout,QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt5.QtCore import Qt
import Addresses
from Addresses import icon_image, coordinates_x, coordinates_y
from MemoryFunctions import read_memory_address
from MouseFunctions import use_on_me, right_click, left_click
from KeyboardFunctions import press_hotkey
from Functions import read_my_stats, read_my_wpt, read_target_info, delete_item


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)) else QIcon()
        )

        # Set Title and Size
        self.setWindowTitle("Spells & Healing")
        self.setFixedSize(450, 550)  # Slightly increased to fit new save/load UI

        # --- Status "bar" label at the bottom (acts like a status bar)
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: Red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Check Boxes
        self.start_heal_checkBox = QCheckBox("Start Heal", self)
        self.start_attack_checkBox = QCheckBox("Start Attack", self)

        # Combo Boxes
        self.hp_mana_comboBox = QComboBox(self)
        self.hotkey_rune_list_comboBox = QComboBox(self)
        self.actionList_comboBox = QComboBox(self)
        self.actionList_comboBox.setFixedWidth(50)

        # Line Edits
        self.hp_below_lineEdit = QLineEdit(self)
        self.hp_below_lineEdit.setFixedWidth(40)
        self.hp_above_lineEdit = QLineEdit(self)
        self.hp_above_lineEdit.setFixedWidth(40)
        self.min_mp_lineEdit = QLineEdit(self)
        self.min_mp_lineEdit.setFixedWidth(70)
        self.targetName_lineEdit = QLineEdit(self)
        self.hpFrom_lineEdit = QLineEdit(self)
        self.hpTo_lineEdit = QLineEdit(self)
        self.hpFrom_lineEdit.setFixedWidth(40)
        self.hpTo_lineEdit.setFixedWidth(40)
        self.hpFrom_lineEdit.setMaxLength(3)
        self.hpTo_lineEdit.setMaxLength(2)
        self.min_mp_spell_lineEdit = QLineEdit(self)
        self.min_mp_spell_lineEdit.setFixedWidth(70)
        self.spell_dist_lineEdit = QLineEdit(self)
        self.spell_dist_lineEdit.setMaxLength(1)
        self.spell_dist_lineEdit.setFixedWidth(40)
        self.profile_name_lineEdit = QLineEdit(self)

        # Validators to ensure numeric input
        int_validator_4 = QIntValidator(0, 9999, self)
        int_validator_3 = QIntValidator(1, 100, self)
        int_validator_2 = QIntValidator(0, 99, self)
        int_validator_1 = QIntValidator(1, 9, self)

        self.hp_below_lineEdit.setValidator(int_validator_3)
        self.hp_above_lineEdit.setValidator(int_validator_2)
        self.min_mp_lineEdit.setValidator(int_validator_4)
        self.hpFrom_lineEdit.setValidator(int_validator_3)
        self.hpTo_lineEdit.setValidator(int_validator_2)
        self.min_mp_spell_lineEdit.setValidator(int_validator_4)
        self.spell_dist_lineEdit.setValidator(int_validator_1)

        # List Widgets
        self.healList_listWidget = QListWidget(self)
        self.attackList_listWidget = QListWidget(self)
        self.savedAttackHealList_listWidget = QListWidget(self)

        # Double-click to delete item
        self.healList_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.healList_listWidget, item)
        )
        self.attackList_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.attackList_listWidget, item)
        )

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize sections
        self.heal_list()
        self.attack_hotkey_rune()
        self.add_heal_spell()
        self.add_attack_spell()
        self.save_load_list()
        self.save_load_profile()

        # Finally add the status label at the bottom row
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

    def heal_list(self) -> None:
        groupbox = QGroupBox("Heal Hotkeys && Runes")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        groupbox_layout.addWidget(self.healList_listWidget)
        self.layout.addWidget(groupbox, 0, 0)

    def attack_hotkey_rune(self) -> None:
        groupbox = QGroupBox("Attack Hotkeys && Runes")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        groupbox_layout.addWidget(self.attackList_listWidget)
        self.layout.addWidget(groupbox, 1, 0)

        for file in os.listdir("HealingAttack"):
            if file.endswith(".json"):
                self.savedAttackHealList_listWidget.addItem(file.split('.')[0])

    def save_load_list(self) -> None:
        groupbox = QGroupBox("Save && Load")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        groupbox_layout.addWidget(self.savedAttackHealList_listWidget)
        self.layout.addWidget(groupbox, 2, 0)

    def save_load_profile(self):
        """
        Create a small groupbox for saving & loading the heal/attack lists.
        """
        groupbox = QGroupBox("Save && Load Profile")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        save_button = QPushButton("Save", self)
        load_button = QPushButton("Load", self)

        save_button.clicked.connect(self.save_spells)
        load_button.clicked.connect(self.load_spells)

        layout0 = QHBoxLayout(self)
        layout1 = QHBoxLayout(self)

        layout0.addWidget(QLabel("Profile:", self))
        layout0.addWidget(self.profile_name_lineEdit)
        layout1.addWidget(save_button)
        layout1.addWidget(load_button)

        groupbox_layout.addLayout(layout0)
        groupbox_layout.addLayout(layout1)

        # We place this groupbox in row=2, col=1 (above the status label)
        self.layout.addWidget(groupbox, 2, 1)

    def add_heal_spell(self) -> None:
        groupbox = QGroupBox("Add Heal Action")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button
        add_healing_button = QPushButton("Add", self)
        add_healing_button.clicked.connect(self.add_heal)

        # ComboBoxes
        self.hp_mana_comboBox.addItems(["HP%", "MP%"])
        self.hotkey_rune_list_comboBox.addItems(
            ["UH", "Potion"] + [f"F{i}" for i in range(1, 13)]
        )

        # CheckBox function
        self.start_heal_checkBox.stateChanged.connect(self.check_startHeal_state)

        # Index changed
        self.hp_mana_comboBox.currentIndexChanged.connect(self.index_changed)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        layout1.addWidget(self.hp_mana_comboBox)
        layout1.addWidget(self.hotkey_rune_list_comboBox)
        layout2.addWidget(QLabel("Below:", self))
        layout2.addWidget(self.hp_below_lineEdit)
        layout2.addWidget(QLabel("Above:", self))
        layout2.addWidget(self.hp_above_lineEdit)
        layout3.addWidget(QLabel("Min MP:", self))
        layout3.addWidget(self.min_mp_lineEdit)
        layout3.addWidget(add_healing_button)
        layout4.addWidget(self.start_heal_checkBox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1)

    def add_attack_spell(self) -> None:
        groupbox = QGroupBox("Attack Hotkeys & Runes")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button
        add_attack_button = QPushButton("Add", self)
        add_attack_button.clicked.connect(self.add_attack)

        # ComboBox
        self.actionList_comboBox.addItems(
            ["HMM", "GFB", "SD"] + [f"F{i}" for i in range(1, 13)]
        )

        # CheckBox function
        self.start_attack_checkBox.stateChanged.connect(self.check_startAttack_state)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)

        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.targetName_lineEdit)
        layout2.addWidget(QLabel("Action:", self))
        layout2.addWidget(self.actionList_comboBox)
        layout2.addWidget(QLabel("Dist:", self))
        layout2.addWidget(self.spell_dist_lineEdit)
        layout3.addWidget(QLabel("From:", self))
        layout3.addWidget(self.hpFrom_lineEdit)
        layout3.addWidget(QLabel("% To:", self))
        layout3.addWidget(self.hpTo_lineEdit)
        layout3.addWidget(QLabel("%", self))
        layout4.addWidget(QLabel("Min MP:", self))
        layout4.addWidget(self.min_mp_spell_lineEdit)
        layout4.addWidget(add_attack_button)
        layout5.addWidget(self.start_attack_checkBox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)
        self.layout.addWidget(groupbox, 1, 1)

    # ---------------------- Save & Load Functions --------------------------

    def save_spells(self):
        """
        Save both healing and attacking spells to a JSON file.
        File name: "HealingAttackProfiles/<profile_name>.json"
        """
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_label.setText("")  # clear

        profile_name = self.profile_name_lineEdit.text().strip()
        if not profile_name:
            self.status_label.setText("Please enter a profile name before saving.")
            self.profile_name_lineEdit.setStyleSheet("border: 2px solid red;")
            return
        else:
            self.profile_name_lineEdit.setStyleSheet("")

        # Collect healing spells
        heal_list = []
        for i in range(self.healList_listWidget.count()):
            item = self.healList_listWidget.item(i)
            heal_data = item.data(Qt.UserRole)  # The dict we stored
            heal_list.append(heal_data)

        # Collect attack spells
        attack_list = []
        for i in range(self.attackList_listWidget.count()):
            item = self.attackList_listWidget.item(i)
            attack_data = item.data(Qt.UserRole)
            attack_list.append(attack_data)

        # Build final dictionary
        data_to_save = {
            "healing": heal_list,
            "attacking": attack_list
        }

        filename = f"HealingAttack/{profile_name}.json"
        with open(filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

        self.profile_name_lineEdit.clear()
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' saved successfully!")

    def load_spells(self):
        """
        Load healing and attacking spells from a JSON file.
        Clears current lists and repopulates them.
        """
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_label.setText("")  # clear

        profile_name = self.savedAttackHealList_listWidget.currentItem()
        if not profile_name:
            # Highlight list if nothing selected
            self.savedAttackHealList_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list.")
            return
        else:
            self.savedAttackHealList_listWidget.setStyleSheet("")
        profile_name = profile_name.text()
        filename = f"HealingAttack/{profile_name}.json"
        if not os.path.exists(filename):
            self.status_label.setText(f"No file found for '{profile_name}'.")
            return

        with open(filename, "r") as f:
            loaded_data = json.load(f)

        # Clear current lists
        self.healList_listWidget.clear()
        self.attackList_listWidget.clear()

        # Repopulate healing spells
        for heal_data in loaded_data.get("healing", []):
            # Rebuild the string name for display
            heal_name = (
                f"{heal_data['Option']} "
                f"{heal_data['Below']} > {heal_data['Type']} > "
                f"{heal_data['Above']}  MinMP={heal_data['MinMp']}"
            )
            heal_item = QListWidgetItem(heal_name)
            heal_item.setData(Qt.UserRole, heal_data)
            self.healList_listWidget.addItem(heal_item)

        # Repopulate attacking spells
        for attack_data in loaded_data.get("attacking", []):
            # We convert the 'Action' to readable text for display. But we only stored the index.
            # We'll reconstruct similarly as we did in 'add_attack'...
            # For example, we used:
            #   f"{monsters_name} {hp_from_val} > {self.actionList_comboBox.currentText()} > {hp_to_val} ...
            # We'll create a small map or list:
            all_actions = ["HMM", "GFB", "SD"] + [f"F{i}" for i in range(1, 13)]
            # Index in 'attack_data["Action"]' => all_actions[that_index]

            action_str = all_actions[attack_data["Action"]]

            attack_name = (
                f"{attack_data['Name']} {attack_data['HpFrom']} > "
                f"{action_str} > {attack_data['HpTo']}  MinMP={attack_data['MinMp']}"
                f" Distance < {attack_data['Distance']}"
            )
            attack_item = QListWidgetItem(attack_name)
            attack_item.setData(Qt.UserRole, attack_data)
            self.attackList_listWidget.addItem(attack_item)

        self.profile_name_lineEdit.clear()
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' loaded successfully!")

    # ------------------- Existing functionality (unchanged) -------------------

    def index_changed(self, index):
        if index == 1:  # MP%
            self.min_mp_lineEdit.setDisabled(True)
        else:  # HP%
            self.min_mp_lineEdit.setDisabled(False)

    def add_heal(self) -> None:
        self.status_label.setText("")
        self.hp_below_lineEdit.setStyleSheet("")
        self.hp_above_lineEdit.setStyleSheet("")

        self.status_label.setStyleSheet("color: Red; font-weight: bold;")

        has_error = False

        if not self.hp_below_lineEdit.text().strip():
            self.hp_below_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please fill in the 'Below' field.")
            has_error = True

        if not self.hp_above_lineEdit.text().strip():
            self.hp_above_lineEdit.setStyleSheet("border: 2px solid red;")
            if not has_error:
                self.status_label.setText("Please fill in the 'Above' field.")
            has_error = True

        if has_error:
            return

        self.status_label.setStyleSheet("color: Green; font-weight: bold;")

        if not self.min_mp_lineEdit.text():
            self.min_mp_lineEdit.setText("0")

        hp_below_val = int(self.hp_below_lineEdit.text())
        hp_above_val = int(self.hp_above_lineEdit.text())
        min_mp_val = int(self.min_mp_lineEdit.text())

        heal_name = (
            f"{self.hotkey_rune_list_comboBox.currentText()} "
            f"{hp_below_val} > {self.hp_mana_comboBox.currentText()} > "
            f"{hp_above_val}  MinMP={min_mp_val}"
        )

        heal_data = {
            "Type": self.hp_mana_comboBox.currentText(),
            "Option": self.hotkey_rune_list_comboBox.currentText(),
            "Below": hp_below_val,
            "Above": hp_above_val,
            "MinMp": min_mp_val
        }

        heal_item = QListWidgetItem(heal_name)
        heal_item.setData(Qt.UserRole, heal_data)
        self.healList_listWidget.addItem(heal_item)

        self.hp_above_lineEdit.clear()
        self.hp_below_lineEdit.clear()
        self.min_mp_lineEdit.clear()
        self.status_label.setText("Heal action added successfully!")

    def add_attack(self) -> None:
        self.status_label.setText("")
        self.targetName_lineEdit.setStyleSheet("")
        self.hpFrom_lineEdit.setStyleSheet("")
        self.hpTo_lineEdit.setStyleSheet("")
        self.spell_dist_lineEdit.setStyleSheet("")

        self.status_label.setStyleSheet("color: Red; font-weight: bold;")

        has_error = False

        if not self.targetName_lineEdit.text().strip():
            self.targetName_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please fill in the 'Name' field.")
            has_error = True

        if not self.hpFrom_lineEdit.text().strip():
            self.hpFrom_lineEdit.setStyleSheet("border: 2px solid red;")
            if not has_error:
                self.status_label.setText("Please fill in the 'From' field.")
            has_error = True

        if not self.hpTo_lineEdit.text().strip():
            self.hpTo_lineEdit.setStyleSheet("border: 2px solid red;")
            if not has_error:
                self.status_label.setText("Please fill in the 'To' field.")
            has_error = True

        if not self.spell_dist_lineEdit.text().strip():
            self.spell_dist_lineEdit.setStyleSheet("border: 2px solid red;")
            if not has_error:
                self.status_label.setText("Please fill in the 'Dist' field.")
            has_error = True

        if has_error:
            return

        self.status_label.setStyleSheet("color: Green; font-weight: bold;")

        if not self.min_mp_spell_lineEdit.text():
            self.min_mp_spell_lineEdit.setText("0")

        monsters_name = self.targetName_lineEdit.text().strip()
        hp_from_val = int(self.hpFrom_lineEdit.text())
        hp_to_val = int(self.hpTo_lineEdit.text())
        min_mp_val = int(self.min_mp_spell_lineEdit.text())
        dist_val = int(self.spell_dist_lineEdit.text())

        attack_name = (
            f"{monsters_name} {hp_from_val} > "
            f"{self.actionList_comboBox.currentText()} > "
            f"{hp_to_val}  MinMP={min_mp_val}"
            f" Distance < {dist_val}"
        )

        attack_data = {
            "Name": monsters_name,
            "Action": self.actionList_comboBox.currentIndex(),
            "HpFrom": hp_from_val,
            "HpTo": hp_to_val,
            "MinMp": min_mp_val,
            "Distance": dist_val
        }

        attack_item = QListWidgetItem(attack_name)
        attack_item.setData(Qt.UserRole, attack_data)
        self.attackList_listWidget.addItem(attack_item)

        self.hpFrom_lineEdit.clear()
        self.hpTo_lineEdit.clear()
        self.min_mp_spell_lineEdit.clear()
        self.targetName_lineEdit.clear()
        self.spell_dist_lineEdit.clear()
        self.status_label.setText("Attack action added successfully!")

    def check_startHeal_state(self) -> None:
        thread = Thread(target=self.start_healing_thread)
        thread.daemon = True
        if self.start_heal_checkBox.checkState() == 2:
            thread.start()

    def check_startAttack_state(self) -> None:
        thread = Thread(target=self.start_attacking_thread)
        thread.daemon = True
        if self.start_attack_checkBox.checkState() == 2:
            thread.start()

    def start_attacking_thread(self):
        while self.start_attack_checkBox.checkState() == 2:
            try:
                for attack_index in range(self.attackList_listWidget.count()):
                    attack_data = self.attackList_listWidget.item(attack_index).data(Qt.UserRole)

                    # Ensure attack_data contains valid data
                    if not attack_data:
                        print(f"Invalid attack data at index {attack_index}.")
                        continue

                    target_hp = attack_data.get('HpFrom', None)
                    if target_hp is None or attack_data.get('HpTo', None) is None:
                        print(f"Invalid target HP range in attack data: {attack_data}")
                        continue

                    if read_memory_address(Addresses.attack_address, 0, 2) != 0:
                        current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                        target_x, target_y, target_name, target_hp = read_target_info()
                        x, y, z = read_my_wpt()

                        if current_hp is None or current_max_hp is None or current_mp is None or current_max_mp is None:
                            print("Failed to read player stats.")
                            continue

                        if target_x is None or target_y is None or target_name is None or target_hp is None:
                            print("Failed to read target info.")
                            continue

                        # If the "Action" index is above 2, it might be a hotkey
                        if (
                            attack_data['Action'] > 2
                            and (int(attack_data['HpFrom']) >= target_hp > int(attack_data['HpTo']))
                            and current_mp >= int(attack_data['MinMp'])
                            and (attack_data['Name'] == '*' or target_name in attack_data['Name'])
                            and (attack_data['Distance'] >= abs(x - target_x)
                                 and attack_data['Distance'] >= abs(y - target_y))
                        ):
                            press_hotkey(attack_data['Action'] - 2)
                            time.sleep(random.uniform(0.3, 0.6))
                            break
            except Exception as e:
                print(f"Error in start_attacking_thread: {e}")
                time.sleep(random.uniform(0.1, 0.3))

    def start_healing_thread(self):
        healed = True
        heal_multiplayer = 0.0
        while self.start_heal_checkBox.checkState() == 2:
            try:
                if healed:
                    heal_multiplayer = random.uniform(0.9, 1.0)
                    healed = False
                for heal_index in range(self.healList_listWidget.count()):
                    heal_data = self.healList_listWidget.item(heal_index).data(Qt.UserRole)
                    heal_type = heal_data['Type']
                    heal_option = heal_data['Option']
                    heal_below = heal_data['Below']
                    heal_above = heal_data['Above']
                    heal_min_mp = heal_data['MinMp']
                    heal_below = heal_below * heal_multiplayer
                    heal_above = heal_above * heal_multiplayer

                    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                    if current_hp is None or current_max_hp is None or current_mp is None or current_max_mp is None:
                        print("Failed to read stats.")
                        continue
                    # HP-based healing
                    if heal_type.startswith("HP"):
                        hp_percentage = (current_hp * 100) / current_max_hp
                        if heal_option == "UH":
                            if heal_below >= hp_percentage >= heal_above:
                                time.sleep(random.uniform(0.1, 0.2))
                                use_on_me(coordinates_x[5], coordinates_y[5])
                                healed = True
                        else:
                            # Potions or hotkeys (F1..F12)
                            if heal_below >= hp_percentage >= heal_above and current_mp >= heal_min_mp:
                                time.sleep(random.uniform(0.1, 0.2))
                                press_hotkey(int(heal_option[1:]))
                                healed = True
                    # MP-based healing
                    elif heal_type.startswith("MP"):
                        mp_percentage = (current_mp * 100) / current_max_mp
                        if heal_below >= mp_percentage >= heal_above:
                            time.sleep(random.uniform(0.1, 0.2))
                            press_hotkey(int(heal_option[1:]))
                            healed = True

                # Delay to prevent overloading
                time.sleep(random.uniform(0.1, 0.2))

            except Exception as e:
                print(f"Error in healing thread: {e}")

