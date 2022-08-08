from itertools import product
from typing import Counter


DIE_SIDES = 100
SPACES = 10
GOAL = 21
P1 = 6
P2 = 1
POSSIBILITIES = Counter(sum(x) for x in product((1, 2, 3), repeat=3))


class Player:
    def __init__(self, x: int):
        self.x = x
        self.score = 0

    def play_round(self, die: int, mod=DIE_SIDES):
        rolls = [die, (die+1) % mod, (die+2) % mod]
        rollsum = sum(rolls) + 3
        self.x = (self.x + rollsum) % SPACES
        self.score += self.x + 1
        return (die + 3) % mod

    @property
    def is_win(self):
        return self.score >= 1000

class Game:
    def __init__(self, players: list[Player]):
        self.players = players
        self.die = 0
        self.roll_count = 0

    def play_round(self):
        for i, player in enumerate(self.players):
            self.die = player.play_round(self.die)
            self.roll_count += 3
            if player.is_win:
                return player, self.players[i-1]
        return False

    def play_until_win(self):
        while True:
            if result := self.play_round():
                return result

def next_pos(add_n: int, current_pos: int):
    return ((current_pos + add_n - 1) % 10) + 1

def quantum_game(start: int):
    cache: list[tuple[int, int, int, int]] = [(start, 0, 0, 1)]
    wins: dict[int, int] = {}
    losses: dict[int, int] = {}
    while cache:
        item = cache.pop()
        pos, rolls, score, ways = item
        if score >= GOAL:
            wins[rolls] = wins.get(rolls, 0) + ways
            continue
        else:
            losses[rolls] = losses.get(rolls, 0) + ways
        for n, c in POSSIBILITIES.items():
            npos = next_pos(n, pos)
            nscore = score + npos
            nrolls = rolls + 3
            nways = ways * c
            nitem = npos, nrolls, nscore, nways
            cache.append(nitem)
    return wins, losses


def count_wins(p1_wins, p1_losses, p2_wins, p2_losses):
    total_1: int = 0
    total_2: int = 0
    for rolls, ways in p1_wins.items():
        prev_rolls = rolls - 3
        total_1 += (ways * p2_losses.get(prev_rolls, 0))
    for rolls, ways in p2_wins.items():
        total_2 += (ways * p1_losses.get(rolls, 0))
    return total_1, total_2


if __name__ == '__main__':
    player1 = Player(3)
    player2 = Player(7)
    game = Game([player1, player2])
    winner, loser = game.play_until_win()
    print(loser.score * game.roll_count)

    p1_wins, p1_losses = quantum_game(P1)
    p2_wins, p2_losses = quantum_game(P2)
    print(max(count_wins(p1_wins, p1_losses, p2_wins, p2_losses)))
