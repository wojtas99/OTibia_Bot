import sys
from urllib.request import urlopen  # <-- Use the standard library urlopen

import urllib3
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QVBoxLayout


class DownloadThread(QThread):
    data_downloaded = pyqtSignal(str, str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        # Use urllib.request.urlopen
        http = urllib3.PoolManager()
        r = http.request('GET', self.url)
        info = r.headers
        self.data_downloaded.emit(self.url, str(info))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.list_widget = QListWidget()
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.start_download)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def start_download(self):
        urls = [
            'http://google.com',
            'http://twitter.com',
            'http://yandex.ru',
            'http://stackoverflow.com/',
            'http://www.youtube.com/'
        ]
        self.threads = []
        for url in urls:
            downloader = DownloadThread(url)
            downloader.data_downloaded.connect(self.on_data_ready)
            self.threads.append(downloader)
            downloader.start()

    def on_data_ready(self, url, info):
        """
        Slot method that accepts two arguments:
        1) The URL string
        2) The response info (headers) string
        """
        self.list_widget.addItem(f"URL: {url}\n{info}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec())


