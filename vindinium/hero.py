class HeroManager(object):
    def __init__(self, player_id, heroes):
        self.heroes = {}
        for hero in heroes:
            self.heroes[hero['id']] = Hero(hero['name'])
        self.player = self.heroes[player_id]

    def update(self, board, heroes):
        for hero in heroes:
            self.heroes[hero['id']].update(
                board[hero['pos']['x']][hero['pos']['y']],
                hero['life'],
                hero['gold'],
                hero['mineCount'],
            )

    def is_player(self, hid):
        return self.heroes.get(int(hid or 0)) == self.player

    def __getitem__(self, item):
        return self.heroes[int(item)]


class Hero(object):
    def __init__(self, name):
        self.name = name
        self.tile = None
        self.life = None
        self.gold = None
        self.mines = None

    def update(self, tile, life, gold, mines):
        self.tile = tile
        self.life = life
        self.gold = gold
        self.mines = mines