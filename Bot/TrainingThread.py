import random

from PyQt5.QtCore import QThread, Qt

from Functions import read_my_stats
from KeyboardFunctions import press_hotkey


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
