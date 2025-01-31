import random

from PyQt5.QtCore import QThread, Qt

import Addresses
from Addresses import coordinates_x, coordinates_y
from Functions import read_my_stats, read_target_info, read_my_wpt
from KeyboardFunctions import press_hotkey
from MemoryFunctions import read_memory_address, read_pointer_address
from MouseFunctions import use_on_me


def read_heal_data(heal_data):
    heal_type = heal_data['Type']
    heal_option = heal_data['Option']
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
                    heal_type, heal_option, heal_below, heal_above, heal_min_mp = read_heal_data(self.healing_list.item(index).data(Qt.UserRole))
                    heal_below = heal_below * heal_multiplayer
                    heal_above = heal_above * heal_multiplayer
                    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
                    hp_percentage = (current_hp * 100) / current_max_hp
                    mp_percentage = (current_mp * 100) / current_max_mp
                    if heal_type.startswith("HP"):
                        if heal_option == "UH":
                            if heal_below >= hp_percentage >= heal_above:
                                use_on_me(coordinates_x[5], coordinates_y[5])
                                QThread.msleep(random.randint(100, 200))
                                healed = True
                        else:
                            if heal_below >= hp_percentage >= heal_above and current_mp >= heal_min_mp:
                                press_hotkey(int(heal_option[1:]))
                                QThread.msleep(random.randint(100, 200))
                                healed = True
                    elif heal_type.startswith("MP"):
                        if heal_below >= mp_percentage >= heal_above:
                            press_hotkey(int(heal_option[1:]))
                            QThread.msleep(random.randint(100, 200))
                            healed = True
                    QThread.msleep(random.randint(100, 200))
                QThread.msleep(random.randint(100, 200))
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False


def attack_monster(attack_data) -> bool:
    monsters = 10
    x, y, z = read_my_wpt()
    target_x, target_y, target_z, target_name, target_hp = read_target_info()
    current_hp, current_max_hp, current_mp, current_max_mp = read_my_stats()
    if Addresses.client_name == "WADclient":
        #monsters = int((read_pointer_address(Addresses.monsters_on_screen, Addresses.monsters_on_screen_offset, 1) - 47)/25)
        monsters = 10
    elif Addresses.client_name == "Altaron":
        monsters = 10
    hp_percentage = (current_hp * 100) / current_max_hp
    if (attack_data['Action'] > 2
            and (int(attack_data['HpFrom']) >= target_hp > int(attack_data['HpTo']))
            and current_mp >= int(attack_data['MinMp'])
            and (attack_data['Name'] == '*' or target_name in attack_data['Name'])
            and (attack_data['Distance'] >= abs(x - target_x)
            and attack_data['Distance'] >= abs(y - target_y))
            and attack_data['MinHp'] <= hp_percentage
            and attack_data['Count'] <= monsters):
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
                    if read_memory_address(Addresses.attack_address, 0, 2) != 0:
                        if attack_monster(attack_data):
                            press_hotkey(int(attack_data['Action'] - 2))
                            QThread.msleep(random.randint(150, 250))
                            break
                QThread.msleep(random.randint(100, 200))
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False
