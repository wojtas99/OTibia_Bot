import random
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QListWidgetItem

import Addresses
from Addresses import walker_Lock, coordinates_x, coordinates_y
from Functions.MemoryFunctions import *
from Functions.KeyboardFunctions import walk
from Functions.MouseFunctions import mouse_function


class WalkerThread(QThread):
    index_update = pyqtSignal(int, object)

    def __init__(self, waypoints):
        super().__init__()
        self.waypoints = waypoints
        self.running = True

    def run(self):
        current_wpt = 0
        timer, timer2 = 0, 0
        old_x, old_y = 0, 0
        while self.running:
            try:
                if timer2 >= 1:
                    current_wpt = self.find_wpt(current_wpt)
                    timer2 = 0
                self.index_update.emit(0, current_wpt)
                wpt_data = self.waypoints[current_wpt]
                wpt_action = wpt_data['Action']
                wpt_direction = wpt_data['Direction']
                map_x = wpt_data['X']
                map_y = wpt_data['Y']
                map_z = wpt_data['Z']
                x, y, z = read_my_wpt()
                while (x or y or z) is None:
                    x, y, z = read_my_wpt()
                if x == map_x and y == map_y and z == map_z and wpt_action == 0:
                    timer = 0
                    current_wpt = (current_wpt + 1) % len(self.waypoints)
                    continue
                if not walker_Lock.locked() or wpt_direction == 9:
                    if old_x == x and old_y == y:
                        timer2 += 0.2
                    else:
                        timer2 = 0
                    old_x, old_y = x, y
                    if wpt_action == 0:
                        walk(wpt_direction, x, y, z, map_x, map_y, map_z)
                    elif wpt_action == 1:
                        # Rope
                        sleep_value = random.randint(500, 600)
                        QThread.msleep(sleep_value)
                        timer += sleep_value
                        mouse_function(coordinates_x[10], coordinates_y[10], option=1)
                        QThread.msleep(random.randint(100, 200))
                        x, y, z = read_my_wpt()
                        map_x = wpt_data['X']
                        map_y = wpt_data['Y']
                        mouse_function(coordinates_x[0] + (map_x - x) * Addresses.square_size, coordinates_y[0] + (map_y - y) * Addresses.square_size, option=2)
                        current_wpt = (current_wpt + 1) % len(self.waypoints)
                    elif wpt_action == 2:
                        # Shovel
                        sleep_value = random.randint(500, 600)
                        QThread.msleep(sleep_value)
                        timer += sleep_value
                        mouse_function(coordinates_x[9], coordinates_y[9], option=1)
                        QThread.msleep(random.randint(100, 200))
                        x, y, z = read_my_wpt()
                        map_x = wpt_data['X']
                        map_y = wpt_data['Y']
                        mouse_function(coordinates_x[0] + (map_x - x) * Addresses.square_size,
                            coordinates_y[0] + (map_y - y) * Addresses.square_size,
                                       option=2)
                        current_wpt = (current_wpt + 1) % len(self.waypoints)
                    elif wpt_action == 3:
                        # Ladder
                        sleep_value = random.randint(500, 600)
                        QThread.msleep(sleep_value)
                        timer += sleep_value
                        mouse_function(coordinates_x[0], coordinates_y[0], option=1)
                        current_wpt = (current_wpt + 1) % len(self.waypoints)

                if timer > 5000:
                    current_wpt = self.lost_wpt(current_wpt)
                    timer = 0
                sleep_value = random.randint(50, 100)
                QThread.msleep(sleep_value)
                if not walker_Lock.locked():
                    timer += sleep_value
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False

    def find_wpt(self, index):
        current_wpt = index
        x, y, z = read_my_wpt()
        while (x or y or z) is None:
            x, y, z = read_my_wpt()
        for wpt in range(current_wpt, len(self.waypoints)):
            wpt_data = self.waypoints[wpt]
            map_x = wpt_data['X']
            map_y = wpt_data['Y']
            map_z = wpt_data['Z']
            wpt_action = wpt_data['Action']
            wpt_direction = wpt_data['Direction']
            if (z == map_z and abs(map_x - x) <= 7 and abs(map_y - y) <= 5 and wpt_action == 0 and (wpt_direction == 0 or wpt_direction == 9)
                    and 0 > index - wpt >= -5):
                current_wpt = wpt
                if wpt_direction == 0:
                    return current_wpt
        return current_wpt

    def lost_wpt(self, index):
        current_wpt = 0
        x, y, z = read_my_wpt()
        while (x or y or z) is None:
            x, y, z = read_my_wpt()
        for wpt in range(0, len(self.waypoints)):
            wpt_data = self.waypoints[wpt]
            map_x = wpt_data['X']
            map_y = wpt_data['Y']
            map_z = wpt_data['Z']
            wpt_action = wpt_data['Action']
            wpt_direction = wpt_data['Direction']
            if z == map_z and abs(map_x - x) <= 7 and abs(map_y - y) <= 5 and wpt_action == 0 and (wpt_direction == 0 or wpt_direction == 9):
                current_wpt = wpt
        return current_wpt


class RecordThread(QThread):
    wpt_update = pyqtSignal(int, object)

    def __init__(self, comboBox):
        super().__init__()
        self.running = True
        self.comboBox = comboBox

    def run(self):
        x, y, z = read_my_wpt()
        waypoint_data = {
            "Action": 0,
            "Direction": int(self.comboBox.currentIndex()),
            "X": x,
            "Y": y,
            "Z": z
        }
        waypoint = QListWidgetItem(f'Stand: {x} {y} {z} {self.comboBox.currentText()}')
        waypoint.setData(Qt.UserRole, waypoint_data)
        self.wpt_update.emit(1, waypoint)
        old_x, old_y, old_z = x, y, z
        while self.running:
            try:
                x, y, z = read_my_wpt()
                if z != old_z:  # Stair, hole, etc.
                    if y > old_y and x == old_x:  # Move South
                        waypoint_data = {
                            "Action": 0,
                            "Direction": 2,  # South index
                            "X": x,
                            "Y": y,
                            "Z": z
                        }
                        waypoint = QListWidgetItem(f'Stand: {x} {y} {z} South')
                        waypoint.setData(Qt.UserRole, waypoint_data)
                        self.wpt_update.emit(1, waypoint)
                    if y < old_y and x == old_x:  # Move North
                        waypoint_data = {
                            "Action": 0,
                            "Direction": 1,  # North index
                            "X": x,
                            "Y": y,
                            "Z": z
                        }
                        waypoint = QListWidgetItem(f'Stand: {x} {y} {z} North')
                        waypoint.setData(Qt.UserRole, waypoint_data)
                        self.wpt_update.emit(1, waypoint)
                    if y == old_y and x > old_x:  # Move East
                        waypoint_data = {
                            "Action": 0,
                            "Direction": 3,  # East index
                            "X": x,
                            "Y": y,
                            "Z": z
                        }
                        waypoint = QListWidgetItem(f'Stand: {x} {y} {z} East')
                        waypoint.setData(Qt.UserRole, waypoint_data)
                        self.wpt_update.emit(1, waypoint)


                    if y == old_y and x < old_x:  # Move West
                        waypoint_data = {
                            "Action": 0,
                            "Direction": 4,  # West index
                            "X": x,
                            "Y": y,
                            "Z": z
                        }
                        waypoint = QListWidgetItem(f'Stand: {x} {y} {z} West')
                        waypoint.setData(Qt.UserRole, waypoint_data)
                        self.wpt_update.emit(1, waypoint)

                if (x != old_x or y != old_y) and z == old_z:
                    waypoint_data = {
                        "Action": 0,
                        "Direction": int(self.comboBox.currentIndex()),
                        "X": x,
                        "Y": y,
                        "Z": z
                    }
                    waypoint = QListWidgetItem(f'Stand: {x} {y} {z} {self.comboBox.currentText()}')
                    waypoint.setData(Qt.UserRole, waypoint_data)
                    self.wpt_update.emit(1, waypoint)
                old_x, old_y, old_z = x, y, z
                QThread.msleep(100)
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False
