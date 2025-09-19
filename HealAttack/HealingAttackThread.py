import random
from PyQt5.QtCore import QThread, Qt

import Addresses
from Addresses import coordinates_x, coordinates_y
from Functions.KeyboardFunctions import press_hotkey
from Functions.MemoryFunctions import *
from Functions.MouseFunctions import mouse_function


def read_heal_data(heal_data):
    heal_type = heal_data['Type']
    heal_option = heal_data['Key']
    heal_below = heal_data['Below']
    heal_above = heal_data['Above']
    heal_min_mp = heal_data['MinMp']
    return heal_type, heal_option, heal_below, heal_above, heal_min_mp


class HealThread(QThread):

    def __init__(self, healing_list):
        super().__init__()
        self.healing_list = healing_list
        self.running = True

    def run(self):
        healed = True
        heal_multiplayer = 0.0
        while self.running:
            try:
                if healed:
                    heal_multiplayer = random.uniform(0.9, 1.0)
                    healed = False
                for index in range(self.healing_list.count()):
                    heal_type, heal_option, heal_below, heal_above, heal_min_mp = read_heal_data(
                        self.healing_list.item(index).data(Qt.UserRole))
                    heal_below = heal_below * heal_multiplayer
                    heal_above = heal_above * heal_multiplayer
                    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                    hp_percentage = (current_hp * 100) / current_max_hp
                    mp_percentage = (current_mp * 100) / current_max_mp
                    if heal_type.startswith("HP"):
                        if heal_option == "Health":
                            if heal_below >= hp_percentage >= heal_above:
                                mouse_function(coordinates_x[5], coordinates_y[5], Addresses.coordinates_x[0], Addresses.coordinates_y[0], option=5)
                                QThread.msleep(random.randint(10, 50))
                                healed = True
                        else:
                            if heal_below >= hp_percentage >= heal_above and current_mp >= heal_min_mp:
                                press_hotkey(int(heal_option[1:]))
                                QThread.msleep(random.randint(10, 50))
                                healed = True
                    elif heal_type.startswith("MP"):
                        if heal_below >= mp_percentage >= heal_above:
                            if heal_option == "Mana":
                                mouse_function(coordinates_x[11], coordinates_y[11], Addresses.coordinates_x[0], Addresses.coordinates_y[0], option=5)
                                QThread.msleep(random.randint(100, 500))
                                healed = True
                            else:
                                press_hotkey(int(heal_option[1:]))
                                QThread.msleep(random.randint(10, 50))
                                healed = True
                    QThread.msleep(random.randint(100, 200))
                QThread.msleep(random.randint(100, 200))
            except Exception as e:
                print("Exception: ", e)

    def stop(self):
        self.running = False


def attack_monster(attack_data) -> bool:
    target_x, target_y, target_z, target_name, target_hp = read_target_info()
    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
    if target_hp < 0 or target_hp > 100:
        target_hp = 100
    hp_percentage = (current_hp * 100) / current_max_hp
    if ((int(attack_data['HpFrom']) >= target_hp > int(attack_data['HpTo'])) or int(attack_data['HpFrom'] == 0)
            and current_mp >= int(attack_data['MinMp'])
            and (attack_data['Name'] == '*' or target_name in attack_data['Name'])
            and attack_data['MinHp'] <= hp_percentage):
        return True
    return False


class AttackThread(QThread):

    def __init__(self, attack_list):
        super().__init__()
        self.attack_list = attack_list
        self.running = True

    def run(self):
        while self.running:
            try:
                for attack_index in range(self.attack_list.count()):
                    attack_data = self.attack_list.item(attack_index).data(Qt.UserRole)
                    if read_targeting_status() != 0:
                        if attack_monster(attack_data):
                            if attack_data['Key'][0] == 'F':

                                press_hotkey(int(attack_data['Key'][1:]))
                                QThread.msleep(random.randint(150, 250))
                            else:
                                if attack_data['Key'] == 'First Rune':
                                    mouse_function(coordinates_x[6],
                                                coordinates_y[6],
                                                   option=1)
                                elif attack_data['Key'] == 'Second Rune':
                                    mouse_function(coordinates_x[8],
                                                coordinates_y[8],
                                                   option=1)
                                x, y, z = read_my_wpt()
                                target_x, target_y, target_z, target_name, target_hp = read_target_info()
                                x = target_x - x
                                y = target_y - y
                                mouse_function(coordinates_x[0] + x * Addresses.square_size, coordinates_y[0] + y * Addresses.square_size, option=2)
                                QThread.msleep(random.randint(800, 1000))
                QThread.msleep(random.randint(100, 200))
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False
