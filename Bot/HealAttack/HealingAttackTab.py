import base64, json, os
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout, QGroupBox, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QFormLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt5.QtCore import Qt
from Addresses import icon_image
from HealAttack.HealingAttackThread import HealThread, AttackThread
from Functions.GeneralFunctions import delete_item, manage_profile


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.attack_thread = None
        self.heal_thread = None

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)) else QIcon()
        )
        # Set Title and Size
        self.setWindowTitle("Healing & Attack")
        self.setFixedSize(450, 550)

        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: Red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Check Boxes
        self.startHeal_checkBox = QCheckBox("Start Heal", self)
        self.startAttack_checkBox = QCheckBox("Start Attack", self)

        # Combo Boxes
        # Heal
        self.healType_comboBox = QComboBox(self)
        self.healKey_comboBox = QComboBox(self)

        # Attack
        self.attackType_comboBox = QComboBox(self)
        self.attackKey_comboBox = QComboBox(self)


        # Line Edits
        # Heal
        self.hpBelow_lineEdit = QLineEdit(self)
        self.hpBelow_lineEdit.setFixedWidth(40)
        self.hpAbove_lineEdit = QLineEdit(self)
        self.hpAbove_lineEdit.setFixedWidth(40)
        self.minMPHeal_lineEdit = QLineEdit(self)

        # Attack
        self.targetName_lineEdit = QLineEdit(self)
        self.hpFrom_lineEdit = QLineEdit(self)
        self.hpFrom_lineEdit.setFixedWidth(40)
        self.hpFrom_lineEdit.setMaxLength(3)
        self.hpTo_lineEdit = QLineEdit(self)
        self.hpTo_lineEdit.setFixedWidth(40)
        self.hpTo_lineEdit.setMaxLength(2)
        self.minMPAttack_lineEdit = QLineEdit(self)
        self.minMPAttack_lineEdit.setFixedWidth(40)
        self.minHPAttack_lineEdit = QLineEdit(self)
        self.minHPAttack_lineEdit.setFixedWidth(40)
        self.targetCount_lineEdit = QLineEdit(self)
        self.targetCount_lineEdit.setFixedWidth(40)
        self.profile_lineEdit = QLineEdit(self)

        int_validator_3 = QIntValidator(0, 9999, self)
        int_validator_2 = QIntValidator(1, 100, self)
        int_validator_1 = QIntValidator(0, 99, self)

        self.hpTo_lineEdit.setValidator(int_validator_1)
        self.minHPAttack_lineEdit.setValidator(int_validator_1)

        self.targetCount_lineEdit.setValidator(int_validator_2)
        self.hpBelow_lineEdit.setValidator(int_validator_2)
        self.hpAbove_lineEdit.setValidator(int_validator_2)
        self.hpFrom_lineEdit.setValidator(int_validator_2)

        self.minMPHeal_lineEdit.setValidator(int_validator_3)
        self.minMPAttack_lineEdit.setValidator(int_validator_3)

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
        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)

        # Initialize sections
        self.healList()
        self.attackList()
        self.profileList()
        # Finally add the status label at the bottom row
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

        for file in os.listdir("Save/HealingAttack"):
            if file.endswith(".json"):
                self.savedAttackHealList_listWidget.addItem(file.split('.')[0])

    def healList(self) -> None:
        groupbox = QGroupBox("Healing")
        groupbox_layout = QHBoxLayout(self)
        groupbox.setLayout(groupbox_layout)


        # Button
        addHeal_button = QPushButton("Add", self)
        addHeal_button.clicked.connect(self.add_heal)

        # ComboBoxes
        self.healType_comboBox.addItems(["HP%", "MP%"])
        self.healKey_comboBox.addItems(
             [f"F{i}" for i in range(1, 13)] + ["UH", "Potion"]
        )

        # CheckBox function
        self.startHeal_checkBox.stateChanged.connect(self.startHeal_thread)

        # Index changed
        self.healType_comboBox.currentIndexChanged.connect(self.index_changed)

        # Layouts
        groupbox_layout2 = QVBoxLayout(self)

        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("When:", self))
        layout1.addWidget(self.healType_comboBox)

        layout2 = QHBoxLayout(self)
        layout2.addWidget(QLabel("Value:  ", self))
        layout2.addWidget(self.hpBelow_lineEdit)
        layout2.addWidget(QLabel("-", self))
        layout2.addWidget(self.hpAbove_lineEdit)

        layout3 = QHBoxLayout(self)
        layout3.addWidget(QLabel("Press:"))
        layout3.addWidget(self.healKey_comboBox)

        layout4 = QHBoxLayout(self)
        layout4.addWidget(QLabel("Min MP:"))
        layout4.addWidget(self.minMPHeal_lineEdit)

        layout5 = QHBoxLayout(self)
        layout5.addWidget(addHeal_button)
        layout5.addWidget(self.startHeal_checkBox)

        groupbox_layout2.addLayout(layout1)
        groupbox_layout2.addLayout(layout2)
        groupbox_layout2.addLayout(layout3)
        groupbox_layout2.addLayout(layout4)
        groupbox_layout2.addLayout(layout5)

        self.hpBelow_lineEdit.setPlaceholderText("85")
        self.hpAbove_lineEdit.setPlaceholderText("60")
        self.minMPHeal_lineEdit.setPlaceholderText("90")

        groupbox_layout.addWidget(self.healList_listWidget)
        groupbox_layout.addLayout(groupbox_layout2)
        self.layout.addWidget(groupbox, 0, 0, 1, 2)

    def attackList(self) -> None:
        groupbox = QGroupBox("Attack")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button
        add_attack_button = QPushButton("Add", self)
        add_attack_button.clicked.connect(self.add_attack)

        # ComboBox
        self.attackType_comboBox.addItems(
            ["Exori, Exori Gran", "Exori Mas, Exevo Mas San",
             "Exevo Gran Mas Vis, Exevo Gran Mas Flam",
             "Avalanche, Great Fire Ball",
             "Exori Hur, Exori Flam"]
        )

        self.attackKey_comboBox.addItems(
            [f"F{i}" for i in range(1, 13)] + ["HMM", "GFB", "SD"]
        )

        # CheckBox function
        self.startAttack_checkBox.stateChanged.connect(self.start_attack_thread)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        layout1.addWidget(self.attackKey_comboBox)
        layout1.addWidget(QLabel("Min. Creatures:", self), alignment=Qt.AlignLeft)
        layout1.addWidget(self.targetCount_lineEdit)
        self.targetCount_lineEdit.setPlaceholderText("1")
        layout1.addWidget(QLabel("HP:", self), alignment=Qt.AlignLeft)
        layout1.addWidget(self.hpFrom_lineEdit)
        layout1.addWidget(QLabel(" -", self), alignment=Qt.AlignLeft)
        layout1.addWidget(self.hpTo_lineEdit, alignment=Qt.AlignLeft)
        layout1.addWidget(QLabel("Min MP:", self))
        layout1.addWidget(self.minMPAttack_lineEdit)

        self.minMPAttack_lineEdit.setPlaceholderText("300")
        self.hpFrom_lineEdit.setPlaceholderText("100")
        self.hpTo_lineEdit.setPlaceholderText("0")
        self.minHPAttack_lineEdit.setPlaceholderText("50")

        layout2.addWidget(self.targetName_lineEdit)
        self.targetName_lineEdit.setPlaceholderText("Orc, Minotaur, etc., * - All monsters")
        layout2.addWidget(QLabel("Min HP%:", self))
        layout2.addWidget(self.minHPAttack_lineEdit)

        layout4.addWidget(self.attackType_comboBox)
        layout4.addWidget(add_attack_button)
        layout4.addWidget(self.startAttack_checkBox)

        groupbox_layout.addWidget(self.attackList_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 1, 0, 1, 2)

    def profileList(self) -> None:

        # Layouts
        groupbox = QGroupBox("Save && Load")
        groupbox_layout = QHBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        groupbox2_layout = QVBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Buttons
        save_button = QPushButton("Save", self)
        load_button = QPushButton("Load", self)

        save_button.clicked.connect(self.save_profile)
        load_button.clicked.connect(self.load_profile)

        # Add Widgets
        layout1.addWidget(QLabel("Profile:", self))
        layout1.addWidget(self.profile_lineEdit)
        layout2.addWidget(save_button)
        layout2.addWidget(load_button)

        # Add Layouts
        groupbox2_layout.addLayout(layout1)
        groupbox2_layout.addLayout(layout2)

        # Final
        groupbox_layout.addWidget(self.savedAttackHealList_listWidget)
        groupbox_layout.addLayout(groupbox2_layout)
        self.layout.addWidget(groupbox, 2, 0)


    def save_profile(self):
        profile_name = self.profile_lineEdit.text().strip()
        if not profile_name:
            return
        heal_list = [
            self.healList_listWidget.item(i).data(Qt.UserRole)
            for i in range(self.healList_listWidget.count())
        ]
        attack_list = [
            self.attackList_listWidget.item(i).data(Qt.UserRole)
            for i in range(self.attackList_listWidget.count())
        ]
        data_to_save = {
            "healing": heal_list,
            "attacking": attack_list
        }

        if manage_profile("save", "Save/HealingAttack", profile_name, data_to_save):
            self.status_label.setText(f"Profil '{profile_name}' zapisany!")
        else:
            self.status_label.setText("Błąd przy zapisie profilu.")

    def load_profile(self):
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
        filename = f"Save/HealingAttack/{profile_name}.json"
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
                f"{heal_data['Type']} From {heal_data['Below']} To {heal_data['Above']}"
                f"Min MP {heal_data['MinMp']} Press " +
                f"{heal_data['Option']} "
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

        self.profile_lineEdit.clear()
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' loaded successfully!")


    def index_changed(self, index):
        if index == 1:  # MP%
            self.minMPHeal_lineEdit.setDisabled(True)
        else:  # HP%
            self.minMPHeal_lineEdit.setDisabled(False)

    def add_heal(self) -> None:
        self.status_label.setText("")
        self.hpBelow_lineEdit.setStyleSheet("")
        self.hpAbove_lineEdit.setStyleSheet("")

        self.status_label.setStyleSheet("color: Red; font-weight: bold;")

        has_error = False

        if not self.hpBelow_lineEdit.text().strip():
            self.hpBelow_lineEdit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please fill in the 'Below' field.")
            has_error = True

        if not self.hpAbove_lineEdit.text().strip():
            self.hpAbove_lineEdit.setStyleSheet("border: 2px solid red;")
            if not has_error:
                self.status_label.setText("Please fill in the 'Above' field.")
            has_error = True

        if has_error:
            return

        self.status_label.setStyleSheet("color: Green; font-weight: bold;")

        if not self.minMPHeal_lineEdit.text():
            self.minMPHeal_lineEdit.setText("0")

        hp_below_val = int(self.hpBelow_lineEdit.text())
        hp_above_val = int(self.hpAbove_lineEdit.text())
        min_mp_val = int(self.minMPHeal_lineEdit.text())

        heal_name = (
                f"{self.healType_comboBox.currentText()}  {hp_below_val}-{hp_above_val}"
                f"  :  Press " +
                f"{self.healKey_comboBox.currentText()} "
        )

        heal_data = {
            "Type": self.healType_comboBox.currentText(),
            "Option": self.healKey_comboBox.currentText(),
            "Below": hp_below_val,
            "Above": hp_above_val,
            "MinMp": min_mp_val
        }

        heal_item = QListWidgetItem(heal_name)
        heal_item.setData(Qt.UserRole, heal_data)
        self.healList_listWidget.addItem(heal_item)

        self.hpAbove_lineEdit.clear()
        self.hpBelow_lineEdit.clear()
        self.minMPHeal_lineEdit.clear()
        self.status_label.setText("Heal action added successfully!")

    def add_attack(self) -> None:
        self.status_label.setText("")
        self.targetName_lineEdit.setStyleSheet("")
        self.hpFrom_lineEdit.setStyleSheet("")
        self.hpTo_lineEdit.setStyleSheet("")
        self.targetCount_lineEdit.setStyleSheet("")

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

        if not self.targetCount_lineEdit.text().strip():
            self.targetCount_lineEdit.setStyleSheet("border: 2px solid red;")
            if not has_error:
                self.status_label.setText("Please fill in the 'Min Creatures' field.")
            has_error = True

        if has_error:
            return

        self.status_label.setStyleSheet("color: Green; font-weight: bold;")

        if not self.minMPAttack_lineEdit.text():
            self.minMPAttack_lineEdit.setText("0")
        if not self.minHPAttack_lineEdit.text():
            self.minHPAttack_lineEdit.setText("0")

        monsters_name = self.targetName_lineEdit.text().strip()
        hp_from_val = int(self.hpFrom_lineEdit.text())
        hp_to_val = int(self.hpTo_lineEdit.text())
        min_mp_val = int(self.minMPAttack_lineEdit.text())
        min_hp_val = int(self.minHPAttack_lineEdit.text())
        count_val = int(self.targetCount_lineEdit.text())


        attack_name = (
            f"{monsters_name} {hp_from_val}>"
            f"{self.attackKey_comboBox.currentText()}>"
            f"{hp_to_val}  MinMP={min_mp_val} MinHP%={min_hp_val}"
            f" Count={count_val}+"
        )

        attack_data = {
            "Name": monsters_name,
            "Action": self.attackKey_comboBox.currentIndex(),
            "HpFrom": hp_from_val,
            "HpTo": hp_to_val,
            "MinMp": min_mp_val,
            "MinHp": min_hp_val,
            "Count": count_val
        }

        attack_item = QListWidgetItem(attack_name)
        attack_item.setData(Qt.UserRole, attack_data)
        self.attackList_listWidget.addItem(attack_item)

        self.hpFrom_lineEdit.clear()
        self.hpTo_lineEdit.clear()
        self.minMPAttack_lineEdit.clear()
        self.minHPAttack_lineEdit.clear()
        self.targetCount_lineEdit.clear()
        self.targetName_lineEdit.clear()
        self.status_label.setText("Attack action added successfully!")

    def startHeal_thread(self, state) -> None:
        if state == Qt.Checked:
            if not self.heal_thread:
                self.heal_thread = HealThread(self.healList_listWidget)
                self.heal_thread.start()
        else:
            if self.heal_thread:
                self.heal_thread.stop()
                self.heal_thread = None

    def start_attack_thread(self, state) -> None:
        if state == Qt.Checked:
            if not self.attack_thread:
                self.attack_thread = AttackThread(self.attackList_listWidget)
                self.attack_thread.start()
        else:
            if self.attack_thread:
                self.attack_thread.stop()
                self.attack_thread = None



