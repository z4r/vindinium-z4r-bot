import re

MOVES = {
    (0, 1): 'East',
    (0, -1): 'West',
    (1, 0): 'South',
    (-1, 0): 'North',
}


class Tile(object):
    PATTERN = NotImplemented
    PASSABLE = NotImplemented

    def __init__(self, x, y, board, rawtile, match):
        self.x = x
        self.y = y
        self.board = board
        self.rawtile = rawtile
        self._match = match

    @classmethod
    def match(cls, token):
        return re.match(cls.PATTERN, token)

    def __repr__(self):
        return repr((self.x, self.y))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __sub__(self, other):
        return MOVES.get((other.x - self.x, other.y - self.y), 'Stay')

    @property
    def neighbors(self):
        for dx, dy in MOVES.keys():
            x, y = self.x + dx, self.y + dy
            if 0 <= x < self.board.size and 0 <= y < self.board.size:
                yield self.board[x][y]


class EmptyTile(Tile):
    PATTERN = r'  '
    PASSABLE = True


class TavernTile(Tile):
    PATTERN = r'\[\]'
    PASSABLE = False


class WallTile(Tile):
    PATTERN = r'##'
    PASSABLE = False


class HeroTile(Tile):
    PATTERN = r'@([0-9])'
    PASSABLE = True

    def __init__(self, x, y, board, rawtile, match):
        super(HeroTile, self).__init__(x, y, board, rawtile, match)
        self.hero = self._match.group(1)


class MineTile(Tile):
    PATTERN = r'\$([-0-9])'
    PASSABLE = False

    def __init__(self, x, y, board, rawtile, match):
        super(MineTile, self).__init__(x, y, board, rawtile, match)
        owner = self._match.group(1)
        self.owner = owner if owner in map(str, range(1, 5)) else None


class Board(object):
    def __init__(self, size):
        self.size = size
        self.tiles = None

    def update(self, tiles):
        self.tiles = [self._parse(index, tile) for index, tile in enumerate(re.findall(r'..', tiles))]

    @property
    def taverns(self):
        return [tile for tile in self.tiles if isinstance(tile, TavernTile)]

    @property
    def mines(self):
        return [tile for tile in self.tiles if isinstance(tile, MineTile)]

    @property
    def heroes(self):
        return [tile for tile in self.tiles if isinstance(tile, HeroTile)]

    def __getitem__(self, item):
        item = item * self.size
        return self.tiles[item:item + self.size]

    def __iter__(self):
        for index in range(self.size):
            yield self[index]

    def __repr__(self):
        return '\n'.join([''.join([repr(y) for y in x]) for x in self])

    def _parse(self, index, rawtile):
        for cls in (EmptyTile, TavernTile, WallTile, MineTile, HeroTile):
            match = cls.match(rawtile)
            if match:
                return cls(index / self.size, index % self.size, self, rawtile, match)

    def printable(self):
        for x in range(self.size):
            buffer = ''
            for y in range(self.size):
                buffer += self[y][x].rawtile
            print buffer


if __name__ == '__main__':
    b = Board(18)
    b.update("##############        ############################        ##############################    ##############################$4    $4############################  @4    ########################  @1##    ##    ####################  []        []  ##################        ####        ####################  $4####$4  ########################  $4####$4  ####################        ####        ##################  []        []  ####################  @2##    ##@3  ########################        ############################$-    $-##############################    ##############################        ############################        ##############")
    #b = Board(4)
    #b.update('  ####    ####      ##          ')
    b.printable()