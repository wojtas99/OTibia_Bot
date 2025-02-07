import random

import numpy as np
from PyQt5.QtCore import QThread, QMutex, QMutexLocker
from Addresses import coordinates_x, coordinates_y, screen_width, screen_height, screen_x, screen_y, walker_Lock
from Functions.GeneralFunctions import load_items_images
from Functions.MemoryFunctions import *
from Functions.GeneralFunctions import WindowCapture, merge_close_points
from Functions.KeyboardFunctions import press_hotkey, chase_monster
from Functions.MouseFunctions import right_click, left_click, manage_collect
import cv2 as cv

lootLoop = 2


class TargetThread(QThread):

    def __init__(self, targets, loot_state, skin_state, chase_state):
        super().__init__()
        self.running = True
        self.targets = targets
        self.loot_state = loot_state
        self.skin_state = skin_state
        self.chase_state = chase_state
        self.state_lock = QMutex()

    def run(self):
        global lootLoop
        sleep_value = 0
        while self.running:
            QThread.msleep(random.randint(10, 20))
            try:
                open_corpse = False
                timer = 0
                target_id = read_targeting_status()
                # Attack if no target
                if target_id == 0:
                    # Simulate pressing "~" key to switch target or approach
                    press_hotkey(10)
                    QThread.msleep(random.randint(100, 150))
                    target_id = read_targeting_status()
                if target_id != 0:
                    target_x, target_y, target_z, target_name, target_hp = read_target_info()
                    if target_hp <= 0:
                        continue
                    if any(target['Name'] == target_name for target in self.targets):
                        target_index = next(i for i, target in enumerate(self.targets) if target['Name'] == target_name)
                        target_data = self.targets[target_index]
                        while read_targeting_status() != 0:
                            if timer / 1000 > 15:
                                # Press "~" again to try re-targeting or un-stuck
                                press_hotkey(10)
                                timer = 0
                                QThread.msleep(random.randint(100, 150))
                            target_x, target_y, target_z, target_name, target_hp = read_target_info()
                            x, y, z = read_my_wpt()
                            # If within attack distance
                            if (((int(target_data['Distance']) >= abs(x - target_x)
                                 and int(target_data['Distance']) >= abs(y - target_y))
                                or target_data['Distance'] == 0)
                                    and abs(x - target_x) < 7 and abs(y - target_y) < 5):
                                if not walker_Lock.locked():
                                    walker_Lock.acquire()
                                if self.chase_state:
                                    chase_monster(x, y, target_x, target_y)
                            else:
                                if walker_Lock.locked() and lootLoop > 1:
                                    walker_Lock.release()
                                press_hotkey(10)
                                sleep_value = random.randint(90, 150)
                                QThread.msleep(sleep_value)
                                timer += sleep_value
                                target_x, target_y, target_z, target_name, target_hp = read_target_info()

                            open_corpse = True
                            sleep_value = random.randint(90, 150)
                            QThread.msleep(sleep_value)
                            timer += sleep_value
                    # If we have to skin
                    if self.skin_state and open_corpse:
                        x, y, z = read_my_wpt()
                        x = target_x - x
                        y = target_y - y
                        press_hotkey(9)  # Example: F9 as skin hotkey
                        left_click(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75)
                        QThread.msleep(random.randint(100, 200))
                    if self.loot_state and open_corpse:
                        x, y, z = read_my_wpt()
                        x = target_x - x
                        y = target_y - y
                        right_click(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75)
                        QThread.msleep(random.randint(500, 600))
                        '''
                        backpack = read_pointer_address(Addresses.backpack_address, Addresses.backpack_offset, 1)
                        for _ in range(3):
                            if backpack == read_pointer_address(Addresses.backpack_address, Addresses.backpack_offset,1):
                                right_click(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75)
                                QThread.msleep(random.randint(500, 600))
                        '''
                        x, y, z = read_my_wpt()
                        '''
                        if z != target_z:
                            walk(1, 0, 0, 0, 0, 0, 0)
                        '''
                        lootLoop = 0
                        while self.chase_state and lootLoop < 2:
                            QThread.msleep(random.randint(100, 150))

                if walker_Lock.locked() and lootLoop > 1:
                    walker_Lock.release()
            except Exception as e:
                print(f"Error: {e}")

    def update_states(self, option, state):
        """Thread-safe method to update loot and skin states."""
        with QMutexLocker(self.state_lock):
            if option == 0:
                self.loot_state = state
            elif option == 1:
                self.skin_state = state

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
                                screenshot = cv.resize(screenshot, None, fx=3, fy=3, interpolation=cv.INTER_CUBIC)
                            result = cv.matchTemplate(screenshot, val, cv.TM_CCOEFF_NORMED)
                            locations = list(zip(*(np.where(result >= 0.9))[::-1]))
                            if locations:
                                locations = merge_close_points(locations, 35)
                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                locations = [[int(lx / 3), int(ly / 3)] for lx, ly in locations]
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
