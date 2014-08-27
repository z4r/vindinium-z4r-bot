import requests
from board import Board
from hero import HeroManager


class Game(object):
    START_TIMEOUT = 10 * 60
    MOVE_TIMEOUT = 15

    def __init__(self):
        self.session = requests.session()

    def play(self, bot, url, params):
        state = self.next(url, params, self.START_TIMEOUT)
        heroes = HeroManager(state['hero']['id'], state['game']['heroes'])
        board = Board(state['game']['board']['size'])
        print('ELO: {}'.format(state['hero']['elo']), state['viewUrl'])
        while not state['game']['finished']:
            board.update(state['game']['board']['tiles'])
            heroes.update(board, state['game']['heroes'])
            direction = bot.move(board, heroes)
            try:
                state = self.next(state['playUrl'], {'dir': direction}, self.MOVE_TIMEOUT)
            except requests.RequestException as e:
                print e
                state['game']['finished'] = True

        self.session.close()

    def next(self, url, params, timeout):
        response = self.session.post(url, params, timeout=timeout)
        response.raise_for_status()
        return response.json()
