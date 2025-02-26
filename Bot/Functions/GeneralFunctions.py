import base64
import io
import requests
import win32con
import win32gui
import win32ui
from PIL import Image, ImageSequence
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
    if Addresses.client_name == "Altaron":
        for item_index in range(list_widget.count()):
            item_name = list_widget.item(item_index).text()
            item_data = list_widget.item(item_index).data(Qt.UserRole)
            loot_container = item_data['Loot']
            item_name = item_name.replace(' ', '_')
            response = requests.get(f'https://wiki.altaron.pl/images/{item_name}.gif')
            if item_name == 'Sakiewka':
                item_image = Image.open(io.BytesIO(base64.b64decode(
                    'iVBORw0KGgoAAAANSUhEUgAAACIAAAAWCAAAAACAxxGlAAAB4UlEQVQoFRXBWVLcQBAFwPeqq6VpLXAbh38IB9hmuf9FQKO1lyrjTD5JVNarVHNof+uVINnyeWYH6Q4+iQYvV2nm0K7vlITA8nVWpwgc/AVavXJt7pQYNQhIWs3FEDQEgs9ervPKzR2khCBCEm7VnNr1Ucnf7di2q7iDACkUCuluBtE+Db3wtazLejaA+I8UCgm4g9oPc1K+leVzvQwQEN9IIQnAgdCP8xT5npfPNTeQQoJCAnDQAUgcH6bI17J8bdmcFAkhiNCtmTnhEB3mOfJPuS9bMYBBYx+D0Gu+qoEANU1T5EtZl704yBDTcFPCyrGfDSQY0jQpn8t636uTlH6YU6S3a1uPBhLQ2zQpX8q67NWFlG6Yh0ir57aejQQY0jQp/5b7shcnKdqPKdLKeRzFSACapkn5Xu5fWzF+k9h3Sqv5Kg0gQE3zqPwo92XLBlAkBBV4a7WZAwQ1zaPyo9yXrTRQQggE4DBrzRyAaJqGyLeyLlsxinademsOodVcqwOit3FQvtT1fhSn3oaklrNJEM/nlZuD2o9J+VT29agI/TgP2s6rMarnYzuzgdqnFPiz7ttVEdPDw6j1OKrEiLKv21VB7dIt8Ec9tqshDo+Po5bjqOwiyn7fzgqG/nYL/wCI3CF0bN+r4gAAAABJRU5ErkJggg=='
                    ))).convert('RGBA')
                image_np = np.array(item_image)
                image_bgr = cv.cvtColor(image_np, cv.COLOR_RGBA2BGR)
                item_image = cv.cvtColor(image_bgr, cv.COLOR_BGR2GRAY)
                item_image = cv.resize(item_image, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)
                Addresses.item_list[item_name] = []
                Addresses.item_list[item_name].append(item_image)
                Addresses.item_list[item_name].append(loot_container)
            if response.status_code != 200 or item_name == 'Sakiewka':
                continue

            item_image = Image.open(io.BytesIO(response.content))
            Addresses.item_list[item_name] = []
            if item_image.format == 'GIF':
                for i, frame in enumerate(ImageSequence.Iterator(item_image)):
                    frame_rgba = frame.convert('RGBA')
                    background = Image.open(
                        io.BytesIO(base64.b64decode(Addresses.background_image))
                    ).convert('RGBA')
                    datas = frame_rgba.getdata()
                    newData = []
                    for item in datas:
                        if item[0] == 255 and item[1] == 255 and item[2] == 255:
                            newData.append((255, 255, 255, 0))
                        else:
                            newData.append(item)
                    frame_rgba.putdata(newData)
                    background.paste(frame_rgba, (0, 0), frame_rgba)
                    background = np.array(background)
                    background = background[:22, :, :]
                    background = cv.cvtColor(background, cv.COLOR_BGR2GRAY)
                    background = cv.GaussianBlur(background, (7, 7), 0)
                    background = cv.resize(background, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)
                    background = np.array(background)
                    Addresses.item_list[item_name].append(background)
                item_image.close()
                Addresses.item_list[item_name].append(loot_container)
    elif Addresses.client_name == "Medivia":
        for item_index in range(list_widget.count()):
            item_name = list_widget.item(item_index).text()
            item_data = list_widget.item(item_index).data(Qt.UserRole)
            loot_container = item_data['Loot']
            item_name = item_name.replace(' ', '_')
            file_page_url = f"https://wiki.mediviastats.info/File:{item_name}.gif"
            response = requests.get(file_page_url)
            if response:
                soup = BeautifulSoup(response.text, "html.parser")
                full_media_div = soup.find("div", class_="fullMedia")
                if not full_media_div:
                    continue
                gif_url = full_media_div.find("a").get("href")
                response = requests.get('https://wiki.mediviastats.info' + gif_url)
                if response.status_code != 200:
                    continue
                item_image = Image.open(io.BytesIO(response.content))
                Addresses.item_list[item_name] = []
                if item_image.format == 'GIF':
                    for i, frame in enumerate(ImageSequence.Iterator(item_image)):
                        frame_rgba = frame.convert('RGBA')
                        background = Image.open(
                            io.BytesIO(base64.b64decode(Addresses.background_image))
                        ).convert('RGBA')
                        background.paste(frame_rgba, (0, 0), frame_rgba)
                        background = np.array(background)
                        background = background[:22, :, :]
                        background = cv.cvtColor(background, cv.COLOR_BGR2GRAY)
                        background = cv.GaussianBlur(background, (7, 7), 0)
                        background = cv.resize(background, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)
                        background = np.array(background)
                        Addresses.item_list[item_name].append(background)
                    item_image.close()
                    Addresses.item_list[item_name].append(loot_container)
            else:
                file_page_url = f"https://wiki.mediviastats.info/File:{item_name}.png"
                response = requests.get(file_page_url)
                if response:
                    soup = BeautifulSoup(response.text, "html.parser")
                    full_media_div = soup.find("div", class_="fullMedia")
                    if not full_media_div:
                        continue
                    gif_url = full_media_div.find("a").get("href")
                    response = requests.get('https://wiki.mediviastats.info' + gif_url)
                    if response.status_code != 200:
                        continue
                    item_image = Image.open(io.BytesIO(response.content))
                    Addresses.item_list[item_name] = []
                    frame_rgba = item_image.convert('RGBA')
                    background = Image.open(
                        io.BytesIO(base64.b64decode(Addresses.background_image))
                    ).convert('RGBA')
                    background.paste(frame_rgba, (0, 0), frame_rgba)
                    background = np.array(background)
                    background = background[:22, :, :]
                    background = cv.cvtColor(background, cv.COLOR_BGR2GRAY)
                    background = cv.GaussianBlur(background, (7, 7), 0)
                    background = cv.resize(background, None, fx=zoom_img, fy=zoom_img, interpolation=cv.INTER_CUBIC)
                    background = np.array(background)
                    Addresses.item_list[item_name].append(background)
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




