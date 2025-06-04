from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QComboBox, QLineEdit, QListWidget, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidgetItem, QLabel
)
from PyQt5.QtGui import QIcon
from Training.TrainingThread import TrainingThread, ClickThread, SetThread, FishingThread


class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()

        # Thread Variables
        self.click_thread = None
        self.training_thread = None
        self.set_thread = None
        self.fishing_thread = None

        # Load Icon
        self.setWindowIcon(QIcon('Images/Icon.jpg'))

        # Set Title and Size
        self.setWindowTitle("Training")
        self.setFixedSize(300, 400)

        # --- Status label at the bottom (for messages, instructions, and showing coordinates)
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        # Check Boxes
        self.burn_mana_checkbox = QCheckBox("Burn Mana", self)
        self.start_click_checkbox = QCheckBox("Start", self)
        self.start_fishing_checkbox = QCheckBox("Start", self)

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

        # Finally, add the status label in row=2 (bottom)
        self.layout.addWidget(self.status_label, 3, 0, 1, 2)

        # Initialize
        self.burn_mana_list()
        self.add_hotkeys()
        self.click_key()
        self.fishing()


    def fishing(self) -> None:
        groupbox = QGroupBox("Fishing")
        groupbox_layout = QVBoxLayout(self)
        groupbox.setLayout(groupbox_layout)

        fishing_button = QPushButton("Fishing Rod", self)
        water_button = QPushButton("Water", self)
        bait_button = QPushButton("Bait", self)
        food_button = QPushButton("Food", self)

        self.start_fishing_checkbox.stateChanged.connect(self.start_fishing_thread)

        fishing_button.clicked.connect(lambda: self.startSet_thread(0))
        water_button.clicked.connect(lambda: self.startSet_thread(1))
        bait_button.clicked.connect(lambda: self.startSet_thread(2))
        food_button.clicked.connect(lambda: self.startSet_thread(3))

        # Layouts
        layout1 = QHBoxLayout(self)

        layout1.addWidget(fishing_button)
        layout1.addWidget(water_button)
        layout1.addWidget(bait_button)
        layout1.addWidget(food_button)
        layout1.addWidget(self.start_fishing_checkbox)
        groupbox_layout.addLayout(layout1)
        self.layout.addWidget(groupbox, 2, 0, 1, 2)


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

    def start_fishing_thread(self, state) -> None:
        if state == Qt.Checked:
            if not self.fishing_thread:
                self.fishing_thread = FishingThread(self.status_label)
                self.fishing_thread.start()
        else:
            if self.fishing_thread:
                self.fishing_thread.stop()
                self.fishing_thread = None


    def startSet_thread(self, index) -> None:
        self.set_thread = SetThread(index, self.status_label)
        self.set_thread.start()
