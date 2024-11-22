import win32gui
import Addresses
from Addresses import icon_image, coordinates_x, coordinates_y, screen_width, screen_height,  screen_x, screen_y, lock
import base64
import os
import json
import time
import numpy as np
import cv2 as cv
from threading import Thread
from Functions import read_my_wpt, read_target_info
from KeyboardFunctions import walk

import win32con
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QGridLayout,
    QGroupBox, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from MemoryFunctions import read_memory_address

from MouseFunctions import right_click
from MouseFunctions import drag_drop
from MouseFunctions import collect_item, left_click

from GeneralFunctions import WindowCapture
from GeneralFunctions import merge_close_points


class TargetLootTab(QWidget):
    def __init__(self, parent=None):
        super(TargetLootTab, self).__init__(parent)

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Targeting")
        self.setFixedSize(350, 400)

        # Check Boxes
        self.startLoot_checkBox = QCheckBox("Open Corpses", self)
        self.startTarget_checkBox = QCheckBox("Start Targeting", self)
        self.chase_checkBox = QCheckBox("Chase", self)

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

        # Layouts
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Initialize UI components
        self.target_list()
        self.save_load_target_loot()
        self.set_target()
        self.loot_list()
        self.target_loot()

    def target_list(self) -> None:
        groupbox = QGroupBox("Target List", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        delete_target_button = QPushButton("Del", self)
        clear_targets_button = QPushButton("Clear", self)

        # Button functions
        delete_target_button.clicked.connect(self.delete_target)
        clear_targets_button.clicked.connect(self.clear_targets_list)

        # Layouts
        layout1 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(delete_target_button)
        layout1.addWidget(clear_targets_button)

        # Add Layouts
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

        # Populate list widget
        for file in os.listdir("Targeting"):
            self.targetLootProfile_listWidget.addItem(f"{file.split('.')[0]}")

        # Layouts for input fields and buttons
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout1.addWidget(QLabel("Name:", self))
        layout1.addWidget(self.targetLootProfile_lineEdit)
        layout2.addWidget(save_target_loot_button)
        layout2.addWidget(load_target_loot_button)

        # Add layouts to groupbox
        groupbox_layout.addWidget(self.targetLootProfile_listWidget)
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 2, 0)

    def set_target(self) -> None:
        groupbox = QGroupBox("Define Target", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        add_target_button = QPushButton("Add", self)
        add_target_button.setFixedWidth(50)
        add_target_button.clicked.connect(self.add_target)

        # Combo Boxes
        self.attackDist_comboBox.addItems(["All", "1", "2", "3", "4", "5"])

        # Layouts for input fields
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add widgets to layouts
        layout1.addWidget(self.targetName_lineEdit)
        layout1.addWidget(add_target_button)
        layout2.addWidget(QLabel("Attack Distance:", self))
        layout2.addWidget(self.attackDist_comboBox)

        # Add layouts to groupbox
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 1, 1, 1)

    def target_loot(self) -> None:
        groupbox = QGroupBox("Start", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Connect checkbox state changes to function
        self.startTarget_checkBox.stateChanged.connect(self.start_target_loot)

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add widgets to layouts
        layout1.addWidget(self.startLoot_checkBox)
        layout1.addWidget(self.chase_checkBox)
        layout2.addWidget(self.startTarget_checkBox)

        # Add layouts to groupbox
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 1, 1, 1, 1)

    def loot_list(self) -> None:
        groupbox = QGroupBox("Loot List", self)
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        add_item_button = QPushButton("Add", self)
        delete_item_button = QPushButton("Del", self)
        add_item_button.setFixedWidth(40)
        delete_item_button.setFixedWidth(40)

        # Button functions
        add_item_button.clicked.connect(self.add_item)
        delete_item_button.clicked.connect(self.delete_item)

        # Layout for input fields
        layout1 = QHBoxLayout(self)
        layout1.addWidget(self.itemName_lineEdit)
        layout1.addWidget(self.lootOption_lineEdit)
        layout1.addWidget(add_item_button)
        layout1.addWidget(delete_item_button)

        # Add to groupbox
        groupbox_layout.addWidget(self.lootList_listWidget)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 2, 1)

    def add_item(self) -> None:
        item_name = self.itemName_lineEdit.text()
        loot_container = self.lootOption_lineEdit.text()
        if item_name and loot_container:
            for index in range(self.lootList_listWidget.count()):
                if item_name.upper() == self.lootList_listWidget.item(index).text().upper():
                    return
            item_data = {"Loot": int(loot_container)}
            item = QListWidgetItem(item_name)
            item.setData(Qt.UserRole, item_data)
            self.itemName_lineEdit.clear()
            self.lootOption_lineEdit.clear()
            self.lootList_listWidget.addItem(item)

    def delete_item(self) -> None:
        selected_item = self.lootList_listWidget.currentItem()
        if selected_item:
            self.lootList_listWidget.takeItem(self.lootList_listWidget.row(selected_item))

    def add_target(self) -> None:
        monster_name = self.targetName_lineEdit.text()
        for index in range(self.targetList_listWidget.count()):
            if monster_name.upper() == self.targetList_listWidget.item(index).text().split(' | ')[0].upper():
                return
        monster_data = {
            "Distance": self.attackDist_comboBox.currentText(),
        }
        monster = QListWidgetItem(monster_name)
        if monster_data['Distance'] == 'All':
            monster_data['Distance'] = 0
        monster.setData(Qt.UserRole, monster_data)
        self.attackDist_comboBox.setCurrentIndex(0)
        self.targetName_lineEdit.clear()
        self.targetList_listWidget.addItem(monster)

    def delete_target(self) -> None:
        selected_monster = self.targetList_listWidget.currentItem()
        if selected_monster:
            self.targetList_listWidget.takeItem(self.targetList_listWidget.row(selected_monster))

    def clear_targets_list(self) -> None:
        self.targetList_listWidget.clear()

    def save_target_loot(self) -> None:
        target_loot_name = self.targetLootProfile_lineEdit.text()
        for index in range(self.targetLootProfile_listWidget.count()):
            if target_loot_name.upper() == self.targetLootProfile_listWidget.item(index).text().upper():
                return
        if target_loot_name and self.targetList_listWidget.count():
            target_list = [
                {"name": self.targetList_listWidget.item(i).text(),
                 "data": self.targetList_listWidget.item(i).data(Qt.UserRole)}
                for i in range(self.targetList_listWidget.count())
            ]
            with open(f"Targeting/{target_loot_name}.json", "w") as f:
                json.dump(target_list, f, indent=4)

            looting_list = [
                {"name": self.lootList_listWidget.item(i).text(),
                 "data": self.lootList_listWidget.item(i).data(Qt.UserRole)}
                for i in range(self.lootList_listWidget.count())
            ]
            with open(f"Looting/{target_loot_name}.json", "w") as f:
                json.dump(looting_list, f, indent=4)
            self.targetLootProfile_listWidget.addItem(target_loot_name)
            self.targetLootProfile_lineEdit.clear()

    def load_target_loot(self) -> None:
        target_loot_name = self.targetLootProfile_listWidget.currentItem().text()
        if target_loot_name:
            with open(f"Targeting/{target_loot_name}.json", "r") as f:
                target_list = json.load(f)
                self.targetList_listWidget.clear()
                for entry in target_list:
                    target = QListWidgetItem(entry["name"])
                    target.setData(Qt.UserRole, entry["data"])
                    self.targetList_listWidget.addItem(target)

            with open(f"Looting/{target_loot_name}.json", "r") as f:
                loot_list = json.load(f)
                self.lootList_listWidget.clear()
                for entry in loot_list:
                    item = QListWidgetItem(entry["name"])
                    item.setData(Qt.UserRole, entry["data"])
                    self.lootList_listWidget.addItem(item)

    def start_target_loot(self) -> None:
        thread = Thread(target=self.start_target_loot_thread)
        thread.daemon = True
        if self.startTarget_checkBox.checkState() == 2:
            thread.start()

    # Target monsters
    def start_target_loot_thread(self) -> None:
        """
        Thread method to automate targeting monsters and looting based on specific criteria.

        Returns:
            None
        """
        while self.startTarget_checkBox.checkState() == 2:
            open_corpse = False
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, 0xC0, 0x290001)
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, 0xC0, 0xC0290001)
            time.sleep(0.1)
            target_id = read_memory_address(Addresses.attack_address, 0, 2)
            timer = 0
            if target_id != 0:
                target_x, target_y, target_name, target_hp = read_target_info()
                time.sleep(0.1)
                if self.targetList_listWidget.findItems("*", Qt.MatchFixedString):
                    target_name = "*"
                if self.targetList_listWidget.findItems(target_name, Qt.MatchFixedString):
                    target_index = self.targetList_listWidget.findItems(target_name, Qt.MatchFixedString)[0]
                    target_data = target_index.data(Qt.UserRole)
                    while read_memory_address(Addresses.attack_address, 0, 2) != 0:
                        if timer > 15:
                            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, 0xC0, 0x290001)
                            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, 0xC0, 0xC0290001)
                            timer = 0
                            time.sleep(0.1)
                        open_corpse = True
                        target_x, target_y, target_name, target_hp = read_target_info()
                        x, y, z = read_my_wpt()
                        if self.chase_checkBox.checkState() == 2:
                            walk(0, x, y, 0, target_x, target_y, 0)
                            time.sleep(0.1)
                        if not lock.locked():
                            lock.acquire()
                        if (int(target_data['Distance']) < abs(x - target_x) or int(target_data['Distance']) < abs(y - target_y)) and lock.locked() and int(target_data['Distance']) != 0:
                            lock.release()
                            break
                        timer += 0.1
                        time.sleep(0.1)
                    if open_corpse and self.startLoot_checkBox.checkState() == 2:
                        x, y, z = read_my_wpt()
                        x = target_x - x
                        y = target_y - y
                        right_click(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75)
                        time.sleep(0.2)
                        for _ in range(2):
                            for item_index in range(self.lootList_listWidget.count()):
                                item_name = self.lootList_listWidget.item(item_index).text()
                                item_data = self.lootList_listWidget.item(item_index).data(Qt.UserRole)
                                loot_container = item_data['Loot']
                                file_name = [
                                    x for x in os.listdir('ItemImages/') if x.split('.')[0] == item_name
                                ]
                                if file_name:
                                    capture_screen = WindowCapture(
                                        screen_width[0] - screen_x[0],
                                        screen_height[0] - screen_y[0], screen_x[0], screen_y[0]
                                    )

                                    if '.png' in file_name[0]:
                                        loaded_image = cv.imread(f'ItemImages/{item_name}.png')
                                        screenshot = capture_screen.get_screenshot()
                                        result = cv.matchTemplate(screenshot, loaded_image, cv.TM_CCOEFF_NORMED)
                                        locations = list(zip(*(np.where(result >= 0.85))[::-1]))
                                        locations = merge_close_points(locations, 15)
                                        locations = sorted(locations, key=lambda point: (point[1], point[0]),
                                                           reverse=True)
                                        locations = [[int(x), int(y)] for x, y in locations]

                                        for x, y in locations:
                                            if loot_container > 0:
                                                collect_item(
                                                    x + screen_x[0], y + screen_y[0], coordinates_x[loot_container],
                                                    coordinates_y[loot_container]
                                                )
                                            elif loot_container == 0:
                                                drag_drop(
                                                    x + screen_x[0], y + screen_y[0]
                                                )
                                            elif loot_container == -1:
                                                right_click(x + screen_x[0], y + screen_y[0])
                                            elif loot_container == -2:
                                                left_click(x + screen_x[0], y + screen_y[0])
                                                left_click(x + screen_x[0], y + screen_y[0])
                                            time.sleep(0.1)

                                    else:
                                        for item_name in os.listdir(f'ItemImages/{file_name[0]}'):
                                            loaded_image = cv.imread(f'ItemImages/{file_name[0]}/{item_name}')
                                            screenshot = capture_screen.get_screenshot()
                                            result = cv.matchTemplate(screenshot, loaded_image, cv.TM_CCOEFF_NORMED)
                                            locations = list(zip(*(np.where(result >= 0.75))[::-1]))
                                            locations = merge_close_points(locations, 15)
                                            locations = sorted(locations, key=lambda point: (point[1], point[0]),
                                                               reverse=True)
                                            locations = [[int(x), int(y)] for x, y in locations]

                                            for x, y in locations:
                                                if loot_container > 0:
                                                    collect_item(
                                                        x + screen_x[0], y + screen_y[0], coordinates_x[loot_container],
                                                        coordinates_y[loot_container]
                                                    )
                                                elif loot_container == 0:
                                                    drag_drop(
                                                        x + screen_x[0], y + screen_y[0]
                                                    )

                                                elif loot_container == -1:
                                                    right_click(x + screen_x[0], y + screen_y[0])
                                                elif loot_container == -2:
                                                    left_click(x + screen_x[0], y + screen_y[0])
                                                    left_click(x + screen_x[0], y + screen_y[0])
                                                time.sleep(0.1)
                else:
                    win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, 0xC0, 0x290001)
                    win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, 0xC0, 0xC0290001)
                    time.sleep(0.1)
            if lock.locked():
                lock.release()
