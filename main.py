import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QInputDialog, QPushButton, QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize
import shutil
import requests

SCREEN_SIZE = [700, 700]


def is_normal_line(line):
    if line == '':
        return False
    for i in line:
        if i.isdigit() or i == '.' or i == ',':
            pass
        else:
            return False
    return True


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.payload = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b', 'll': '37.818474,55.654924', 'z': '9',
                        'l': 'map'}


        self.map_file = ''

        uic.loadUi('Map_design.ui', self)

        self.button_connections()

        self.get_map()
        self.init_image()

    def get_map(self):
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=self.payload)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def init_image(self):
        self.image = QImage(self.map_file).scaled(814, 741)
        self.pixmap = QPixmap.fromImage(self.image)
        self.frame.setPixmap(self.pixmap)

        self.show()

    def button_connections(self):
        self.search_button.clicked.connect(self.load_new_params)

    def load_new_params(self):
        x = self.x_line.text()
        y = self.y_line.text()
        z = self.z_line.text()
        if is_normal_line(x) and is_normal_line(y) and is_normal_line(z):
            self.payload['ll'] = x + ',' + y
            self.payload['z'] = z
        self.get_map()
        self.init_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pril = Map()
    pril.setFixedSize(838, 826)
    sys.exit(app.exec())
