#!/usr/bin/env python

import cgi
import json
import tntfl.constants as Constants
from tntfl.ladder import TableFootballLadder
import tntfl.template_utils as utils
from tntfl.web import serve_template, getInt, getString
base = ""


def filterGames(game, fromTime, toTime, includeDeleted):
    return (not fromTime or game.time >= fromTime) and (not toTime or game.time <= toTime) and (includeDeleted or not game.isDeleted())


def getGames(ladder, form):
    player = getString('player', form)
    player1 = getString('player1', form)
    player2 = getString('player2', form)

    if player and player in ladder.players:
        # Player
        player = ladder.getPlayer(player)
        games = player.games

    elif player1 and player2 and player1 in ladder.players and player2 in ladder.players:
        # Head to Head
        player1 = ladder.getPlayer(player1)
        player2 = ladder.getPlayer(player2)
        games = utils.getSharedGames(player1, player2)
    else:
        # Games and Recent
        games = ladder.games
    return games


form = cgi.FieldStorage()

ladder = TableFootballLadder(Constants.ladderFilePath)
games = getGames(ladder, form)

fromTime = getInt('from', form)
toTime = getInt('to', form)
includeDeleted = getInt('includeDeleted', form, 0)
limit = getInt('limit', form, 10)
games = [g for g in games if filterGames(g, fromTime, toTime, includeDeleted)]
if limit:
    games = games[-limit:]

print 'Content-Type: application/json'
print
print json.dumps([utils.gameToJson(game, base) for game in games])
