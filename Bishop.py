class Bishop:
    def __init__(self, board, coords, color):
        self.board = board
        self.row, self.col = coords
        self.color = color
        self.option = False
        self.walk = False

    def move_options(self):
        flag = False
        for kr, kc in (1, 1), (1, -1), (-1, 1), (-1, -1):
            i, j = kr, kc
            f = False
            while 0 <= self.row + i < len(self.board.board) and \
                    0 <= self.col + j < len(self.board.board[0]):
                if f:
                    if self.board.board[self.row + i][self.col + j].color != self.color:
                        self.board.board[self.row + i][self.col + j].option = flag = True
                    break
                if self.board.board[self.row + i][self.col + j] == ' ':
                    self.board.board[self.row + i][self.col + j] = self.board.space
                    flag = True
                else:
                    f = True
                    continue
                i += kr
                j += kc
        return flag

    def check_move(self, coords):
        row, col = coords
        if (abs(self.row - row) != abs(self.col - col)) or (row == self.row and col == self.col):
            return False
        kr = 1 if row > self.row else -1
        kc = 1 if col > self.col else -1
        i, j = kr, kc
        while 0 <= self.row + i < len(self.board.board) and \
                0 <= self.col + j < len(self.board.board[0]):
            if self.board.board[self.row + i][self.col + j] not in (' ', self.board.space):
                if self.board.board[row][col] not in (' ', self.board.space) and \
                        self.board.board[row][col].color == self.color:
                    return False
                if self.row + i - row:
                    return False
            if self.row + i == row and self.col + j == col:
                break
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

    def __repr__(self):
        if self.walk:
            return "\033[46m!\033[0m"
        if self.option:
            return "\033[36m!"
        if self.color == "white":
            return "\033[37m!"
        if self.color == "black": return "\033[31m!"
