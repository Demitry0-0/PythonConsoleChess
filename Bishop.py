class Bishop:
    def __init__(self, board, coords, color):
        self.board = board
        self.row, self.col = coords
        self.color = color
        self.option = False

    def move_options(self):
        for kr, kc in (1, 1), (1, -1), (-1, 1), (-1, -1):
            i, j = kr, kc
            flag = False
            while 0 <= self.row + i < len(self.board.board) and \
                    0 <= self.col + j < len(self.board.board[0]):
                if flag:
                    if self.board.board[self.row + i][self.col + j].color != self.color:
                        self.board.board[self.row + i][self.col + j].option = True
                    break
                if self.board.board[self.row + i][self.col + j] == ' ':
                    self.board.board[self.row + i][self.col + j] = "\033[36mΔ"
                else:
                    flag = True
                    continue
                i += kr
                j += kc

    def check_move(self, coords):
        row, col = coords
        if abs(self.row - row) != abs(self.col - col):
            return False
        kr, kc = self.k(row, col)
        i, j = kr, kc
        while 0 <= self.row + i < len(self.board.board) and \
                0 <= self.col + j < len(self.board.board[0]):
            if self.board.board[self.row + i][self.col + j] != ' ' and \
                    'Δ' not in str(self.board.board[self.row + i][self.col + j]):
                if self.board.board[self.row + i][self.col + j].color == self.color:
                    return False
                if self.row + i - row:
                    return False
            i += kr
            j += kc
        return True

    def move(self, coords):
        row, col = coords
        if not self.check_move(coords):
            return False
        self.board.board[self.row][self.col] = ' '
        self.board.board[row][col] = self
        self.row, self.col = row, col
        return True

    def k(self, row, col):
        if self.row - row < 0:
            if self.col - col < 0:
                return -1, -1
            return -1, 1
        elif self.col - col < 0:
            return 1, -1
        return 1, 1

    def __repr__(self):
        if self.option:
            return "\033[36m!"
        if self.color == "white":
            return "\033[37m!"
        if self.color == "black":
            return "\033[31m!"
