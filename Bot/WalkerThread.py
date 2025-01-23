import random
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QListWidgetItem

from Addresses import walker_Lock, coordinates_x, coordinates_y
from Functions import read_my_wpt
from KeyboardFunctions import walk
from MouseFunctions import left_click, right_click


class WalkerThread(QThread):
    index_update = pyqtSignal(int, object)

    def __init__(self, waypoints):
        super().__init__()
        self.waypoints = waypoints
        self.running = True

    def run(self):
        current_wpt = 0
        timer = 0
        while self.running:
            try:
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
                if not walker_Lock.locked():
                    if wpt_action == 0:
                        walk(wpt_direction, x, y, z, map_x, map_y, map_z)
                    elif wpt_action == 1:
                        # Rope
                        sleep_value = random.randint(500, 600)
                        QThread.msleep(sleep_value)
                        timer += sleep_value
                        right_click(coordinates_x[10], coordinates_y[10])
                        QThread.msleep(random.randint(100, 200))
                        left_click(coordinates_x[0], coordinates_y[0])
                        x, y, z = read_my_wpt()
                        map_x = wpt_data['X']
                        map_y = wpt_data['Y']
                        left_click(coordinates_x[0] + (map_x - x) * 75, coordinates_y[0] + (map_y - y) * 75)
                        current_wpt = (current_wpt + 1) % len(self.waypoints)
                    elif wpt_action == 2:
                        # Shovel
                        sleep_value = random.randint(500, 600)
                        QThread.msleep(sleep_value)
                        timer += sleep_value
                        right_click(coordinates_x[9], coordinates_y[9])
                        QThread.msleep(random.randint(100, 200))
                        x, y, z = read_my_wpt()
                        map_x = wpt_data['X']
                        map_y = wpt_data['Y']
                        left_click(
                            coordinates_x[0] + (map_x - x) * 75,
                            coordinates_y[0] + (map_y - y) * 75
                        )
                        current_wpt = (current_wpt + 1) % len(self.waypoints)
                    elif wpt_action == 3:
                        # Ladder
                        sleep_value = random.randint(500, 600)
                        QThread.msleep(sleep_value)
                        timer += sleep_value
                        right_click(coordinates_x[0], coordinates_y[0])  # e.g. click on Ladder
                        current_wpt = (current_wpt + 1) % len(self.waypoints)

                if timer > 5000:
                    current_wpt = self.lost_wpt()
                    timer = 0
                sleep_value = random.randint(20, 30)
                QThread.msleep(sleep_value)
                if not walker_Lock.locked():
                    timer += sleep_value
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False

    def lost_wpt(self):
        current_wpt = 0
        x, y, z = read_my_wpt()
        while (x or y or z) is None:
            x, y, z = read_my_wpt()
        for wpt in range(0, len(self.waypoints)):
            wpt_data = self.waypoints[wpt]
            map_x = wpt_data['X']
            map_y = wpt_data['Y']
            map_z = wpt_data['Z']
            if z == map_z and abs(map_x - x) <= 7 and abs(map_y - y) <= 5:
                current_wpt = wpt
                left_click(coordinates_x[0] + (map_x - x) * 75, coordinates_y[0] + (map_y - y) * 75)
                QThread.msleep(random.randint(1000, 2000))
                break
        return current_wpt


class RecordThread(QThread):
    wpt_update = pyqtSignal(int, object)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        x, y, z = read_my_wpt()
        waypoint_data = {
            "Action": 0,
            "Direction": 0,
            "X": x,
            "Y": y,
            "Z": z
        }
        waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')
        waypoint.setData(Qt.UserRole, waypoint_data)
        self.wpt_update.emit(1, waypoint)
        old_x, old_y, old_z = x, y, z
        while self.running:
            try:
                x, y, z = read_my_wpt()
                if (x != old_x or y != old_y) and z == old_z:
                    waypoint_data = {
                        "Action": 0,
                        "Direction": 0,
                        "X": x,
                        "Y": y,
                        "Z": z
                    }
                    waypoint = QListWidgetItem(f'Stand: {x} {y} {z}')
                    waypoint.setData(Qt.UserRole, waypoint_data)
                    self.wpt_update.emit(1, waypoint)
                old_x, old_y, old_z = x, y, z
                QThread.msleep(100)
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False
