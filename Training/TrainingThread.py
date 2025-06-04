import random

import win32gui
from PyQt5.QtCore import QThread, Qt
from win32con import VK_LBUTTON

from Addresses import fishing_x, fishing_y
from Functions.MemoryFunctions import *
from Functions.KeyboardFunctions import press_hotkey
from Functions.MouseFunctions import mouse_function


class TrainingThread(QThread):

    def __init__(self, training_list):
        super().__init__()
        self.training_list = training_list
        self.running = True

    def run(self):
        while self.running:
            try:
                for index in range(self.training_list.count()):
                    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                    while (current_hp or current_max_hp or current_mp or current_max_mp) is None:
                        current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                    hotkey_data = self.training_list.item(index).data(Qt.UserRole)
                    hotkey_mana = hotkey_data['Mana']
                    if current_mp >= hotkey_mana:
                        press_hotkey(int(self.training_list.item(index).text()[1:]))
                        QThread.msleep(random.randint(500, 600))
                QThread.msleep(random.randint(500, 600))
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False


class ClickThread(QThread):
    def __init__(self, timer, hotkey):
        super().__init__()
        self.timer = timer
        self.hotkey = hotkey
        self.running = True

    def run(self):
        timer = 0
        while self.running:
            try:
                if timer/1000 >= self.timer:
                    press_hotkey(int(self.hotkey[1:]))
                    timer = 0
                sleep_value = random.randint(500, 600)
                QThread.msleep(sleep_value)
                timer += sleep_value

            except Exception as e:
                print(e)

    def stop(self):
        self.running = False


class FishingThread(QThread):
    def __init__(self, status_label):
        super().__init__()
        self.status_label = status_label
        self.running = True

    def run(self):
        timer = 0
        counter = 0
        baits = 0
        if fishing_x[2] != 0:
            QThread.msleep(random.randint(1000, 1100))
            mouse_function(fishing_x[2], fishing_y[2], option=1)
            QThread.msleep(random.randint(1000, 1100))
            mouse_function(fishing_x[1], fishing_y[1], option=2)
            QThread.msleep(random.randint(1000, 1100))
            baits += 1
        while self.running:
            mouse_function(fishing_x[0], fishing_y[0], option=1)
            mouse_function(fishing_x[1], fishing_y[1], option=2)
            counter += 1
            randomizer = random.randint(1000, 1100)
            timer += randomizer
            QThread.msleep(randomizer)
            self.status_label.setText(f"Clicked {counter} times | used {baits} baits")
            if counter % 1015 == 0 and fishing_x[2] != 0:
                QThread.msleep(random.randint(1000, 1100))
                mouse_function(fishing_x[2], fishing_y[2], option=1)
                QThread.msleep(random.randint(1000, 1100))
                mouse_function(fishing_x[1], fishing_y[1], option=2)
                QThread.msleep(random.randint(1000, 1100))
                baits += 1
            if int(timer/1000) >= 20 and fishing_x[3] != 0:
                for _ in range(3):
                    mouse_function(fishing_x[3], fishing_y[3], option=1)
                    QThread.msleep(random.randint(300, 500))
                timer = 0



        return
    def stop(self):
        self.running = False


class SetThread(QThread):

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
            self.status_label.setText(f"Current: X={cur_x}  Y={cur_y}")
            if win32api.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                fishing_x[self.index], fishing_y[self.index] = cur_x, cur_y
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.status_label.setText(f"Coordinates set at X={fishing_x[self.index]}, Y={fishing_y[self.index]}")
                self.running = False
                return
