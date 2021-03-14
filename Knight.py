class Knight:
    def __init__(self, board, coords, color):
        self.board = board
        self.row, self.col = coords
        self.color = color
        self.option = False
        self.walk = False

    def move_options(self):
        flag = False
        for i in (2, -2):
            for j in (1, -1):
                if 0 <= self.row + i < len(self.board.board) and \
                        0 <= self.col + j < len(self.board.board[0]):
                    if self.board.board[self.row + i][self.col + j] == ' ':
                        self.board.board[self.row + i][self.col + j] = self.board.space
                        flag = True
                    elif self.board.board[self.row + i][self.col + j].color != self.color:
                        self.board.board[self.row + i][self.col + j].option = flag = True
                if 0 <= self.row + j < len(self.board.board) and \
                        0 <= self.col + i < len(self.board.board[0]):
                    if self.board.board[self.row + j][self.col + i] == ' ':
                        self.board.board[self.row + j][self.col + i] = self.board.space
                        flag = True
                    elif self.board.board[self.row + j][self.col + i].color != self.color:
                        self.board.board[self.row + j][self.col + i].option = flag = True
        return flag

    def check_move(self, coords):
        row, col = coords
        if (self.row - row in (2, -2) and self.col - col in (1, -1)) or \
                (self.row - row in (1, -1) and self.col - col in (2, -2)):
            if self.board.board[row][col] not in (' ', self.board.space):
                if self.board.board[row][col].color == self.color:
                    return False
            return True
        return False

    def move(self, coords):
        row, col = coords
        if not self.check_move(coords):
            return False
        self.board.board[self.row][self.col] = ' '
        self.board.board[row][col] = self
        self.row, self.col = row, col
        return True

    def __repr__(self):
        if self.option:
            return "\033[36m?"
        if self.color == "white":
            return "\033[37m?"
        if self.color == "black":
            return "\033[31m?"
