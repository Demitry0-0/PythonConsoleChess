class Pawn:
    def __init__(self, board, coords, color):
        self.board = board
        self.row, self.col = coords
        self.color = color
        self.first = True
        self.k = -1 if not self.board.reverse and color == 'white' else 1
        self.option = False

    def move_options(self):
        # Δ
        row, col = self.row, self.col
        # print(row, col)
        flag = False
        if self.board.board[row + self.k][col] == ' ':
            self.board.board[row + self.k][col] = "\033[36mΔ"
            flag = True
            if self.first and self.board.board[row + self.k * 2][col] == ' ':
                self.board.board[row + self.k * 2][col] = "\033[36mΔ"
        if 0 <= row + self.k < len(self.board.board):
            row += self.k
            if 0 <= col + 1 < len(self.board.board[0]) and self.board.board[row][col + 1] != ' ':
                if self.board.board[row][col + 1].color != self.color:
                    self.board.board[row][col + 1].option = falg = True
            if 0 <= col - 1 < len(self.board.board[0]) and self.board.board[row][col - 1] != ' ':
                if self.board.board[row][col - 1].color != self.color:
                    self.board.board[row][col - 1].option = flag = True
        return flag

    def check_move(self, coords):
        row, col = coords
        if self.first and not (2 >= self.k * (row - self.row) >= 1):
            return False
        elif not self.first and self.k * (row - self.row) != 1:
            return False
        if 1 < abs(col - self.col):
            return False
        if abs(col - self.col) == 1 and (self.board.board[row][col] == ' ' or
                                         self.board.board[row][col].color == self.color):
            return False
        if self.first:
            self.first = False
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
        if self.option:
            return "\033[36m*"
        if self.color == "white":
            return "\033[37m*"
        if self.color == "black":
            return "\033[31m*"
