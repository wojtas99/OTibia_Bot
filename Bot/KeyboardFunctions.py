import random
import time

import win32api
import win32gui
import Addresses
from Addresses import rParam, lParam, coordinates_x, coordinates_y
from MouseFunctions import left_click
import win32con


def walk(wpt_direction, my_x, my_y, my_z, map_x, map_y, map_z) -> None:
    x = map_x - my_x
    y = map_y - my_y
    z = map_z - my_z
    if wpt_direction != 0:
        if wpt_direction == 1 and (-2 <= y < 0 or (y == 0 == x)) and abs(z) <= 1:  # Walk North
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])
            return
        if wpt_direction == 2 and 0 < y <= 2 and abs(z) <= 1:  # Walk South
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])
            return
        if wpt_direction == 3 and 0 < x <= 2 and abs(z) <= 1:  # Walk East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])
            return
        if wpt_direction == 4 and -2 <= x < 0 and abs(z) <= 1:  # Walk West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])
            return
    else:
        '''if x == 1 and y == -1 and z == 0:  # Diagonal North East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[4], lParam[4])  # 9
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[4], lParam[4])  # 9
            return
        if x == 1 and y == 1 and z == 0:  # Diagonal South East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[6], lParam[6])  # 3
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[6], lParam[6])  # 3
            return
        if x == -1 and y == -1 and z == 0:  # Diagonal North West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[5], lParam[5])  # 7
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[5], lParam[5])  # 7
            return
        if x == -1 and y == 1 and z == 0:  # Diagonal South West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[7], lParam[7])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[7], lParam[7])
            return'''
        if x == 1 and y == 0 and z == 0:  # Walk East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])
            return
        if x == -1 and y == 0 and z == 0:  # Walk West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])
            return
        if x == 0 and y == 1 and z == 0:  # Walk South
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])
            return
        if x == 0 and y == -1 and z == 0:  # Walk North
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])
            return
        if abs(x) <= 7 and abs(y) <= 5 and z == 0:  # Map click
            left_click(coordinates_x[0] + x * 70, coordinates_y[0] + y * 70)
            time.sleep(random.uniform(0.5, 0.7))
            return


def press_key(key) -> None:
    if len(key) == 1:
        vk_code = win32api.VkKeyScan(key)
        if vk_code != -1:
            scan_code = win32api.MapVirtualKey(vk_code & 0xFF, 0)
            # Construct lParam for KEYDOWN and KEYUP
            keydown_lparam = (scan_code << 16) | 0x0001
            keyup_lparam = keydown_lparam | (0x3 << 30)
            # Send KEYDOWN message
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, vk_code & 0xFF, keydown_lparam)
            # Send KEYUP message
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, vk_code & 0xFF, keyup_lparam)


def press_hotkey(hotkey) -> None:
    hotkey_index = (((0x003A0001 >> 16) + hotkey) << 16) + 1
    win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, 0x6F + hotkey, hotkey_index)
    win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, 0x6F + hotkey, hotkey_index)