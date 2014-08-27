#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from game import Game
from bot import ZARBot
START_TIMEOUT = 10 * 60
BOT = ZARBot


def arena(arguments):
    for i in range(arguments.games):
        Game().play(
            BOT(),
            '{}/api/{}'.format(arguments.server, 'arena'),
            {'key': arguments.apikey}
        )


def training(arguments):
    params = {
        'key': arguments.apikey,
        'turns': arguments.turns
    }
    if arguments.map:
        params['map'] = 'm{}'.format(arguments.map)
    Game().play(
        BOT(),
        '{}/api/{}'.format(arguments.server, 'training'),
        params
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='vindinium')
    subparsers = parser.add_subparsers(help='game mode')

    training_parser = subparsers.add_parser('training', help='start a training session')
    training_parser.add_argument('-t', '--turns', metavar='#TURNS', help='Number of turns (default: 300)', type=int, default=300)
    training_parser.add_argument('-m', '--map', metavar='MAP', help='Map ID (default: random)', type=int, choices=range(1, 7))
    training_parser.set_defaults(func=training)

    arena_parser = subparsers.add_parser('arena', help='Start an arena session')
    arena_parser.add_argument('-g', '--games', metavar='#GAMES', help='Number of consecutive games (default: 1)', type=int, default=1)
    arena_parser.set_defaults(func=arena)

    parser.add_argument('-k', '--apikey', metavar='APIKEY', help='vindinium apikey (http://vindinium.org/register)', required=True)
    parser.add_argument('-s', '--server', metavar='SERVER', help='Server Host', default='http://vindinium.org')

    args = parser.parse_args()
    args.func(args)
