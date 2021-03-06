from collections import OrderedDict
from datetime import date, datetime, timedelta
from tntfl.player import PerPlayerStat
from tntfl.achievements import Achievement


def getSharedGames(player1, player2):
    return [g for g in player1.games if g.redPlayer == player2.name or g.bluePlayer == player2.name]


def isPositionSwap(game):
    bluePosBefore = game.bluePosAfter + game.bluePosChange
    redPosBefore = game.redPosAfter + game.redPosChange
    positionSwap = False
    if bluePosBefore > 0 and redPosBefore > 0:
        if bluePosBefore == game.redPosAfter or redPosBefore == game.bluePosAfter:
            positionSwap = True
    return positionSwap


def playerHref(base, name):
    return base + 'player/' + name + '/json'


def gameToJson(game, base):
    asJson = {
        'red': {
            'name': game.redPlayer,
            'href': playerHref(base, game.redPlayer),
            'score': game.redScore,
            'skillChange': -game.skillChangeToBlue,
            'rankChange': game.redPosChange,
            'newRank': game.redPosAfter,
            'achievements': [{'name': a.name, 'description': a.description} for a in game.redAchievements],
        },
        'blue': {
            'name': game.bluePlayer,
            'href': playerHref(base, game.bluePlayer),
            'score': game.blueScore,
            'skillChange': game.skillChangeToBlue,
            'rankChange': game.bluePosChange,
            'newRank': game.bluePosAfter,
            'achievements': [{'name': a.name, 'description': a.description} for a in game.blueAchievements],
        },
        'positionSwap': isPositionSwap(game),
        'date': game.time,
    }
    if game.isDeleted():
        asJson['deleted'] = {
            'at': game.deletedAt,
            'by': game.deletedBy
        }
    return asJson


def getTrendWithDates(player):
    trend = []
    games = player.games[-10:] if len(player.games) >= 10 else player.games
    skill = 0
    for i, game in enumerate(games):
        skill += game.skillChangeToBlue if game.bluePlayer == player.name else -game.skillChangeToBlue
        trend.append((game.time, skill))
    return trend


def ladderToJson(players, ladder, base, includePlayers):
    if includePlayers:
        return [{
            'rank': ladder.getPlayerRank(p.name),
            'name': p.name,
            'player': playerToJson(p, ladder),
            'trend': getTrendWithDates(p),
        } for i, p in enumerate(players)]
    else:
        return [{'rank': i + 1, 'name': p.name, 'skill': p.elo, 'href': playerHref(base, p.name)} for i, p in enumerate(players)]


def playerToJson(player, ladder):
    return {
        'name': player.name,
        'rank': ladder.getPlayerRank(player.name),
        'active': ladder.isPlayerActive(player),
        'skill': player.elo,
        'overrated': player.overrated(),
        'total': {
            'for': player.goalsFor,
            'against': player.goalsAgainst,
            'games': len(player.games),
            'gamesAsRed': player.gamesAsRed,
            'wins': player.wins,
            'losses': player.losses,
            'gamesToday': player.gamesToday,
        },
        'games': {'href': 'games/json'},
    }


def getPerPlayerStats(player):
    pps = {}
    for game in player.games:
        if game.redPlayer == player.name:
            if game.bluePlayer not in pps:
                pps[game.bluePlayer] = PerPlayerStat(game.bluePlayer)
            pps[game.bluePlayer].append(game.redScore, game.blueScore, -game.skillChangeToBlue)
        elif game.bluePlayer == player.name:
            if game.redPlayer not in pps:
                pps[game.redPlayer] = PerPlayerStat(game.redPlayer)
            pps[game.redPlayer].append(game.blueScore, game.redScore, game.skillChangeToBlue)
    return pps


def perPlayerStatsToJson(stats):
    return [{
        'opponent': opponent,
        'skillChange': stats[opponent].skillChange,
        'for': stats[opponent].goalsFor,
        'against': stats[opponent].goalsAgainst,
        'games': stats[opponent].games,
        'wins': stats[opponent].wins,
        'losses': stats[opponent].losses,
    } for opponent in stats.keys()]


def getPlayerAchievementsJson(player):
    achievements = [{
        'name': a.name,
        'description': a.description,
        'time': player.achievements[a]
    } for a in player.achievements.keys()]
    [achievements.append({
        'name': clz.name,
        'description': clz.description,
    }) for clz in Achievement.__subclasses__() if clz not in player.achievements.keys()]
    return achievements


def appendChristmas(links, base):
    if datetime.now().month == 12:
        links.append('<link href="%scss/christmas.css" rel="stylesheet">' % base)
    return links


def getGamesPerDay(games):
    if len(games) == 0:
        return []
    gamesPerDay = [[date.fromtimestamp(games[0].time).strftime('%s'), 0]]
    for game in games:
        day = date.fromtimestamp(game.time).strftime('%s')
        if gamesPerDay[-1][0] != day:
            gamesPerDay.append([day, 0])
        gamesPerDay[-1][1] += 1
    return gamesPerDay


def getStatsJson(ladder, base):
    winningStreak = ladder.getStreaks()['win']
    mostSignificantGames = sorted([g for g in ladder.games if not g.isDeleted()], key=lambda x: abs(x.skillChangeToBlue), reverse=True)
    return {
        'totals': {
            'games': len(ladder.games),
            'players': len(ladder.players),
            'activePlayers': ladder.getNumActivePlayers(),
            'achievements': [[{
                'name': a.name,
                'description': a.description,
            }, c] for a, c in sorted(ladder.getAchievements().iteritems(), reverse=True, key=lambda t: t[1])],
        },
        'records': {
            'winningStreak': {
                'player': winningStreak['player'].name,
                'count': winningStreak['streak'].count,
            },
            'mostSignificant': [gameToJson(g, base) for g in mostSignificantGames[0:5]],
            'leastSignificant': [gameToJson(g, base) for g in reversed(mostSignificantGames[-5:])],
        },
        'gamesPerDay': getGamesPerDay(ladder.games),
    }
