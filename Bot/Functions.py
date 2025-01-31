import base64
import io
import requests
from PIL import Image, ImageSequence
import numpy as np
import cv2 as cv
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
import Addresses
from MemoryFunctions import read_pointer_address, read_memory_address


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
                    '''cv.imshow("test", background)
                    cv.waitKey(0)
                    cv.destroyAllWindows()'''
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


def delete_item(list_widget, item) -> None:
    # Get the index of the clicked item
    index = list_widget.row(item)
    # Remove the item using the index
    list_widget.takeItem(index)


def read_my_stats():
    if Addresses.client_name == "Altaron":
        current_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_offset, 1)
        current_max_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_max_offset, 1)
        current_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_offset, 1)
        current_max_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_max_offset, 1)
        return current_hp, current_max_hp, current_mp, current_max_mp
    elif Addresses.client_name == "Medivia":
        current_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_offset, 3)
        current_max_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_max_offset, 3)
        current_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_offset, 3)
        current_max_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_max_offset, 3)
        return current_hp, current_max_hp, current_mp, current_max_mp
    elif Addresses.client_name == "WADclient":
        current_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_offset, 3)
        current_max_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_max_offset, 3)
        current_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_offset, 3)
        current_max_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_max_offset, 3)
        return current_hp, current_max_hp, current_mp, current_max_mp


def read_my_wpt():
    try:
        x = read_memory_address(Addresses.my_x_address, 0, 1)
        y = read_memory_address(Addresses.my_y_address, 0, 1)
        z = read_memory_address(Addresses.my_z_address, 0, 7)
        if x is None or y is None or z is None:
            print("Failed to read coordinates.")
            return None, None, None
        return x, y, z
    except Exception as e:
        print(f"Exception in read_my_wpt: {e}")
        return None, None, None


def read_target_info():
    if Addresses.client_name == "Altaron":
        target_x = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_x = read_memory_address(target_x, Addresses.target_x_offset, 1)
        target_y = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_y = read_memory_address(target_y, Addresses.target_y_offset, 1)
        target_z = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_z = read_memory_address(target_z, Addresses.target_z_offset, 4)
        target_name = "*"
        target_hp = read_memory_address(read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address, Addresses.target_hp_offset, 7)
        return target_x, target_y, target_z, target_name, target_hp
    elif Addresses.client_name == "Medivia":
        target_x = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_x = read_memory_address(target_x, Addresses.target_x_offset, 1)
        target_y = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_y = read_memory_address(target_y, Addresses.target_y_offset, 1)
        target_z = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_z = read_memory_address(target_z, Addresses.target_z_offset, 4)
        target_name = "*"
        target_hp = read_memory_address(read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address, Addresses.target_hp_offset, 7)
        return target_x, target_y, target_z, target_name, target_hp
    elif Addresses.client_name == "WADclient":
        target_x = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_x = read_memory_address(target_x, Addresses.target_x_offset, 1)
        target_y = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_y = read_memory_address(target_y, Addresses.target_y_offset, 1)
        target_z = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_z = read_memory_address(target_z, Addresses.target_z_offset, 7)
        target_name = "*"
        target_hp = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_hp = read_memory_address(target_hp, Addresses.target_hp_offset, 7)
        return target_x, target_y, target_z, target_name, target_hp


