import io
import urllib

import requests
import win32con
import win32gui
import win32ui
from PIL import Image, ImageSequence, ImageFile
import numpy as np
import cv2 as cv
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup

import Addresses
import os
import json


def load_items_images(list_widget) -> None:
    zoom_img = 3
    Addresses.item_list = {}
    link = Addresses.item_link
    for item_index in range(list_widget.count()):
        item_name = list_widget.item(item_index).text()
        item_data = list_widget.item(item_index).data(Qt.UserRole)
        loot_container = item_data['Loot']
        item_name = item_name.replace(' ', '_')
        if item_name[0] == '*':
            item = Image.open(f'Images/{Addresses.client_name}/{item_name[1:]}.png').convert('RGBA')
            item = np.array(item)
            item = item[:22, :, :]
            item = cv.cvtColor(item, cv.COLOR_BGR2GRAY)
            item = cv.GaussianBlur(item, (7, 7), 0)
            item = cv.resize(item, None, fx=zoom_img, fy=zoom_img,
                                      interpolation=cv.INTER_CUBIC)
            Addresses.item_list[item_name[1:]] = []
            Addresses.item_list[item_name[1:]].append(item)
            Addresses.item_list[item_name[1:]].append(loot_container)
        else:
            response = requests.get(f'{link}{item_name}.gif')
            if response.status_code != 200:
                response = requests.get(f'{link}{item_name}.png')
                if response.status_code != 200:
                    continue
            soup = BeautifulSoup(response.text, "html.parser")
            full_media_div = soup.find("div", class_="fullMedia")
            if not full_media_div:
                continue
            media_url = full_media_div.find("a").get("href")
            base_link = link[:link.rfind('/')]
            parsed = urllib.parse.urlparse(base_link + media_url)
            base_link = f"{parsed.scheme}://{parsed.netloc}"
            response = requests.get(base_link + media_url)
            if response.status_code != 200:
                continue

            Addresses.item_list[item_name] = []
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            item_image = Image.open(io.BytesIO(response.content))
            if item_image.format == 'GIF':
                for frame in ImageSequence.Iterator(item_image):
                    frame_rgba = frame.convert('RGBA')
                    datas = frame_rgba.getdata()
                    newData = [
                        (255, 255, 255, 0) if (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255) else pixel
                        for pixel in datas
                    ]
                    frame_rgba.putdata(newData)
                    background = Image.open(f'Images/{Addresses.client_name}/Background.png').convert('RGBA')
                    background.paste(frame_rgba, (0, 0), frame_rgba)
                    background_np = np.array(background)
                    background_np = background_np[:22, :, :]
                    background_np = cv.cvtColor(background_np, cv.COLOR_BGR2GRAY)
                    background_np = cv.GaussianBlur(background_np, (7, 7), 0)
                    background_np = cv.resize(background_np, None, fx=zoom_img, fy=zoom_img,
                                              interpolation=cv.INTER_CUBIC)
                    Addresses.item_list[item_name].append(background_np)
                item_image.close()
            elif item_image.format == 'PNG':
                image_rgba = item_image.convert('RGBA')
                datas = image_rgba.getdata()
                newData = [
                    (255, 255, 255, 0) if (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255) else pixel
                    for pixel in datas
                ]
                image_rgba.putdata(newData)
                background = Image.open(f'Images/{Addresses.client_name}/Background.png').convert('RGBA')
                background.paste(image_rgba, (0, 0), image_rgba)
                background_np = np.array(background)
                background_np = background_np[:22, :, :]
                background_np = cv.cvtColor(background_np, cv.COLOR_BGR2GRAY)
                background_np = cv.GaussianBlur(background_np, (7, 7), 0)
                background_np = cv.resize(background_np, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)
                Addresses.item_list[item_name].append(background_np)
                item_image.close()
            else:
                item_image.close()
                continue

            Addresses.item_list[item_name].append(loot_container)


def merge_close_points(points, distance_threshold):
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
    def __init__(self, w, h, x, y):
        window_name = Addresses.game_name + " - EasyBot"
        self.hwnd = win32gui.FindWindow(None, window_name)
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dc_obj = win32ui.CreateDCFromHandle(wDC)
        cDC = dc_obj.CreateCompatibleDC()
        data_bitmap = win32ui.CreateBitmap()
        data_bitmap.CreateCompatibleBitmap(dc_obj, self.w, self.h)
        cDC.SelectObject(data_bitmap)
        cDC.BitBlt((0, 0), (self.w, self.h), dc_obj, (self.x, self.y), win32con.SRCCOPY)
        signed_ints_array = data_bitmap.GetBitmapBits(True)
        img = np.frombuffer(signed_ints_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dc_obj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(data_bitmap.GetHandle())
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img


def delete_item(list_widget, item) -> None:
    index = list_widget.row(item)
    list_widget.takeItem(index)


def manage_profile(action: str, directory: str, profile_name: str, data: dict = None):
    file_path = os.path.join(directory, f"{profile_name}.json")
    if action.lower() == "save":
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    elif action.lower() == "load":
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r") as f:
            return json.load(f)




