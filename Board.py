from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen
from King import King
import os


class Board:
    def __init__(self):
        self.board = self.create_field()
        self.reverse = False
        self.abcnum = ('A', 'H')
        self.coords = (0, 0)
        self.space = "\033[36mΔ"
        self.comand = ''

    def create_field(self):
        return [[' '] * 8 for _ in range(8)]

    def fill(self, Pawn, Knight, Bishop, Rook, Queen, King):
        mrow, mcol = len(self.board), len(self.board[0])
        lst = [Rook, Knight, Bishop]
        lst = lst + [Queen, King] + lst[::-1]
        colors = ("black", "white")
        k = 0
        for i in range(2):
            for j in range(mcol):
                self.board[0][j] = lst[j](self, ((len(self.board) - 1) * i, j), colors[i])
                self.board[1][j] = Pawn(self, (abs(i - 1) + (len(self.board) - 2) * i, j), colors[i])
            self.board.reverse()

    def check(self, coords):
        try:
            if coords.lower() in ("exit", "replay"):
                self.comand = coords.lower()
            elif coords.lower() == "reverse":
                self.reverse = not self.reverse
            row, col = sorted("".join(coords.split()), key=lambda x: ord(x))
            if not col.isalpha() or not row.isdigit():
                return False
            if len(col) > 1:  # Можно модернизировать!
                return False
            row = len(self.board) - int(row)
            col = ord(col.upper()) - ord(self.abcnum[0])
            if not (0 <= row < len(self.board) and 0 <= col < len(self.board[0])):
                return False
            if self.board[row][col] == ' ':
                return False
            self.coords = (row, col)
            return True
        except Exception:
            return False

    def display(self):
        os.system("cls")
        print("\b", end='')
        for i, lst in enumerate(self.board):
            print(len(self.board) - i, *lst + ["\033[0m"])
        print(' ', end=' ')
        for i in range(ord(self.abcnum[0]), ord(self.abcnum[1]) + 1):
            print(chr(i), end=' ')
        print()

    def clear(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.space == self.board[i][j]:
                    self.board[i][j] = ' '
                elif self.board[i][j] != ' ':
                    self.board[i][j].option = False


def game():
    players = ["white", "black"]
    board = Board()
    board.fill(Pawn=Pawn, Knight=Knight, Rook=Rook, Bishop=Bishop, Queen=Queen, King=King)
    kings = {"black": board.board[0][4], "white": board.board[7][4]}
    flag = True
    error = ''
    while True:
        if flag:
            board.display()
            print(error)
            piece = board.check(input("Введите координаты фигуры\n"))
            if not piece:
                error = "Координаты фигуры введены не верно"
                continue
        flag = True
        frow, fcol = board.coords
        if board.board[frow][fcol].color != players[0]:
            error = "Ход другого игрока"
            continue
        if not board.board[frow][fcol].move_options():
            error = "У этой фигуры нет ходов"
            continue
        error = ''
        while True:
            board.display()
            print(error)
            bias = board.check(input("Введите координаты хода\n"))
            if not bias:
                if board.comand == "exit":
                    return False
                elif board.comand == "replay":
                    return True
                error = "Координаты введены не верно"
                continue
            mrow, mcol = board.coords
            if board.board[mrow][mcol] != board.space and \
                    board.board[frow][fcol].color == board.board[mrow][mcol].color:
                flag = False
                break
            space = board.board[mrow][mcol]
            if not board.board[frow][fcol].move((mrow, mcol)):
                error = "Фигура туда пойти не может"
                continue
            if kings[players[0]].check_shah(kings[players[0]].coords):
                error = "Короля нельзя ставить под шах"
                board.board[mrow][mcol].move((frow, fcol))
                board.board[mrow][mcol] = space
                continue
            kings[players[1]].shah = kings[players[1]].check_shah(kings[players[1]].coords)
            break
        error = ''
        board.clear()
        if flag:
            players.append(players.pop(0))
            if board.reverse:
                board.board.reverse()


if __name__ == "__main__":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    while game():
        pass
