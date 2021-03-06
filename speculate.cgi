#!/usr/bin/env python

import cgi
from time import time
from tntfl.game import Game
from tntfl.web import serve_template, getInt


def deserialise(serialisedGames):
    gameParts = serialisedGames.split(',')
    games = []
    now = time()
    numGames = len(gameParts) / 4
    for i in range(0, numGames):
        g = Game(gameParts[4 * i].lower(), gameParts[4 * i + 1], gameParts[4 * i + 3].lower(), gameParts[4 * i + 2], now - (numGames - i))
        games.append(g)
    return games


form = cgi.FieldStorage()
speculativeGames = deserialise(form.getfirst('previousGames', ''))

serve_template(
    'speculate.mako',
    speculativeGames=speculativeGames,
    showInactive=getInt('showInactive', form, 0),
    includePlayers=getInt('players', form, 0),
)
