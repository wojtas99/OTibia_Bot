import random

import numpy as np
from PyQt5.QtCore import QThread, QMutex, QMutexLocker

import Addresses
from Addresses import coordinates_x, coordinates_y, screen_width, screen_height, screen_x, screen_y, walker_Lock
from Functions.GeneralFunctions import load_items_images
from Functions.MemoryFunctions import *
from Functions.GeneralFunctions import WindowCapture, merge_close_points
from Functions.KeyboardFunctions import press_hotkey, chase_monster, stay_diagonal, chaseDiagonal_monster
from Functions.MouseFunctions import manage_collect, mouse_function
import cv2 as cv

lootLoop = 2


class TargetThread(QThread):

    def __init__(self, targets, loot_state, attack_key):
        super().__init__()
        self.running = True
        self.targets = targets
        self.attack_key = attack_key + 1
        self.loot_state = loot_state
        self.state_lock = QMutex()

    def run(self):
        global lootLoop
        while self.running:
            QThread.msleep(random.randint(10, 20))
            try:
                open_corpse = False
                timer = 0
                target_id = read_targeting_status()
                if target_id == 0:
                    if Addresses.battle_x[0] != 0:
                        mouse_function(Addresses.battle_x[0], Addresses.battle_y[0], option=2)
                        QThread.msleep(random.randint(1000, 1500))
                    else:
                        press_hotkey(self.attack_key)
                    QThread.msleep(random.randint(100, 150))
                    target_id = read_targeting_status()
                if target_id == 0:
                    if walker_Lock.locked() and lootLoop > 1:
                        walker_Lock.release()
                if target_id != 0:
                    target_x, target_y, target_z, target_name, target_hp = read_target_info()
                    if any(target['Name'] == target_name or target['Name'] == '*' for target in self.targets):
                        if any(target['Name'] == target_name for target in self.targets):
                            target_index = next(i for i, target in enumerate(self.targets) if target['Name'] == target_name)
                        else:
                            target_index = 0
                        target_data = self.targets[target_index]
                        while read_targeting_status() != 0:
                            if timer / 1000 > 25:
                                if Addresses.battle_x[0] != 0:
                                    mouse_function(Addresses.battle_x[0], Addresses.battle_y[0], option=2)
                                else:
                                    press_hotkey(self.attack_key)
                                timer = 0
                                QThread.msleep(random.randint(100, 150))
                            target_x, target_y, target_z, target_name, target_hp = read_target_info()
                            x, y, z = read_my_wpt()
                            dist_x = abs(x - target_x)
                            dist_y = abs(y - target_y)
                            if (target_data['Dist'] >= dist_x and target_data['Dist'] >= dist_y) or target_data['Dist'] == 0:
                                open_corpse = True
                                if not walker_Lock.locked():
                                    walker_Lock.acquire()
                                if target_data['Stance'] == 1:
                                    chase_monster(x, y, target_x, target_y)
                                elif target_data['Stance'] == 2:
                                    stay_diagonal(x, y, target_x, target_y)
                                elif target_data['Stance'] == 3:
                                    chaseDiagonal_monster(x, y, target_x, target_y)
                            else:
                                if Addresses.battle_x[0] != 0:
                                    mouse_function(Addresses.battle_x[0], Addresses.battle_y[0], option=2)
                                else:
                                    press_hotkey(self.attack_key)
                                QThread.msleep(random.randint(100, 150))
                                if walker_Lock.locked() and lootLoop > 1:
                                    walker_Lock.release()
                            sleep_value = random.randint(90, 150)
                            QThread.msleep(sleep_value)
                            timer += sleep_value
                        if target_data['Skin'] != 0 and open_corpse:
                            x, y, z = read_my_wpt()
                            # Do Skining
                        if self.loot_state and open_corpse:
                            x, y, z = read_my_wpt()
                            x = target_x - x
                            y = target_y - y
                            backpack = read_pointer_address(Addresses.backpack_address, Addresses.backpack_offset, 1)
                            if backpack:
                                for _ in range(3):
                                    if backpack == read_pointer_address(Addresses.backpack_address, Addresses.backpack_offset, 1):
                                        mouse_function(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75, option=1)
                                        QThread.msleep(random.randint(500, 600))
                            else:
                                mouse_function(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75, option=1)
                                QThread.msleep(random.randint(500, 600))
                            lootLoop = 0
                    else:
                        if Addresses.battle_x[0] != 0:
                            mouse_function(Addresses.battle_x[0], Addresses.battle_y[0], option=2)
                        else:
                            press_hotkey(self.attack_key)
                        QThread.msleep(random.randint(100, 150))
            except Exception as e:
                print(f"Error: {e}")

    def update_states(self, option, state):
        with QMutexLocker(self.state_lock):
            if option == 0:
                self.loot_state = state

    def stop(self):
        self.running = False


class LootThread(QThread):

    def __init__(self, loot_list, target_state):
        super().__init__()
        self.loot_list = loot_list
        self.running = True
        self.target_state = target_state
        self.state_lock = QMutex()

    def run(self):
        global lootLoop
        zoom_img = 3
        take_screen = True
        load_items_images(self.loot_list)
        item_image = Addresses.item_list
        capture_screen = WindowCapture(screen_width[0] - screen_x[0], screen_height[0] - screen_y[0],
                                       screen_x[0], screen_y[0])

        while self.running:
            try:
                while (lootLoop < 2 or not self.target_state) and self.running:
                    if lootLoop == 0:
                        take_screen = True
                    for file_name, value_list in item_image.items():
                        for val in value_list[:-1]:
                            if take_screen or not self.target_state:
                                take_screen = False
                                screenshot = capture_screen.get_screenshot()
                                screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
                                screenshot = cv.GaussianBlur(screenshot, (7, 7), 0)
                                screenshot = cv.resize(screenshot, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)

                            result = cv.matchTemplate(screenshot, val, cv.TM_CCOEFF_NORMED)
                            locations = list(zip(*(np.where(result >= 0.93))[::-1]))
                            if locations:
                                locations = merge_close_points(locations, 35)
                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                locations = [[int(lx / zoom_img), int(ly / zoom_img)] for lx, ly in locations]
                            for lx, ly in locations:
                                manage_collect(lx, ly, value_list[-1])
                                QThread.msleep(random.randint(150, 250))
                                take_screen = True
                            QThread.msleep(5)
                        QThread.msleep(5)
                    QThread.msleep(5)
                    lootLoop += 1
                QThread.msleep(5)
            except Exception as e:
                print(e)
            QThread.msleep(5)

    def update_states(self, state):
        """Thread-safe method to update loot and skin states."""
        with QMutexLocker(self.state_lock):
            self.target_state = state

    def stop(self):
        self.running = False
