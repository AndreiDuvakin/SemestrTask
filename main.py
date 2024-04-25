import random
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.score = None
        self.field = None
        self.active_button = False
        self.setWindowTitle('Игра: Две лисы и 20 кур')
        self.setFixedSize(800, 700)
        self.buttons = []
        self.setWindowIcon(QIcon('img/chicken.png'))

        self.path = 'img/'

        self.init_game()

    def init_game(self):
        self.field = [['w' for _ in range(7)] for _ in range(7)]
        self.active_button = None
        self.score = 0

        for i in range(7):
            for j in range(7):
                if (2 <= j <= 4 and i <= 1) or (2 <= j <= 4 and i >= 5) or (2 <= i <= 4):
                    button = QPushButton(self)
                    button.setGeometry(103 + j * 81, 69 + 81 * i, 75, 75)
                    button.setIconSize(QSize(75, 75))
                    button.clicked.connect(self.button_checker)
                    button.object = ''
                    self.field[i][j] = button
                else:
                    button = QPushButton(self)
                    button.setGeometry(103 + j * 81, 69 + 81 * i, 0, 0)
                    button.setIconSize(QSize(75, 75))
                    button.object = 'w'
                    button.clicked.connect(self.button_checker)
                    self.field[i][j] = button

        for i in range(7):
            for j in range(7):
                if i > 2 and self.field[i][j].object != 'w':
                    self.field[i][j].object = 'c'

        self.field[2][2].object = 'f'
        self.field[2][4].object = 'f'
        self.load_field()

    def find_qpushbutton_index(self, button):
        for i in range(7):
            for j in range(7):
                if isinstance(self.field[i][j], QPushButton) and self.field[i][j] == button:
                    return i, j
        return -1, -1

    def fox_stepping(self, fox):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dx, dy in directions:
            new_x, new_y = fox[0] + dx, fox[1] + dy
            if 0 <= new_x < 7 and 0 <= new_y < 7:
                if dx == -2 and self.field[new_x + 1][new_y].object == "c" and self.field[new_x][new_y].object == "":
                    self.field[new_x + 1][new_y].object = ""
                    self.field[new_x][new_y].object = "f"
                    self.field[fox[0]][fox[1]].object = ""
                    return
                elif dx == 2 and self.field[new_x - 1][new_y].object == "c" and self.field[new_x][new_y].object == "":
                    self.field[new_x - 1][new_y].object = ""
                    self.field[new_x][new_y].object = "f"
                    self.field[fox[0]][fox[1]].object = ""
                    return
                elif dy == -2 and self.field[new_x][new_y + 1].object == "c" and self.field[new_x][new_y].object == "":
                    self.field[new_x][new_y + 1].object = ""
                    self.field[new_x][new_y].object = "f"
                    self.field[fox[0]][fox[1]].object = ""
                    return
                elif dy == 2 and self.field[new_x][new_y - 1].object == "c" and self.field[new_x][new_y].object == "":
                    self.field[new_x][new_y - 1].object = ""
                    self.field[new_x][new_y].object = "f"
                    self.field[fox[0]][fox[1]].object = ""
                    return
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = fox[0] + dx, fox[1] + dy
            if 0 <= new_x < 7 and 0 <= new_y < 7:
                if self.field[new_x][new_y].object == "":
                    self.field[new_x][new_y].object = "f"
                    self.field[fox[0]][fox[1]].object = ""
                    return

    def load_field(self):
        for i in range(7):
            for j in range(7):
                if isinstance(self.field[i][j], QPushButton):
                    match self.field[i][j].object:
                        case 'f':
                            self.field[i][j].setIcon(QIcon(QPixmap(self.path + 'fox.png')))
                        case 'c':
                            self.field[i][j].setIcon(QIcon(QPixmap(self.path + 'chicken.png')))
                        case _:
                            self.field[i][j].setIcon(QIcon(QPixmap()))

    def find_cor_fox(self):
        foxes = []
        for i in range(7):
            for j in range(7):
                if isinstance(self.field[i][j], QPushButton) and self.field[i][j].object == 'f':
                    foxes.append((i, j))
        return foxes

    def button_checker(self):
        button = self.sender()
        if self.active_button:
            i1, j1 = self.find_qpushbutton_index(button)
            i2, j2 = self.find_qpushbutton_index(self.active_button)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                new_x, new_y = i2, j2
                new_x += dx
                new_y += dy
                if 0 <= new_x < 7 and 0 <= new_y < 7:
                    if self.field[new_x][new_y].object == "":
                        self.field[new_x][new_y].setStyleSheet('''''')
            if (abs(i1 - i2) == 1 and abs(j1 - j2) == 0 or abs(i1 - i2) == 0 and abs(j1 - j2) == 1) and i1 <= i2:
                self.field[i1][j1].object, self.field[i2][j2].object = self.field[i2][j2].object, self.field[i1][
                    j1].object
                self.active_button = None
                foxes = self.find_cor_fox()
                for fox in foxes:
                    self.fox_stepping(fox)
            else:
                self.active_button = False
        else:
            if button.object == 'c':
                self.active_button = button
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dx, dy in directions:
                    new_x, new_y = self.find_qpushbutton_index(self.active_button)
                    new_x += dx
                    new_y += dy
                    if 0 <= new_x < 7 and 0 <= new_y < 7:
                        if self.field[new_x][new_y].object == "":
                            self.field[new_x][new_y].setStyleSheet('''
                            QPushButton {
                                background-color: rgb(0, 150, 0);
                            }
                            ''')
        self.load_field()
        self.is_win()

    def is_win(self):
        chicken_count = 0
        for i in range(7):
            for j in range(7):
                if isinstance(self.field[i][j], QPushButton) and self.field[i][j].object == 'c':
                    chicken_count += 1
        if chicken_count < 9:
            QMessageBox.information(self, 'Game Over', 'К сожалению, вы проиграли')
            self.new_game = MainWindow()
            self.new_game.show()
            self.close()
            del self
        elif (self.field[0][2].object == 'c' and self.field[0][3].object == 'c' and self.field[0][4].object == 'c' and
              self.field[1][2].object == 'c' and self.field[1][3].object == 'c' and self.field[1][4].object == 'c' and
              self.field[2][2].object == 'c' and self.field[2][3].object == 'c' and self.field[2][4].object == 'c'):
            QMessageBox.information(self, 'Game Over', 'Поздравляем, вы победили!')
            self.new_game = MainWindow()
            self.new_game.show()
            self.close()
            del self


def a(b, c, d):
    sys.__excepthook__(b, c, d)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = a
    sys.exit(app.exec())
