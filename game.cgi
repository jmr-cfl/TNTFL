#!/usr/bin/env python

import cgi
import tntfl.constants as Constants
from tntfl.ladder import TableFootballLadder
from tntfl.caching_game_store import CachingGameStore
import tntfl.transforms.transforms as PresetTransforms
from tntfl.web import redirect_302, fail_400, fail_404, serve_template, getInt, getString
from tntfl.hooks.addGame import do

form = cgi.FieldStorage()

if getString('method', form) == "add":
    redPlayer = getString('redPlayer', form)
    bluePlayer = getString('bluePlayer', form)
    redScore = getInt('redScore', form)
    blueScore = getInt('blueScore', form)
    if redPlayer is not None and bluePlayer is not None and redScore is not None and blueScore is not None and redPlayer != bluePlayer:
        ladder = TableFootballLadder(Constants.ladderFilePath, games=[], postGameHooks=[do])
        ladder._gameStore = CachingGameStore(Constants.ladderFilePath, False)
        newGameTime = ladder.appendGame(redPlayer, redScore, bluePlayer, blueScore)
        if getString('view', form) == 'json':
            # Invalidated, regenerate
            # Tablet doesn't display achievements
            ladder = TableFootballLadder(Constants.ladderFilePath, transforms=PresetTransforms.transforms_for_recent())
            game = ladder.games[-1]
            serve_template("game.mako", game=game, ladder=ladder)
        else:
            redirect_302("../%.0f" % newGameTime)
    else:
        fail_400()
else:
    gameTime = getInt('game', form)
    if gameTime is not None:
        try:
            ladder = TableFootballLadder(Constants.ladderFilePath)
            game = next(g for g in ladder.games if g.time == gameTime)
            serve_template("game.mako", game=game, ladder=ladder)
        except StopIteration:
            fail_404()
    else:
        fail_400()
