from Queue import PriorityQueue, Empty
from multiprocessing import TimeoutError
from astar import AStar, GridState
from board import HeroTile, MineTile, TavernTile
from multiprocessing.pool import ThreadPool
from collections import defaultdict


class Bot(object):
    def __init__(self):
        self.board = None
        self.heroes = None
        self.pool = ThreadPool(processes=1)

    def move(self, board, heroes):
        self.board = board
        self.heroes = heroes
        try:
            return self.pool.apply_async(self._move).get(timeout=1)
        except (Empty, TimeoutError):
            return 'Stay'

    def _move(self):
        raise NotImplementedError


class ScoreBoard(PriorityQueue):
    def add(self, score, path):
        self.put((100 - score, path))


class ZARBot(Bot):
    def _path(self, location):
        return AStar(GridState(self.heroes.player.tile, goal=location)).solve()

    def _move(self):
        scores = ScoreBoard()

        locations = []
        locations.extend(self.board.taverns)
        if self.heroes.player.life > 20:
            locations.extend(hero for hero in self.board.heroes if not self.heroes.is_player(hero.hero))
            locations.extend(mine for mine in self.board.mines if not self.heroes.is_player(mine.owner))

        for location in locations:
            path = self._path(location)
            if path:
                score = self._evaluate(path)
                scores.add(score, path)

        #for p, s in sorted(scores.queue):
        #    print '{}\t{}\t{}'.format(s[-1].rawtile, 100 - p, s)

        _, path = scores.get(False)
        return path[0] - path[1]

    def _evaluate(self, path):
        def hero_function():
            hero = self.heroes[path[-1].hero]
            if self.heroes.player.life <= hero.life:
                return 0
            if not hero.mines:
                return 0
            return self.heroes.player.life / (len(path) - 1)

        def tavern_function():
            return (100 - self.heroes.player.life) / (len(path) - 1)

        def mine_function():
            return self.heroes.player.life / (len(path) - 1)

        score_functions = defaultdict(lambda: lambda: 0)
        score_functions[MineTile] = mine_function
        score_functions[HeroTile] = hero_function
        score_functions[TavernTile] = tavern_function
        return score_functions[type(path[-1])]()

if __name__ == '__main__':
    from json import load
    from board import Board
    from hero import HeroManager

    with open('../fakestate.json') as fp:
        state = load(fp)
        h = HeroManager(state['hero']['id'], state['game']['heroes'])
        b = Board(state['game']['board']['size'])
        b.update(state['game']['board']['tiles'])
        h.update(b, state['game']['heroes'])
        print ZARBot().move(b, h)
