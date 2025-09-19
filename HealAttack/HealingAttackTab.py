import json, os
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout, QGroupBox, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QFormLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt5.QtCore import Qt
from HealAttack.HealingAttackThread import HealThread, AttackThread
from Functions.GeneralFunctions import delete_item, manage_profile


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.attack_thread = None
        self.heal_thread = None

        # Load Icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))
        # Set Title and Size
        self.setWindowTitle("Healing & Attack")
        self.setFixedSize(450, 550)

        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: Red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Check Boxes
        self.startHeal_checkBox = QCheckBox("Start", self)
        self.startAttack_checkBox = QCheckBox("Start", self)

        # Combo Boxes
        # Heal
        self.healType_comboBox = QComboBox(self)
        self.healKey_comboBox = QComboBox(self)

        # Attack
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
        self.hpFrom_lineEdit.setFixedWidth(30)
        self.hpFrom_lineEdit.setMaxLength(3)
        self.hpTo_lineEdit = QLineEdit(self)
        self.hpTo_lineEdit.setFixedWidth(30)
        self.hpTo_lineEdit.setMaxLength(2)
        self.minMPAttack_lineEdit = QLineEdit(self)
        self.minMPAttack_lineEdit.setFixedWidth(30)
        self.minHPAttack_lineEdit = QLineEdit(self)
        self.minHPAttack_lineEdit.setFixedWidth(30)
        self.profile_lineEdit = QLineEdit(self)

        int_validator_3 = QIntValidator(0, 9999, self)
        int_validator_2 = QIntValidator(1, 100, self)
        int_validator_1 = QIntValidator(0, 99, self)

        self.hpTo_lineEdit.setValidator(int_validator_1)
        self.minHPAttack_lineEdit.setValidator(int_validator_1)
        self.hpBelow_lineEdit.setValidator(int_validator_2)
        self.hpAbove_lineEdit.setValidator(int_validator_2)
        self.hpFrom_lineEdit.setValidator(int_validator_2)

        self.minMPHeal_lineEdit.setValidator(int_validator_3)
        self.minMPAttack_lineEdit.setValidator(int_validator_3)


        # List Widgets
        self.healList_listWidget = QListWidget(self)
        self.attackList_listWidget = QListWidget(self)
        self.profile_listWidget = QListWidget(self)

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
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

        for file in os.listdir("Save/HealingAttack"):
            if file.endswith(".json"):
                self.profile_listWidget.addItem(file.split('.')[0])

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
            [f"F{i}" for i in range(1, 10)] + ["Health", "Mana"]
        )

        # CheckBox function
        self.startHeal_checkBox.stateChanged.connect(self.startHeal_thread)

        # Layouts
        groupbox2_layout = QVBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(QLabel("When:", self))
        layout1.addWidget(self.healType_comboBox)
        layout2.addWidget(QLabel("Value:  ", self))

        layout2.addWidget(self.hpBelow_lineEdit)
        layout2.addWidget(QLabel("-", self))
        layout2.addWidget(self.hpAbove_lineEdit)

        layout3.addWidget(QLabel("Press:"))
        layout3.addWidget(self.healKey_comboBox)

        layout4.addWidget(QLabel("Min MP:"))
        layout4.addWidget(self.minMPHeal_lineEdit)

        layout5.addWidget(addHeal_button)
        layout5.addWidget(self.startHeal_checkBox)

        self.hpBelow_lineEdit.setPlaceholderText("85")
        self.hpAbove_lineEdit.setPlaceholderText("60")
        self.minMPHeal_lineEdit.setPlaceholderText("90")

        groupbox2_layout.addLayout(layout1)
        groupbox2_layout.addLayout(layout2)
        groupbox2_layout.addLayout(layout3)
        groupbox2_layout.addLayout(layout4)
        groupbox2_layout.addLayout(layout5)

        groupbox_layout.addWidget(self.healList_listWidget)
        groupbox_layout.addLayout(groupbox2_layout)
        self.layout.addWidget(groupbox, 0, 0, 1, 2)

    def attackList(self) -> None:
        groupbox = QGroupBox("Attack")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Button
        add_attack_button = QPushButton("Add", self)
        add_attack_button.clicked.connect(self.add_attack)

        # ComboBox
        self.attackKey_comboBox.addItems(
            [f"F{i}" for i in range(1, 10)] + ["First Rune", "Second Rune"]
        )

        # CheckBox function
        self.startAttack_checkBox.stateChanged.connect(self.start_attack_thread)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)


        layout1.addWidget(self.targetName_lineEdit)
        self.targetName_lineEdit.setPlaceholderText("Orc, Minotaur, etc., * - All Monsters")
        layout1.addWidget(QLabel("Key:", self), alignment=Qt.AlignLeft)
        layout1.addWidget(self.attackKey_comboBox)

        layout2.addWidget(QLabel("HP%:", self), alignment=Qt.AlignLeft)
        layout2.addWidget(self.hpFrom_lineEdit)
        layout2.addWidget(QLabel(" -", self), alignment=Qt.AlignLeft)
        layout2.addWidget(self.hpTo_lineEdit, alignment=Qt.AlignLeft)
        layout2.addWidget(QLabel("Min. MP:", self))
        layout2.addWidget(self.minMPAttack_lineEdit)
        layout2.addWidget(QLabel("Min. HP%:", self))
        layout2.addWidget(self.minHPAttack_lineEdit)

        self.minMPAttack_lineEdit.setPlaceholderText("300")
        self.hpFrom_lineEdit.setPlaceholderText("100")
        self.hpTo_lineEdit.setPlaceholderText("0")
        self.minHPAttack_lineEdit.setPlaceholderText("50")


        layout2.addWidget(add_attack_button)
        layout2.addWidget(self.startAttack_checkBox)

        groupbox_layout.addWidget(self.attackList_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
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
        groupbox_layout.addWidget(self.profile_listWidget)
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
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.status_label.setText(f"Profile '{profile_name}' has been saved!")
            existing_names = [
                self.profile_listWidget.item(i).text()
                for i in range(self.profile_listWidget.count())
            ]
            if profile_name not in existing_names:
                self.profile_listWidget.addItem(profile_name)

    def load_profile(self):
        profile_name = self.profile_listWidget.currentItem()
        if not profile_name:
            self.profile_listWidget.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please select a profile from the list.")
            return
        else:
            self.profile_listWidget.setStyleSheet("")
        profile_name = profile_name.text()
        filename = f"Save/HealingAttack/{profile_name}.json"

        with open(filename, "r") as f:
            loaded_data = json.load(f)

        self.healList_listWidget.clear()
        self.attackList_listWidget.clear()

        for heal_data in loaded_data.get("healing", []):
            heal_name = (
                    f"{heal_data['Type']}  {heal_data['Below']}-{heal_data['Above']}"
                    f"  :  Use " +
                    f"{heal_data['Key']} "
            )
            heal_item = QListWidgetItem(heal_name)
            heal_item.setData(Qt.UserRole, heal_data)
            self.healList_listWidget.addItem(heal_item)

        for attack_data in loaded_data.get("attacking", []):
            attack_name = (
                f"{attack_data['Name']} : ({attack_data['HpFrom']}%-{attack_data['HpTo']}%)"
                f"  :  Use {attack_data['Key']}"
            )
            attack_item = QListWidgetItem(attack_name)
            attack_item.setData(Qt.UserRole, attack_data)
            self.attackList_listWidget.addItem(attack_item)

        self.profile_lineEdit.clear()
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText(f"Profile '{profile_name}' loaded successfully!")

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
                f"  :  Press "
                f"{self.healKey_comboBox.currentText()} "
        )

        heal_data = {
            "Type": self.healType_comboBox.currentText(),
            "Key": self.healKey_comboBox.currentText(),
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

        attack_name = (
            f"{monsters_name} : ({hp_from_val}%-{hp_to_val}%)"
            f"  :  Use {self.attackKey_comboBox.currentText()}"
        )

        attack_data = {
            "Name": monsters_name,
            "Key": self.attackKey_comboBox.currentText(),
            "HpFrom": hp_from_val,
            "HpTo": hp_to_val,
            "MinMp": min_mp_val,
            "MinHp": min_hp_val,
        }

        attack_item = QListWidgetItem(attack_name)
        attack_item.setData(Qt.UserRole, attack_data)
        self.attackList_listWidget.addItem(attack_item)

        self.hpFrom_lineEdit.clear()
        self.hpTo_lineEdit.clear()
        self.minMPAttack_lineEdit.clear()
        self.minHPAttack_lineEdit.clear()
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
