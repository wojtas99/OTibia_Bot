import random
import threading
import Addresses
import win32api, win32con, win32gui
mouse_lock = threading.Lock()


def mouse_function(x_source, y_source, x_dest=0, y_dest=0, option=0) ->None:
    if option != 3 or option != 5:
        x_source += random.randint(0, 10) - 5
        y_source += random.randint(0, 10) - 5
        x_dest += random.randint(0, 10) - 5
        y_dest += random.randint(0, 10) - 5
    with mouse_lock:
        if option == 1: #  Right Click
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x_source, y_source))
        if option == 2: #  Left Click
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x_source, y_source))
        if option == 3: #  Collect Item
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x_dest, y_dest))
        if option == 4: #  Drag'n'Drop
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x_dest, y_dest))
        if option == 5: #  Use on me
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0,win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1,win32api.MAKELONG(x_dest, y_dest))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0,win32api.MAKELONG(x_dest, y_dest))


def manage_collect(x, y, action) -> None:
    if action > 0:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], Addresses.coordinates_x[action], Addresses.coordinates_y[action], option=3)
    elif action == 0:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], Addresses.coordinates_x[0], Addresses.coordinates_y[0], option=4)
    elif action == -1:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], option=1)
    elif action == -2:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], option=2)
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], option=2)
    elif action == -3:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], Addresses.coordinates_x[0], Addresses.coordinates_y[0], option=5)