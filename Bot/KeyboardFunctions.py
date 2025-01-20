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
            win32api.SendMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])
            win32api.SendMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])
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
        if x == 1 and y == -1 and z == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[4], lParam[4])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[4], lParam[4])
            return
        if x == 1 and y == 1 and z == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[6], lParam[6])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[6], lParam[6])
            return
        if x == -1 and y == -1 and z == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[5], lParam[5])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[5], lParam[5])
            return
        if x == -1 and y == 1 and z == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[7], lParam[7])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[7], lParam[7])
            return
        if (x == 1 or x == 2) and -2 < y < 2 and z == 0:  # Walk East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])
            return
        if (x == -1 or x == -2) and -2 < y < 2 and z == 0:  # Walk West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])
            return
        if -2 < x < 2 and (y == 1 or y == 2) and z == 0:  # Walk South
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])
            return
        if -2 < x < 2 and (y == -1 or y == -2) and z == 0:  # Walk North
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])
            return
    if abs(x) <= 7 and abs(y) <= 5 and z == 0:
        left_click(coordinates_x[0] + x * 75, coordinates_y[0] + y * 75)
        time.sleep(1)
        return


def press_hotkey(hotkey) -> None:
    hotkey_index = (((0x003A0001 >> 16) + hotkey) << 16) + 1
    win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, 0x6F + hotkey, hotkey_index)
    win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, 0x6F + hotkey, hotkey_index)