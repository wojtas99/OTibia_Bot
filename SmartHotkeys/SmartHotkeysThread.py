import random
import win32api
import win32con
import win32gui
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QListWidgetItem

from Addresses import coordinates_x, coordinates_y
import Addresses
from Functions.MemoryFunctions import read_target_info, read_my_wpt, read_targeting_status
from Functions.MouseFunctions import mouse_function


class SetSmartHotkeyThread(QThread):
    def __init__(self, hotkeys_listWidget, hotkey_option_combobox, rune_option_combobox, status_label):
        super().__init__()
        self.running = True
        self.hotkeys_listWidget = hotkeys_listWidget
        self.status_label = status_label
        self.hotkey_option_combobox = hotkey_option_combobox
        self.rune_option_combobox = rune_option_combobox

    def run(self):
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        while self.running:
            x, y = win32gui.ScreenToClient(Addresses.game, win32api.GetCursorPos())
            self.status_label.setText(
                f"Current: X={x}  Y={y}"
            )
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.status_label.setText(f"Coordinates set at X={x}, Y={y}")
                self.running = False
                smart_hotkey_data = {
                    "Hotkey": self.hotkey_option_combobox.currentText(),
                    "Option": self.rune_option_combobox.currentText(),
                    "X": x,
                    "Y": y
                }
                hotkey_item = QListWidgetItem(smart_hotkey_data["Hotkey"])
                hotkey_item.setData(Qt.UserRole, smart_hotkey_data)
                self.hotkeys_listWidget.addItem(hotkey_item)
                return


class SmartHotkeysThread(QThread):
    def __init__(self, hotkeys_listWidget):
        super().__init__()
        self.running = True
        self.hotkeys_listWidget = hotkeys_listWidget

    def run(self):
        while self.running:
            for index in range(self.hotkeys_listWidget.count()):
                hotkey_data = self.hotkeys_listWidget.item(index).data(Qt.UserRole)
                hotkey_number = int(hotkey_data['Hotkey'][1:])
                vk_code = 111 + hotkey_number
                if win32api.GetAsyncKeyState(vk_code) & 1:
                    mouse_function(hotkey_data['X'], hotkey_data['Y'], option=1)
                    if hotkey_data['Option'] == 'On Target':
                        target_id = read_targeting_status()
                        if target_id:
                            target_x, target_y, target_z, target_name, target_hp = read_target_info()
                            x, y, z = read_my_wpt()
                            dx = (target_x - x) * Addresses.square_size
                            dy = (target_y - y) * Addresses.square_size
                            mouse_function(coordinates_x[0] + dx, coordinates_y[0] + dy, option=2)
                    elif hotkey_data['Option'] == 'On Yourself':
                        mouse_function(coordinates_x[0], coordinates_y[0], option=2)
                    elif hotkey_data['Option'] == 'With Crosshair':
                        cur_x, cur_y = win32gui.ScreenToClient(Addresses.game, win32api.GetCursorPos())
                        mouse_function(cur_x, cur_y, option=2)
            QThread.msleep(int(random.uniform(10, 20)))

    def stop(self):
        self.running = False
