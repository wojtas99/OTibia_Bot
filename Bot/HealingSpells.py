import Addresses
from Addresses import icon_image, coordinates_x, coordinates_y, testy
import base64
import time
from threading import Thread
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QLabel, QListWidget, QGridLayout,
    QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from MemoryFunctions import read_memory_address
from MouseFunctions import use_on_me, right_click, left_click
from KeyboardFunctions import press_hotkey
from Functions import read_my_stats, read_my_wpt, read_target_info

import base64
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout,
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class HealingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Spells&Healing")
        self.setFixedSize(500, 480)

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

        # List Widgets
        self.healList_listWidget = QListWidget(self)
        self.attackList_listWidget = QListWidget(self)

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize
        self.heal_list()
        self.attack_hotkey_rune()
        self.add_heal_spell()
        self.add_attack_spell()

    def add_heal_spell(self) -> None:
        groupbox = QGroupBox("Add Heal Action")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        add_healing_button = QPushButton("Add", self)

        # Button functions
        add_healing_button.clicked.connect(self.add_heal)

        # Combo Boxes
        self.hp_mana_comboBox.addItems(["HP%", "HP", "MP%", "MP"])
        self.hotkey_rune_list_comboBox.addItems(
            ["UH", "Potion"] + [f"F{i}" for i in range(1, 13)]
        )

        # Check box function
        self.start_heal_checkBox.stateChanged.connect(self.check_startHeal_state)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)

        # Add widgets to layouts
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

        # Add layouts to groupbox
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        self.layout.addWidget(groupbox, 0, 1)

    def add_attack_spell(self) -> None:
        groupbox = QGroupBox("Attack Hotkeys && Runes")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        add_attack_button = QPushButton("Add", self)

        # Button functions
        add_attack_button.clicked.connect(self.add_attack)

        # Combo Boxes
        self.actionList_comboBox.addItems(
            ["HMM", "GFB", "SD"] + [f"F{i}" for i in range(1, 13)]
        )

        # Check box function
        self.start_attack_checkBox.stateChanged.connect(self.check_startAttack_state)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout5 = QHBoxLayout(self)

        # Add widgets to layouts
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

        # Add layouts to groupbox
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        groupbox_layout.addLayout(layout3)
        groupbox_layout.addLayout(layout4)
        groupbox_layout.addLayout(layout5)
        self.layout.addWidget(groupbox, 1, 1)

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

    def add_heal(self) -> None:
        if not self.min_mp_lineEdit.text():
            self.min_mp_lineEdit.setText("0")

        heal_name = (
            f"{self.hotkey_rune_list_comboBox.currentText()} "
            f"{int(self.hp_below_lineEdit.text())} > "
            f"{self.hp_mana_comboBox.currentText()} > "
            f"{int(self.hp_above_lineEdit.text())}  "
            f"MinMP={self.min_mp_lineEdit.text()}"
        )

        if heal_name:
            heal_data = {
                "Type": self.hp_mana_comboBox.currentText(),
                "Option": self.hotkey_rune_list_comboBox.currentText(),
                "Below": int(self.hp_below_lineEdit.text()),
                "Above": int(self.hp_above_lineEdit.text()),
                "MinMp": int(self.min_mp_lineEdit.text())
            }
            heal = QListWidgetItem(heal_name)
            heal.setData(Qt.UserRole, heal_data)
            self.healList_listWidget.addItem(heal)
            self.hp_above_lineEdit.clear()
            self.hp_below_lineEdit.clear()
            self.min_mp_lineEdit.clear()

    def add_attack(self) -> None:
        if not self.min_mp_spell_lineEdit.text():
            self.min_mp_spell_lineEdit.setText("0")

        monsters_name = self.targetName_lineEdit.text()
        attack_name = (
            f"{monsters_name} {int(self.hpFrom_lineEdit.text())} > "
            f"{self.actionList_comboBox.currentText()} > "
            f"{int(self.hpTo_lineEdit.text())}  "
            f"MinMP={self.min_mp_spell_lineEdit.text()}"
            f" Distance < {self.spell_dist_lineEdit.text()}"
        )

        if attack_name:
            attack_data = {
                "Name": self.targetName_lineEdit.text(),
                "Action": self.actionList_comboBox.currentIndex(),
                "HpFrom": int(self.hpFrom_lineEdit.text()),
                "HpTo": int(self.hpTo_lineEdit.text()),
                "MinMp": int(self.min_mp_spell_lineEdit.text()),
                "Distance": int(self.spell_dist_lineEdit.text())
            }
            attack = QListWidgetItem(attack_name)
            attack.setData(Qt.UserRole, attack_data)
            self.attackList_listWidget.addItem(attack)
            self.hpFrom_lineEdit.clear()
            self.hpTo_lineEdit.clear()
            self.min_mp_spell_lineEdit.clear()
            self.targetName_lineEdit.clear()

    def check_startHeal_state(self) -> None:
        """
        Checks if healing should start and creates a separate thread for healing.
        """
        thread = Thread(target=self.start_healing_thread)
        thread.daemon = True
        if self.start_heal_checkBox.checkState() == 2:
            thread.start()

    def check_startAttack_state(self) -> None:
        """
        Checks if attack should start and creates a separate thread for healing.
        """
        thread = Thread(target=self.start_attacking_thread)
        thread.daemon = True
        if self.start_attack_checkBox.checkState() == 2:
            thread.start()

    def start_attacking_thread(self):
        """
        Thread method to handle automatic spell attacking based on the target's HP and MP levels.
        """
        while self.start_attack_checkBox.checkState() == 2:
            for attack_index in range(self.attackList_listWidget.count()):
                attack_data = self.attackList_listWidget.item(attack_index).data(Qt.UserRole)
                if read_memory_address(Addresses.attack_address, 0, 2) != 0:
                    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                    target_x, target_y, target_name, target_hp = read_target_info()
                    x, y, z = read_my_wpt()
                    if (attack_data['Action'] > 2 and (int(attack_data['HpFrom']) >= target_hp > int(attack_data['HpTo']))
                            and current_mp >= int(attack_data['MinMp'])
                            and (attack_data['Name'] == '*' or target_name in attack_data['Name'])
                            and (attack_data['Distance'] >= abs(x - target_x) and attack_data['Distance'] >= abs(y - target_y))):
                        press_hotkey(attack_data['Action'] - 2)
                        time.sleep(0.1)
                        break
                    if (attack_data['Action'] < 2 and (int(attack_data['HpFrom']) >= target_hp > int(attack_data['HpTo']))
                            and current_mp >= int(attack_data['MinMp'])
                            and (attack_data['Name'] == '*' or target_name in attack_data['Name'])
                            and (attack_data['Distance'] >= abs(x - target_x) and attack_data['Distance'] >= abs(y - target_y))):
                        right_click(coordinates_x[6], coordinates_y[6])
                        time.sleep(0.1)
                        x = target_x - x
                        y = target_y - y
                        left_click(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75)
                        break

    def start_healing_thread(self):
        """
        Thread method to handle automatic healing based on the player's HP and MP levels.
        """
        while self.start_heal_checkBox.checkState() == 2:
            for heal_index in range(self.healList_listWidget.count()):
                heal_data = self.healList_listWidget.item(heal_index).data(Qt.UserRole)
                heal_type = heal_data['Type']
                heal_option = heal_data['Option']
                heal_below = heal_data['Below']
                heal_above = heal_data['Above']
                heal_min_mp = heal_data['MinMp']

                current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                time.sleep(0.1)
                if heal_type[:2] == "HP":
                    if heal_option == "UH":
                        if '%' in heal_type:
                            if heal_below >= (current_hp * 100) / current_max_hp >= heal_above:
                                if not testy.locked():
                                    testy.acquire()
                                use_on_me(coordinates_x[5], coordinates_y[5])
                                time.sleep(0.1)
                                heal_index = 0
                        else:
                            if heal_below >= current_hp >= heal_above:
                                if not testy.locked():
                                    testy.acquire()
                                use_on_me(coordinates_x[5], coordinates_y[5])
                                time.sleep(0.1)
                                heal_index = 0
                    else:
                        if '%' in heal_type:
                            if heal_below >= (
                                    current_hp * 100) / current_max_hp >= heal_above and current_mp >= heal_min_mp:
                                if not testy.locked():
                                    testy.acquire()
                                press_hotkey(int(heal_option[1:]))
                                time.sleep(0.1)
                                heal_index = 0
                        else:
                            if heal_below >= current_hp >= heal_above and current_mp >= heal_min_mp:
                                if not testy.locked():
                                    testy.acquire()
                                press_hotkey(int(heal_option[1:]))
                                time.sleep(0.1)
                                heal_index = 0
                else:
                    if '%' in heal_type:
                        if heal_below >= (current_mp * 100) / current_max_mp >= heal_above:
                            press_hotkey(int(heal_option[1:]))
                            time.sleep(0.1)
                            heal_index = 0
                if testy.locked():
                    testy.release()
