DIE_SIDES = 100
SPACES = 10

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

# p1 = Player(5)
# p2 = Player(0)
p1 = Player(3)
p2 = Player(7)
game = Game([p1, p2])
winner, loser = game.play_until_win()
print(loser.score)
print(game.roll_count)
print(loser.score * game.roll_count)
