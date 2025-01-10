import Addresses
import numpy as np
import win32con
import win32ui
import win32gui

from MouseFunctions import collect_item, drag_drop, right_click, left_click


def merge_close_points(points, distance_threshold):
    """
    Merge points that are within a specified distance of each other.

    Args:
        points (list of tuples): A list of tuples representing the coordinates of points.
        distance_threshold (float): The distance threshold to merge points.

    Returns:
        list of tuples: A list of merged points.
    """
    merged_points = []
    merged_indices = set()

    def merge_distance(point1, point2):
        return np.sqrt(np.sum((point1 - point2) ** 2))

    for i in range(len(points)):
        if i not in merged_indices:
            current_point = points[i]
            merged_point = np.array(current_point)
            for j in range(i + 1, len(points)):
                if merge_distance(np.array(current_point), np.array(points[j])) < distance_threshold:
                    merged_point = (merged_point + np.array(points[j])) / 2
                    merged_indices.add(j)
            merged_points.append(tuple(merged_point))

    return merged_points


class WindowCapture:
    w = 0
    h = 0
    hwnd = None

    def __init__(self,w, h, x, y):
        """
        Initializes the WindowCapture object to capture a screenshot of a specified window.

        Args:
            w (int): Width of the capture area.
            h (int): Height of the capture area.
            x (int): X-coordinate of the capture starting point.
            y (int): Y-coordinate of the capture starting point.

        Raises:
            Exception: If the specified window cannot be found.
        """
        window_name = Addresses.game_name + " - " + Addresses.numberEasyBot
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def get_screenshot(self):
        """
        Captures a screenshot of the specified window region.

        Returns:
            np.ndarray: The screenshot image as a NumPy array in RGB format.
        """
        # Get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dc_obj = win32ui.CreateDCFromHandle(wDC)
        cDC = dc_obj.CreateCompatibleDC()
        data_bitmap = win32ui.CreateBitmap()
        data_bitmap.CreateCompatibleBitmap(dc_obj, self.w, self.h)
        cDC.SelectObject(data_bitmap)
        cDC.BitBlt((0, 0), (self.w, self.h), dc_obj, (self.x, self.y), win32con.SRCCOPY)

        # Convert the raw data into a format OpenCV can read
        signed_ints_array = data_bitmap.GetBitmapBits(True)
        img = np.frombuffer(signed_ints_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)  # 4 bytes per pixel (RGBA)

        # Clean up
        dc_obj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(data_bitmap.GetHandle())

        # Drop the alpha channel and make the array contiguous
        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img


def manage_collect(x, y, action) -> None:
    if action > 0:
        collect_item(x + Addresses.screen_x[0], y + Addresses.screen_y[0], Addresses.coordinates_x[action], Addresses.coordinates_y[action])
    elif action == 0:
        drag_drop(x + Addresses.screen_x[0], y + Addresses.screen_y[0])
    elif action == -1:
        right_click(x + Addresses.screen_x[0], y + Addresses.screen_y[0])
    elif action == -2:
        left_click(x + Addresses.screen_x[0], y + Addresses.screen_y[0])
        left_click(x + Addresses.screen_x[0], y + Addresses.screen_y[0])






