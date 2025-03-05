from Addresses import icon_image
import base64
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidgetItem, QLabel
)
from PyQt5.QtGui import QIcon, QPixmap
from Training.TrainingThread import TrainingThread, ClickThread


class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.click_thread = None
        self.training_thread = None

        # Load Icon
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())

        # Set Title and Size
        self.setWindowTitle("Training")
        self.setFixedSize(300, 200)

        # Check Boxes
        self.burn_mana_checkbox = QCheckBox("Burn Mana", self)
        self.start_click_checkbox = QCheckBox("Start", self)

        # Combo Boxes
        self.hotkey_list_combobox = QComboBox(self)
        self.key_list_combobox = QComboBox(self)
        #self.key_list_combobox.setFixedWidth(40)

        # Line Edits
        self.mp_line_edit = QLineEdit(self)
        self.timer_line_edit = QLineEdit(self)
        #self.timer_line_edit.setFixedWidth(40)

        # List Widgets
        self.burn_mana_list_widget = QListWidget(self)

        # Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize
        self.burn_mana_list()
        self.add_hotkeys()
        self.click_key()

    def click_key(self) -> None:
        groupbox = QGroupBox("Click Key")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Combo Box
        for i in range(1, 11):
            self.key_list_combobox.addItem(f"F{i}")

        # Checkbox
        self.start_click_checkbox.stateChanged.connect(self.start_click_thread)

        # Layouts
        layout1 = QHBoxLayout(self)

        layout1.addWidget(QLabel("Time: "))
        layout1.addWidget(self.timer_line_edit)
        layout1.addWidget(QLabel("Key: "))
        layout1.addWidget(self.key_list_combobox)
        layout1.addWidget(self.start_click_checkbox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 1, 0, 1, 2)

    def burn_mana_list(self) -> None:
        groupbox = QGroupBox("Burn Mana")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Add Layouts
        groupbox_layout.addWidget(self.burn_mana_list_widget)
        self.layout.addWidget(groupbox, 0, 0, 1, 1)

    def add_hotkeys(self) -> None:
        groupbox = QGroupBox("Hotkeys")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        # Buttons
        add_hotkey_button = QPushButton("Add", self)

        # Button functions
        add_hotkey_button.clicked.connect(self.add_hotkey)

        # Check Boxes
        self.burn_mana_checkbox.stateChanged.connect(self.start_training_thread)

        # Combo Boxes
        for i in range(1, 11):
            self.hotkey_list_combobox.addItem(f"F{i}")

        # Layouts
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)

        # Add Widgets
        layout1.addWidget(self.mp_line_edit)
        layout1.addWidget(self.hotkey_list_combobox)
        layout1.addWidget(add_hotkey_button)
        layout2.addWidget(self.burn_mana_checkbox)

        # Add Layouts
        groupbox_layout.addLayout(layout1)
        groupbox_layout.addLayout(layout2)
        self.layout.addWidget(groupbox, 0, 1)

    def add_hotkey(self) -> None:
        hotkey_name = self.hotkey_list_combobox.currentText()
        hotkey_data = {"Mana": int(self.mp_line_edit.text())}
        hotkey = QListWidgetItem(hotkey_name)
        hotkey.setData(Qt.UserRole, hotkey_data)
        self.burn_mana_list_widget.addItem(hotkey)
        self.mp_line_edit.clear()
        
    def start_click_thread(self, state) -> None:
        if state == Qt.Checked:
            if not self.click_thread:
                self.click_thread = ClickThread(int(self.timer_line_edit.text()), self.key_list_combobox.currentText())
                self.click_thread.start()
        else:
            if self.click_thread:
                self.click_thread.stop()
                self.click_thread = None

    def start_training_thread(self, state) -> None:
        if state == Qt.Checked:
            self.timer_line_edit.setDisabled(True)
            if not self.training_thread:
                self.training_thread = TrainingThread(self.burn_mana_list_widget)
                self.training_thread.start()
        else:
            self.timer_line_edit.setEnabled(True)
            if self.training_thread:
                self.training_thread.stop()
                self.training_thread = None

