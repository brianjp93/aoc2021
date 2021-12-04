from pathlib import Path
with Path(Path(__file__).parent, 'data').open() as f:
    raw = f.read().strip()
    data = [x.strip() for x in raw.split('\n')]

called = [int(x) for x in data[0].split(',')]


class Board:
    def __init__(self, board):
        self.max_x = 0
        self.max_y = 0
        self.board = self.get_board(board)
        self.marked = set()
        self.last_called = None

    def get_board(self, board):
        board_dict = {}
        for y, line in enumerate(board.split('\n')):
            self.max_y = max(y + 1, self.max_y)
            for x, n in enumerate(line.split()):
                self.max_x = max(x + 1, self.max_x)
                board_dict[(x, y)] = int(n)
        return board_dict

    def get_score(self):
        assert self.last_called
        return sum(y for x, y in self.board.items() if x not in self.marked) * self.last_called

    def mark_number(self, find_n: int):
        self.last_called = find_n
        for coord, n in self.board.items():
            if n == find_n:
                self.marked.add(coord)

    def is_winner(self):
        return self.check_rows() or self.check_columns()

    def check_columns(self):
        assert self.max_x
        assert self.max_y
        for x in range(self.max_x):
            is_winner = True
            for y in range(self.max_y):
                if (x, y) not in self.marked:
                    is_winner = False
            if is_winner:
                return True
        return False

    def check_rows(self):
        assert self.max_x
        assert self.max_y
        for y in range(self.max_y):
            is_winner = True
            for x in range(self.max_x):
                if (x, y) not in self.marked:
                    is_winner = False
            if is_winner:
                return True
        return False


def get_boards():
    boards: list[Board] = []
    for chunk in raw.split('\n\n')[1:]:
        b = Board(chunk)
        boards.append(b)
    return boards

def find_winner() -> Board | None:
    boards = get_boards()
    for n in called:
        for b in boards:
            b.mark_number(n)
            if b.is_winner():
                return b

def find_last_board():
    boards = get_boards()
    not_win = {i for i in range(len(boards))}
    for n in called:
        for i, b in enumerate(boards):
            if i in not_win:
                b.mark_number(n)
                if b.is_winner():
                    if len(not_win) == 1:
                        return b
                    not_win.remove(i)


b = find_winner()
assert b
print(b.get_score())

b = find_last_board()
assert b
print(b.get_score())
