import random

import numpy as np
from PyQt5.QtCore import QThread, QMutex, QMutexLocker
from pytesseract import Output

import Addresses
from Addresses import coordinates_x, coordinates_y, screen_width, screen_height, screen_x, screen_y, walker_Lock, battle_x, battle_y
from Functions.GeneralFunctions import load_items_images
from Functions.MemoryFunctions import *
from Functions.GeneralFunctions import WindowCapture, merge_close_points
from Functions.KeyboardFunctions import press_hotkey, chase_monster, stay_diagonal, chaseDiagonal_monster
from Functions.MouseFunctions import manage_collect, mouse_function
import cv2 as cv
import pytesseract



lootLoop = 4

TITLE_BAR_OFFSET = 35
SCALE_FACTOR = 7.0

def ocr_attackMonster(targets):
    capture_screen = WindowCapture(screen_width[1] - battle_x[0], screen_height[1] - battle_y[0],
                                   battle_x[0] + 10, battle_y[0] + TITLE_BAR_OFFSET)

    screenshot = capture_screen.get_screenshot()
    screenshot = cv.resize(screenshot, None, fx=SCALE_FACTOR, fy=SCALE_FACTOR, interpolation=cv.INTER_CUBIC)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)



    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)


    target_names = [t['Name'].lower() for t in targets]
    n_boxes = len(data['level'])

    combined_words = {}

    for i in range(n_boxes):
        text = data['text'][i].strip()

        if data['conf'][i] > 60 and text:
            block_num = data['block_num'][i]
            line_num = data['line_num'][i]

            key = (block_num, line_num)

            if key not in combined_words:
                combined_words[key] = {
                    'text': [],
                    'x1': data['left'][i],
                    'y1': data['top'][i],
                    'x2': data['left'][i] + data['width'][i],
                    'y2': data['top'][i] + data['height'][i],
                    'conf_sum': int(data['conf'][i]),
                    'count': 1
                }
            else:
                combined_words[key]['x2'] = max(combined_words[key]['x2'], data['left'][i] + data['width'][i])
                combined_words[key]['y2'] = max(combined_words[key]['y2'], data['top'][i] + data['height'][i])
                combined_words[key]['conf_sum'] += int(data['conf'][i])
                combined_words[key]['count'] += 1

            combined_words[key]['text'].append(text)

    print(combined_words)
    for key, item in combined_words.items():
        full_word = ' '.join(item['text']).lower().strip()
        avg_confidence = item['conf_sum'] / item['count']

        if full_word in target_names:
            print(f"Found target: '{full_word}' with {avg_confidence:.2f}% avg confidence.")

            x_scaled = (item['x1'] + item['x2']) // 2
            y_scaled = (item['y1'] + item['y2']) // 2

            click_x_relative = x_scaled // int(SCALE_FACTOR)
            click_y_relative = y_scaled // int(SCALE_FACTOR)

            click_x_absolute = click_x_relative + battle_x[0]
            click_y_absolute = click_y_relative + battle_y[0]

            print("Click coords ", click_x_absolute, click_y_absolute)

            mouse_function(click_x_absolute, click_y_absolute, option=2)
            return




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
                    if walker_Lock.locked() and lootLoop > 1:
                        walker_Lock.release()
                    if self.attack_key < 10: # Hotkey
                        press_hotkey(self.attack_key)
                    else: # OCR
                        ocr_attackMonster(self.targets)
                    QThread.msleep(random.randint(100, 150))
                else:
                    target_x, target_y, target_z, target_name, target_hp = read_target_info()
                    if any(target['Name'] == target_name or target['Name'] == '*' for target in self.targets):
                        if any(target['Name'] == target_name for target in self.targets):
                            target_index = next(i for i, target in enumerate(self.targets) if target['Name'] == target_name)
                        else:
                            target_index = 0
                        target_data = self.targets[target_index]
                        while read_targeting_status() != 0:
                            if timer / 1000 > 25:
                                if self.attack_key < 10:  # Hotkey
                                    press_hotkey(self.attack_key)
                                else:  # OCR
                                    ocr_attackMonster(self.targets)
                                timer = 0
                                QThread.msleep(random.randint(100, 150))
                            target_x, target_y, target_z, target_name, target_hp = read_target_info()
                            x, y, z = read_my_wpt()
                            if target_data['Dist'] != 0:
                                dist_x = abs(x - target_x)
                                dist_y = abs(y - target_y)
                            else:
                                dist_x = 0
                                dist_y = 0
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
                                if self.attack_key < 10:  # Hotkey
                                    press_hotkey(self.attack_key)
                                else:  # OCR
                                    ocr_attackMonster(self.targets)
                                QThread.msleep(random.randint(100, 150))
                                if walker_Lock.locked() and lootLoop > 1:
                                    walker_Lock.release()
                            sleep_value = random.randint(90, 150)
                            QThread.msleep(sleep_value)
                            timer += sleep_value
                        if self.loot_state and open_corpse:
                            x, y, z = read_my_wpt()
                            x = target_x - x
                            y = target_y - y
                            mouse_function(coordinates_x[0] + x * Addresses.square_size, coordinates_y[0] + y * Addresses.square_size, option=1)
                            QThread.msleep(random.randint(300, 500))
                            lootLoop = 0
                    else:
                        if self.attack_key < 10:  # Hotkey
                            press_hotkey(self.attack_key)
                        else:  # OCR
                            ocr_attackMonster(self.targets)
                        QThread.msleep(random.randint(100, 150))
            except Exception as e:
                ...

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
        load_items_images(self.loot_list)
        item_image = Addresses.item_list
        capture_screen = WindowCapture(screen_width[0] - screen_x[0], screen_height[0] - screen_y[0],
                                       screen_x[0], screen_y[0])

        while self.running:
            try:
                while (lootLoop < 2 or not self.target_state) and self.running:
                    my_loot = lootLoop
                    for file_name, value_list in item_image.items():
                        for val in value_list[:-1]:
                            if self.target_state:
                                if my_loot != lootLoop:
                                    break
                            screenshot = capture_screen.get_screenshot()
                            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
                            screenshot = cv.GaussianBlur(screenshot, (7, 7), 0)
                            screenshot = cv.resize(screenshot, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)
                            result = cv.matchTemplate(screenshot, val, cv.TM_CCOEFF_NORMED)
                            locations = list(zip(*(np.where(result >= Addresses.collect_threshold))[::-1]))
                            if locations:
                                locations = merge_close_points(locations, 35)
                                locations = sorted(locations, key=lambda point: (point[1], point[0]), reverse=True)
                                locations = [[int(lx / zoom_img), int(ly / zoom_img)] for lx, ly in locations]
                            for lx, ly in locations:
                                manage_collect(lx, ly, value_list[-1])
                                QThread.msleep(random.randint(400, 650))
                                continue
                    lootLoop += 1
            except Exception as e:
                print(e)

    def update_states(self, state):
        """Thread-safe method to update loot and skin states."""
        with QMutexLocker(self.state_lock):
            self.target_state = state

    def stop(self):
        self.running = False
