import win32api
import win32gui
from PyQt5.QtCore import QThread
from win32con import VK_LBUTTON

import Addresses
from Addresses import coordinates_x, coordinates_y, screen_x, screen_y, screen_width, screen_height, battle_x, battle_y


class SettingsThread(QThread):

    def __init__(self, index, status_label):
        super().__init__()
        self.index = index
        self.status_label = status_label
        self.running = True

    def run(self):
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        while self.running:
            cur_x, cur_y = win32gui.ScreenToClient(Addresses.game, win32api.GetCursorPos())
            QThread.msleep(10)
            if self.index >= 0:
                self.status_label.setText(
                    f"Current: X={cur_x}  Y={cur_y}"
                )
                if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                    coordinates_x[self.index], coordinates_y[self.index] = cur_x, cur_y
                    self.status_label.setStyleSheet("color: green; font-weight: bold;")
                    self.status_label.setText(f"Coordinates set at X={coordinates_x[self.index]}, Y={coordinates_y[self.index]}")
                    self.running = False
                    return
            elif self.index == -1:
                self.status_label.setText(
                    f"Top-left X={cur_x}  Y={cur_y}"
                )
                if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                    screen_x[0], screen_y[0] = cur_x, cur_y
                    break
        QThread.msleep(200)
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        while self.running:
            cur_x, cur_y = win32gui.ScreenToClient(Addresses.game, win32api.GetCursorPos())
            QThread.msleep(10)
            self.status_label.setText(
                f"Bottom-right X={cur_x}  Y={cur_y}"
            )
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                screen_width[0], screen_height[0] = cur_x, cur_y
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.status_label.setText("Screen area set successfully!")
                self.running = False
                return
