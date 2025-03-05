from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QListWidget, QComboBox, QPushButton,
    QLabel, QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Functions.GeneralFunctions import delete_item
from SmartHotkeys.SmartHotkeysThread import SmartHotkeysThread, SetSmartHotkeyThread


class SmartHotkeysTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.smart_hotkeys_thread = None
        self.set_smart_hotkey_thread = None

        # Load Icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Smart Hotkeys")
        self.setFixedSize(300, 200)  # Increased to fit the status label and checkbox

        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: Red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Main layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # List Widgets
        self.smart_hotkeys_listWidget = QListWidget(self)
        self.smart_hotkeys_listWidget.setFixedHeight(60)
        self.smart_hotkeys_listWidget.itemDoubleClicked.connect(
            lambda item: delete_item(self.smart_hotkeys_listWidget, item)
        )

        # Combo Boxes
        self.rune_option_combobox = QComboBox(self)
        self.rune_option_combobox.addItems(["With Crosshair", "On Target", "On Yourself"])

        self.hotkey_option_combobox = QComboBox(self)
        for i in range(1, 13):
            self.hotkey_option_combobox.addItem(f"F{i}")

        # Buttons
        self.coordinates_button = QPushButton("Coordinates", self)

        # Checkbox: Start Smart Hotkeys
        self.start_hotkeys_checkbox = QCheckBox("Start Smart Hotkeys", self)

        # Button functions
        self.coordinates_button.clicked.connect(self.start_set_hotkey_thread)

        # Checkbox function
        self.start_hotkeys_checkbox.stateChanged.connect(self.start_smart_hotkeys_thread)

        # Add Widgets to Layout
        self.layout.addWidget(self.smart_hotkeys_listWidget, 0, 0, 1, 3)
        self.layout.addWidget(self.rune_option_combobox, 1, 0)
        self.layout.addWidget(self.hotkey_option_combobox, 1, 1)
        self.layout.addWidget(self.coordinates_button, 1, 2)

        # Place the checkbox in row 2, col 0..1
        self.layout.addWidget(self.start_hotkeys_checkbox, 2, 0, 1, 2)

        # Finally, add the status label in row 3 (spanning all columns)
        self.layout.addWidget(self.status_label, 3, 0, 1, 3)

    def start_set_hotkey_thread(self):
        self.set_smart_hotkey_thread = SetSmartHotkeyThread(self.smart_hotkeys_listWidget, self.hotkey_option_combobox,
                                                            self.rune_option_combobox, self.status_label)
        self.set_smart_hotkey_thread.start()

    def start_smart_hotkeys_thread(self, state):
        if state == Qt.Checked:
            if not self.smart_hotkeys_thread:
                self.smart_hotkeys_thread = SmartHotkeysThread(self.smart_hotkeys_listWidget)
                self.smart_hotkeys_thread.start()
        else:
            if self.smart_hotkeys_thread:
                self.smart_hotkeys_thread.stop()
                self.smart_hotkeys_thread = None
