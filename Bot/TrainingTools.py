import Addresses
from Addresses import icon_image
import base64
from PyQt5.QtCore import Qt
import random
import time
from threading import Thread
import win32api
import win32con
import win32gui

from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidgetItem, QLabel
)
from PyQt5.QtGui import QIcon, QPixmap

from Functions import read_my_stats, delete_item
from MemoryFunctions import read_pointer_address
from KeyboardFunctions import press_hotkey
from MouseFunctions import right_click


class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load Icon
        self.setWindowIcon(
            QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(
                base64.b64decode(icon_image)) else QIcon()
        )

        # Set Title and Size
        self.setWindowTitle("Training & Tools")
        self.setFixedSize(300, 500)  # Increased a bit to fit the status label

        # --- Status label at the bottom
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # Check Boxes
        self.burn_mana_checkbox = QCheckBox("Burn Mana", self)

        # Combo Boxes
        self.hotkey_list_combobox = QComboBox(self)

        # Line Edits
        self.mp_line_edit = QLineEdit(self)

        # List Widgets
        self.burn_mana_list_widget = QListWidget(self)
        self.burn_mana_list_widget.itemDoubleClicked.connect(
            lambda item: delete_item(self.burn_mana_list_widget, item)
        )

        # Main Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize sections
        self.burn_mana_list()
        self.add_hotkeys()

        # Finally add the status label (let's put it in row 2, spanning 2 columns)
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

    def burn_mana_list(self) -> None:
        groupbox = QGroupBox("Burn Mana")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        groupbox_layout.addWidget(self.burn_mana_list_widget)
        self.layout.addWidget(groupbox, 0, 0, 1, 1)

    def add_hotkeys(self) -> None:
        groupbox = QGroupBox("Hotkeys")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        add_hotkey_button = QPushButton("Add", self)
        add_hotkey_button.clicked.connect(self.add_hotkey)

        # When the checkbox is toggled, start the skill thread if checked
        self.burn_mana_checkbox.stateChanged.connect(self.start_skill)

        # Populate the combo box with F1..F10
        for i in range(1, 11):
            self.hotkey_list_combobox.addItem(f"F{i}")

        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        layout1.addWidget(self.mp_line_edit)
        layout1.addWidget(self.hotkey_list_combobox)
        layout1.addWidget(add_hotkey_button)
        layout2.addWidget(self.burn_mana_checkbox)

        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 1, 1, 1)

    def add_hotkey(self) -> None:
        """
        Adds a new hotkey to the burn_mana_list_widget if the MP field is valid.
        Highlights errors in red and shows status messages inline.
        """
        # Clear previous status / styles
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.mp_line_edit.setStyleSheet("")

        mp_text = self.mp_line_edit.text().strip()
        if not mp_text:
            # If empty, highlight in red
            self.mp_line_edit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("Please enter a valid MP value.")
            return

        # Try to convert to int
        try:
            mp_val = int(mp_text)
        except ValueError:
            self.mp_line_edit.setStyleSheet("border: 2px solid red;")
            self.status_label.setText("MP value must be a number.")
            return

        hotkey_name = self.hotkey_list_combobox.currentText()
        hotkey_data = {"Mana": mp_val}

        hotkey_item = QListWidgetItem(hotkey_name)
        hotkey_item.setData(Qt.UserRole, hotkey_data)
        self.burn_mana_list_widget.addItem(hotkey_item)

        self.mp_line_edit.clear()

        # Success message
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.setText("Hotkey added successfully!")

    def start_skill(self) -> None:
        """
        Starts a separate thread for burning mana if the checkbox is checked.
        """
        thread = Thread(target=self.start_skill_thread)
        thread.daemon = True
        if self.burn_mana_checkbox.checkState() == 2:
            thread.start()


    def start_skill_thread(self) -> None:
        """
        Continuously checks the player's MP and uses hotkeys if needed.
        Also triggers eating if a certain time threshold is reached.
        """
        while self.burn_mana_checkbox.checkState():
            for index in range(self.burn_mana_list_widget.count()):
                current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                hotkey_data = self.burn_mana_list_widget.item(index).data(Qt.UserRole)
                hotkey_mana = hotkey_data['Mana']
                time.sleep(random.uniform(1, 2))
                if current_mp >= hotkey_mana:
                    # The text is like "F1", so skip 'F' => use int(...) for the number
                    press_hotkey(int(self.burn_mana_list_widget.item(index).text()[1:]))
                    time.sleep(random.uniform(1, 2))
