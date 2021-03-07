from Pawn import Pawn
from Bishop import Bishop


class Board:
    def __init__(self):
        self.board = self.create_field()
        self.reverse = False
        self.abcnum = ('A', 'H')
        self.coords = (0, 0)

    def create_field(self):
        return [[' '] * 8 for i in range(8)]

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
        for i, lst in enumerate(self.board):
            print(len(self.board) - i, *lst + ["\033[0m"])
        print(' ', end=' ')
        for i in range(ord(self.abcnum[0]), ord(self.abcnum[1]) + 1):
            print(chr(i), end=' ')
        print()

    def clear(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if 'Δ' in str(self.board[i][j]):
                    self.board[i][j] = ' '
                elif self.board[i][j] != ' ':
                    self.board[i][j].option = False


def game():
    players = ["white", "black"]
    board = Board()
    board.fill(Pawn=Pawn, Knight=Pawn, Bishop=Bishop, Queen=Pawn, King=Pawn, Rook=Pawn)
    while True:
        board.display()
        piece = board.check(input("Введите координаты фигуры\n"))
        if not piece:
            print("Координаты фигуры введены не верно")
            continue
        frow, fcol = board.coords
        if board.board[frow][fcol].color != players[0]:
            print("Ход другого игрока")
            continue
        board.board[frow][fcol].move_options()
        board.display()
        while True:
            bias = board.check(input("Введите координаты хода\n"))
            if not bias:
                print("Координаты введены не верно")
                continue
            mrow, mcol = board.coords
            board.board[frow][fcol].move((mrow, mcol))
            break
        board.clear()
        players.append(players.pop(0))
        if board.reverse:
            board.board.reverse()


def out(text):
    for i in (31, 36, 37):
        print("\033[{}m {}".format(i, text))


import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
if __name__ == "__main__":
    game()