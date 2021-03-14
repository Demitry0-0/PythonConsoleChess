class King:
    def __init__(self, board, coords, color):
        self.board = board
        self.row, self.col = self.coords = coords
        self.color = color
        self.first = True
        self.k = -1 if not self.board.reverse and color == 'white' else 1
        self.option = False
        self.shah = False

    def move_options(self):
        size = (len(self.board.board), len(self.board.board[0]))
        flag = False
        self.board.board[self.row][self.col] = ' '
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == j == 0:
                    continue
                if 0 <= self.row + i < size[0] and 0 <= self.col + j < size[1]:
                    r, c = self.row + i, self.col + j
                    '''if self.board.board[r][c] in (' ', self.board.space):
                        self.board.board[r][c] = self
                        if self.check_shah((r, c)):
                            self.board.board[r][c] = self.board.space
                            flag = True
                        else:
                            self.board.board[r][c] = ' '
                    elif self.board.board[r][c].color != self.color:
                        space = self.board.board[r][c]
                        self.board.board[r][c] = self
                        if self.check_shah((r, c)):
                            space.option = flag = True
                        self.board.board[r][c] = space'''
                    if self.board.board[r][c] in (' ', self.board.space) or \
                            self.board.board[r][c].color != self.color:
                        space = self.board.board[r][c]
                        self.board.board[r][c] = self
                        if not self.check_shah((r, c)):
                            if space in (' ', self.board.space):
                                space = self.board.space
                            else:
                                space.option = True
                            flag = True
                        self.board.board[r][c] = space
        self.board.board[self.row][self.col] = self
        if self.first and not self.shah:
            for k in (-1, 1):
                f = True
                for i in range(1, size[1]):
                    if not (0 < self.col + k * i < size[1] - 1):
                        break
                    if self.board.board[self.row][self.col + k * i] in (self.board.space, ' '):
                        continue
                    f = False
                    break
                if f and self.board.board[self.row][self.col + k] == self.board.space:
                    if '#' in str(self.board.board[self.row][self.col + k * i]):
                        if self.board.board[self.row][self.col + k * i].first:
                            self.board.board[self.row][self.col + k * 2] = self
                            if not self.check_shah((self.row, self.col + k * 2)):
                                self.board.board[self.row][self.col + k * 2] = self.board.space
                            else:
                                self.board.board[self.row][self.col + k * 2] = ' '

        return flag

    def check_move(self, coords):
        row, col = coords
        if abs(self.row - row) > 1 or abs(self.col - col) > 2:
            return False
        if self.board.board[row][col] == self.board.space or self.board.board[row][col].option:
            return True
        return False

    def check_shah(self, coords):
        row, col = coords
        size = (len(self.board.board), len(self.board.board[0]))
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                k = 1
                while True:
                    if i == j == 0:
                        break
                    r, c = row + k * i, col + k * j
                    if not (0 <= r < size[0] and 0 <= c < size[1]):
                        break
                    if self.board.board[r][c] not in (' ', self.board.space):
                        if self.board.board[r][c].color != self.color:
                            if self.board.board[r][c].check_move((row, col)):  # (6, 4)
                                return True
                        break
                    k += 1
        for i in (-2, 2):
            for j in (-1, 1):
                if 0 <= row + i < size[0] and 0 <= col + j < size[1]:
                    r, c = row + i, col + j
                    if self.board.board[r][c] != ' ' and self.board.board[r][c] != self.board.space:
                        if self.board.board[r][c].color != self.color and \
                                '?' in str(self.board.board[r][c]):
                            return True
        return False

    def move(self, coords):
        row, col = coords
        if not self.check_move(coords):
            return False
        if abs(col - self.col) == 2:
            if col > self.col:
                self.board.board[row][-1].move((self.row, self.col + 1))
            elif col < self.col:
                self.board.board[row][0].move((self.row, self.col - 1))
        self.board.board[self.row][self.col] = ' '
        self.board.board[row][col] = self
        self.row, self.col = self.coords = row, col
        self.first = False
        return True

    def __repr__(self):
        if self.option:
            return "\033[36m$"
        if self.color == "white":
            return "\033[37m$"
        if self.color == "black":
            return "\033[31m$"
