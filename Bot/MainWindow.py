import Addresses
import win32gui
import base64
from Addresses import icon_image
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication)
from PyQt5.QtGui import QIcon, QPixmap
from HealingAttack import HealingTab
from Training import TrainingTab
from Walker import WalkerTab
from TargetLoot import TargetLootTab
from Settings import SettingsTab
from SmartHotkeys import SmartHotkeysTab


class MainWindowTab(QWidget):
    def __init__(self):
        super().__init__()

        # Handle closing
        QApplication.instance().aboutToQuit.connect(lambda: win32gui.SetWindowText(Addresses.game, Addresses.game_name))

        # Load Icon
        win32gui.SetWindowText(Addresses.game, Addresses.game_name + " - EasyBot" + Addresses.numberEasyBot)
        self.setWindowIcon(QIcon(pixmap) if (pixmap := QPixmap()).loadFromData(base64.b64decode(icon_image)) else QIcon())
        # Set Title and Size
        self.setFixedSize(400, 100)
        self.setWindowTitle("EasyBot - " + Addresses.numberEasyBot)

        # Instances
        self.targetLootTab_instance = None
        self.walkerTab_instance = None
        self.healingTab_instance = None
        self.settingsTab_instance = None
        self.trainingTab_instance = None
        self.smartHotkeysTab_instance = None

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Buttons
        self.targetLootTab_button = QPushButton('Targeting', self)
        self.walkerTab_button = QPushButton('Walker', self)
        self.healingTab_button = QPushButton('Spells && Healing', self)
        self.settingsTab_button = QPushButton('Settings', self)
        self.smartHotkeysTab_button = QPushButton('Smart Hotkeys', self)
        self.trainingTab_button = QPushButton('Skill && Tools', self)

        # Buttons Functions
        self.targetLootTab_button.clicked.connect(self.targetLoot)
        self.walkerTab_button.clicked.connect(self.walker)
        self.healingTab_button.clicked.connect(self.healing)
        self.settingsTab_button.clicked.connect(self.settings)
        self.smartHotkeysTab_button.clicked.connect(self.smartHotkeys)
        self.trainingTab_button.clicked.connect(self.training)

        # Add Widgets
        self.layout.addWidget(self.walkerTab_button, 0, 0)
        self.layout.addWidget(self.targetLootTab_button, 1, 0)
        self.layout.addWidget(self.healingTab_button, 0, 1)
        self.layout.addWidget(self.settingsTab_button, 1, 1)
        self.layout.addWidget(self.smartHotkeysTab_button, 0, 2)
        self.layout.addWidget(self.trainingTab_button, 1, 2)

    def smartHotkeys(self):
        if self.smartHotkeysTab_instance is None:
            self.smartHotkeysTab_instance = SmartHotkeysTab()
        self.smartHotkeysTab_instance.show()

    def training(self):
        if self.trainingTab_instance is None:
            self.trainingTab_instance = TrainingTab()
        self.trainingTab_instance.show()

    def settings(self):
        if self.settingsTab_instance is None:
            self.settingsTab_instance = SettingsTab()
        self.settingsTab_instance.show()

    def walker(self):
        if self.walkerTab_instance is None:
            self.walkerTab_instance = WalkerTab()
        self.walkerTab_instance.show()

    def targetLoot(self):
        if self.targetLootTab_instance is None:
            self.targetLootTab_instance = TargetLootTab()
        self.targetLootTab_instance.show()

    def healing(self):
        if self.healingTab_instance is None:
            self.healingTab_instance = HealingTab()
        self.healingTab_instance.show()
        