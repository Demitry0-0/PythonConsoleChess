class Rook:
    def __init__(self, board, coords, color):
        self.board = board
        self.row, self.col = coords
        self.color = color
        self.first = True
        self.option = False

    def move_options(self):
        row, col = self.row, self.col
        flag = False
        size = (len(self.board.board), len(self.board.board[0]))
        for i in range(2):
            k = 1
            f1 = f2 = False
            while True:
                for j in (1, -1):
                    if j == 1 and f1:
                        continue
                    elif j == -1 and f2:
                        continue
                    rw = row + j * k * abs(i - 1)
                    cl = col + j * k * i
                    if 0 <= rw < size[0] and 0 <= cl < size[1]:
                        if self.board.board[rw][cl] == ' ':
                            self.board.board[rw][cl] = self.board.space
                            flag = True
                            continue
                        elif self.board.board[rw][cl].color != self.color:
                            self.board.board[rw][cl].option = flag = True
                    if j == 1:
                        f1 = True
                    elif j == -1:
                        f2 = True
                if f1 and f2:
                    break
                k += 1
        return flag

    def check_move(self, coords):
        row, col = coords
        if (row == self.row and col == self.col) or (row != self.row and col != self.col):
            return False
        k1 = (1 if row > self.row else -1) if row != self.row else 0
        k2 = (1 if col > self.col else -1) if col != self.col else 0
        row -= k1
        col -= k2
        for i in range(abs(self.row - row)):
            for j in range(abs(self.col - col)):
                if i == j == 0:
                    continue
                print(row + i * k1, col + j * k2)
                if self.board.board[row + i * k1][col + j * k2] != ' ' and \
                        'Δ' not in str(self.board.board[row + i * k1][col + j * k2]):
                    if self.board.board[row + i * k1][col + j * k2].color == self.color:
                        return False
        return True

    def move(self, coords):
        row, col = coords
        if not self.check_move(coords):
            return False
        self.board.board[self.row][self.col] = ' '
        self.board.board[row][col] = self
        self.row, self.col = row, col
        self.first = False
        return True

    def __repr__(self):
        if self.option:
            return "\033[36m#"
        if self.color == "white":
            return "\033[37m#"
        if self.color == "black":
            return "\033[31m#"
