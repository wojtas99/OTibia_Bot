import Addresses
import base64
import io
import math
import os
import urllib
from urllib import request
import numpy as np
import win32con
import win32ui
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import win32gui


def sort_monsters_by_dist(point, character_x, character_y):
    """
    Calculate the distance between a given point and a character's position.

    Args:
        point (tuple): A tuple representing the coordinates of the point (x, y).
        character_x (int): X coordinate of the character.
        character_y (int): Y coordinate of the character.

    Returns:
        int: The distance between the point and the character.
    """
    calculated_distance = math.sqrt((point[0] - character_x) ** 2 + (point[1] - character_y) ** 2)
    return calculated_distance


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
            window_name (str): The name of the window to capture.
            w (int): Width of the capture area.
            h (int): Height of the capture area.
            x (int): X-coordinate of the capture starting point.
            y (int): Y-coordinate of the capture starting point.

        Raises:
            Exception: If the specified window cannot be found.
        """
        window_name = Addresses.game_name + " - " + Addresses.nickname
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


def replace_polish_characters(text):
    translation_table = str.maketrans({
        'ó': 'o',
        'ą': 'a',
        'ę': 'e',
        'ł': 'l',
        'ś': 's',
        'ć': 'c',
        'ż': 'z',
        'ź': 'z',
        'ń': 'n',
        'Ą': 'A',
        'Ę': 'E',
        'Ó': 'O',
        'Ł': 'L',
        'Ś': 'S',
        'Ć': 'C',
        'Ż': 'Z',
        'Ź': 'Z',
        'Ń': 'N'
    })

    return text.translate(translation_table)


def add_number_to_image(image: Image.Image, number: str = "2") -> Image.Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    if int(number) < 6:
        text_position = (image.width - 10, image.height - 15)
    else:
        text_position = (image.width - 15, image.height - 15)
    draw.text(text_position, number, font=font, fill=(255, 255, 255, 255))

    return image


def load_items_from_url() -> None:
    """
    Downloads images from URLs listed in 'Loot.txt', processes GIFs into individual frames,
    and saves them in the 'ItemImages' folder. Non-GIF images are combined with a background
    before saving.

    Returns:
        None
    """
    with open('Loot.txt', 'r') as f:
        for item in f:
            # Open and process the image
            item = item.strip()
            name = item.split('/')[-1].replace("_", " ")
            # Check if image already exists
            if name in os.listdir('ItemImages/'):
                continue

            # Download the image
            urllib.request.urlretrieve(item, f'ItemImages/{name}')
            gif = Image.open(f'ItemImages/{name}')
            if gif.format == 'GIF':
                name = urllib.parse.unquote(name)
                name = replace_polish_characters(name)
                frames_dir = f'ItemImages/{name.split(".gif")[0]}'
                os.makedirs(frames_dir, exist_ok=True)

                # Iterate through GIF frames and save each as a PNG
                for i, frame in enumerate(ImageSequence.Iterator(gif)):
                    frame = frame.convert('RGBA')
                    background = Image.open(io.BytesIO(base64.b64decode(Addresses.background_image))).convert('RGBA')
                    background.paste(frame, (0, 0), frame)

                    if 5 > i > 0:
                        background = add_number_to_image(background, number=str(i+1))
                    elif 6 > i > 4:
                        background = add_number_to_image(background, number=str(13))
                    elif i > 5:
                        background = add_number_to_image(background, number=str(20))

                    background.save(f'{frames_dir}/{name.split(".gif")[0]}{i}.png')
                gif.close()
                name = item.split('/')[-1].replace("_", " ")
                os.remove(f'ItemImages/{name}')  # Remove original GIF file
            else:
                # Process non-GIF images
                image1 = Image.open(f'ItemImages/{name}').convert('RGBA')
                image2 = Image.open(io.BytesIO(base64.b64decode(Addresses.background_image))).convert('RGBA')
                image2.paste(image1, (0, 0), image1)

                # Dodanie numeru "2" dla obrazu
                image2 = add_number_to_image(image2, number="2")

                image2.save(f'ItemImages/{name}')






