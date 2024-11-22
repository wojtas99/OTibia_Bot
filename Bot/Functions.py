import re

import Addresses
from MemoryFunctions import read_pointer_address, read_memory_address


def read_my_stats():
    if Addresses.client == "Altaron":
        current_hp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_hp_offset, 1)
        current_max_hp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_hp_max_offset, 1)
        current_mp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_mp_offset, 1)
        current_max_mp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_mp_max_offset, 1)
        return current_hp, current_max_hp, current_mp, current_max_mp
    elif Addresses.client == "WAT" or Addresses.client == "Medivia":
        current_hp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_hp_offset, 3)
        current_max_hp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_hp_max_offset, 3)
        current_mp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_mp_offset, 3)
        current_max_mp = read_pointer_address(Addresses.my_stats_ptr, Addresses.my_mp_max_offset, 3)
        return current_hp, current_max_hp, current_mp, current_max_mp


def read_my_wpt():
    x = read_memory_address(Addresses.my_x_address, 0, 1)
    y = read_memory_address(Addresses.my_y_address, 0, 1)
    z = read_memory_address(Addresses.my_z_address, 0, 4)
    return x, y, z


def read_target_info():
    if Addresses.client == "Altaron" or Addresses.client == "WAT":
        target_x = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_x = read_memory_address(target_x, Addresses.target_x_offset, 1)
        target_y = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_y = read_memory_address(target_y, Addresses.target_y_offset, 1)
        target_name = "*"
        target_hp = read_memory_address(read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address, Addresses.target_hp_offset, 7)
        return target_x, target_y, target_name, target_hp
    elif Addresses.client == "Medivia":
        target_base = read_memory_address(Addresses.attack_address, 0, 2)
        if target_base != 0:
            target_x = read_memory_address(target_base - Addresses.base_address, Addresses.target_x_offset, 1)
            target_y = read_memory_address(target_base - Addresses.base_address, Addresses.target_y_offset, 1)
            target_name = read_memory_address(target_base - Addresses.base_address, Addresses.target_name_offset, 9)
            target_name = b''.join(target_name).split(b'\x00', 1)[0].decode('utf-8')
            target_hp = read_memory_address(target_base - Addresses.base_address, Addresses.target_hp_offset, 7)
            return target_x, target_y, target_name, target_hp
    else:
        target_x = read_memory_address(Addresses.attack_address, 0, 2)
        target_x = read_memory_address(target_x - Addresses.base_address, Addresses.target_x_offset, 1)
        target_y = read_memory_address(Addresses.attack_address, 0, 2)
        target_y = read_memory_address(target_y - Addresses.base_address, Addresses.target_y_offset, 1)
        target_name = "*"
        target_hp = 0
        return target_x, target_y, target_name, target_hp