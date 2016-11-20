import abc
import unittest


class TestRunner(unittest.TestCase):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _getJson(self, page, query=None):
        """
        Return JSON content.
        """
        pass

    @abc.abstractmethod
    def _get(self, page, query):
        """
        Return the page content.
        """
        pass


class Tester(unittest.TestCase):
    def _testPageReachable(self, page, query=None):
        self._testResponse(self._get(page, query))

    def _testResponse(self, response):
        self.assertTrue("Traceback (most recent call last):" not in response)


class Pages(Tester):
    def testIndexReachable(self):
        self._testPageReachable('index.cgi')

    def testApiReachable(self):
        self._testPageReachable('api.cgi')

    def testGameReachable(self):
        self._testPageReachable('game.cgi', 'method=view&game=1223308996')

    def testPlayerReachable(self):
        self._testPageReachable('player.cgi', 'player=jrem')

    def testPlayerGamesReachable(self):
        self._testPageReachable('player.cgi', 'player=rc&method=games')

    def testHeadToHeadReachable(self):
        self._testPageReachable('headtohead.cgi', 'player1=jrem&player2=sam')

    def testHeadToHeadGamesReachable(self):
        self._testPageReachable('headtohead.cgi', 'player1=jrem&player2=sam&method=games')

    def testSpeculateReachable(self):
        self._testPageReachable('speculate.cgi')

    def testStatsReachable(self):
        self._testPageReachable('stats.cgi')

    def testHistoricReachable(self):
        self._testPageReachable('historic.cgi')

    def _testResponse(self, response):
        super(Pages, self)._testResponse(response)
        self.assertTrue("<!DOCTYPE html>" in response)


class SpeculatePage(Tester):
    def testAGame(self):
        self._testPageReachable('speculate.cgi', 'redPlayer=tlr&redScore=10&blueScore=0&bluePlayer=cjm&previousGames=')

    def testMultipleGames(self):
        self._testPageReachable('speculate.cgi', 'redPlayer=acas&redScore=10&blueScore=0&bluePlayer=epb&previousGames=tlr%2C10%2C0%2Ccjm%2Cjma%2C10%2C0%2Cmsh')

    def _testResponse(self, response):
        super(SpeculatePage, self)._testResponse(response)
        self.assertTrue("<!DOCTYPE html>" in response)
        self.assertTrue('Speculative Ladder' in response)


class LadderPage(Tester):
    def testRange(self):
        self._testPageReachable('ladder.cgi', 'gamesFrom=1223308996&gamesTo=1223400000')

    def _concat(self, thing):
        return ''.join([l.strip() for l in thing.split('\n')])

    def _testResponse(self, response):
        super(LadderPage, self)._testResponse(response)
        jrem = """
        <td class="ladder-position ladder-first">1</td>
        <td class="ladder-name"><a href="player/jrem/">jrem</a></td>
        <td class="ladder-stat">2</td>
        <td class="ladder-stat">2</td>
        <td class="ladder-stat">0</td>
        <td class="ladder-stat">0</td>
        <td class="ladder-stat">17</td>
        <td class="ladder-stat">3</td>
        <td class="ladder-stat">5.667</td>
        <td class="ladder-stat">0.000</td>
        <td class="ladder-stat ladder-skill">16.503</td>
        """
        jrem = self._concat(jrem)
        response = self._concat(response)
        self.assertFalse("<!DOCTYPE html>" in response)
        self.assertTrue(jrem in response)


class RecentPage(Tester):
    def testReachable(self):
        self._testPageReachable('recent.cgi')


class GamesApi(Tester):
    def assertDictEqualNoHref(self, first, second):
        del(first['red']['href'])
        del(first['blue']['href'])
        del(second['red']['href'])
        del(second['blue']['href'])
        self.maxDiff = None
        self.assertDictEqual(first, second)

    def testPlayerGamesJsonReachable(self):
        response = self._getJson('games.cgi', 'player=rc&limit=0')
        self.assertEqual(len(response), 20)
        self.assertEqual(response[0]['date'], 1278339173)

    def testHeadToHeadGamesJsonReachable(self):
        response = self._getJson('games.cgi', 'player1=jrem&player2=prc&limit=0')
        self.assertEqual(len(response), 11)
        self.assertEqual(response[0]['date'], 1392832399)

    def testRecentJsonReachable(self):
        response = self._getJson('games.cgi')

    def test(self):
        response = self._getJson('games.cgi', 'from=1430402614&to=1430991615')
        self.assertEqual(len(response), 5)
        self.assertEqual(response[0]['date'], 1430402615)
        self.assertDictEqualNoHref(response[0], self._getJson('game.cgi', 'method=view&game=1430402615&view=json'))
        self.assertEqual(response[4]['date'], 1430991614)

    def testLimit(self):
        response = self._getJson('games.cgi', 'from=1430402614&to=1430991615&limit=2')
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]['date'], 1430928939)
        self.assertEqual(response[1]['date'], 1430991614)

    def testDeleted(self):
        response = self._getJson('games.cgi', 'from=1430402614&to=1430991615&includeDeleted=1')
        self.assertEqual(len(response), 6)
        self.assertEqual(response[3]['deleted']['at'], 1430915500)
        self.assertEqual(response[3]['deleted']['by'], 'eu')
        self.assertEqual(response[3]['date'], 1430915499)

    def testNoDeleted(self):
        response = self._getJson('games.cgi', 'from=1430402614&to=1430991615&includeDeleted=0')
        self.assertEqual(len(response), 5)
        self.assertEqual(response[3]['date'], 1430928939)


class PlayerApi(Tester):
    def testPlayerJson(self):
        response = self._getJson('player.cgi', 'player=rc&view=json')
        self.assertEqual(response['name'], "rc")
        self.assertEqual(response['rank'], -1)
        self.assertEqual(response['active'], False)
        self.assertAlmostEqual(response['skill'], 1.21917, 4)
        self.assertAlmostEqual(response['overrated'], 7.96406, 4)
        self.assertEqual(response['total']['for'], 59)
        self.assertEqual(response['total']['against'], 142)
        self.assertEqual(response['total']['games'], 20)
        self.assertEqual(response['total']['wins'], 2)
        self.assertEqual(response['total']['losses'], 16)
        self.assertEqual(response['total']['gamesToday'], 0)


class LadderApi(Tester):
    def testReachable(self):
        response = self._getJson('ladder.cgi', 'view=json')

    def testRange(self):
        response = self._getJson('ladder.cgi', 'gamesFrom=1223308996&gamesTo=1223400000&view=json')
        self.assertEqual(len(response), 3)
        self.assertEqual(response[0]['rank'], 1)
        self.assertEqual(response[0]['name'], 'jrem')
        self.assertAlmostEqual(response[0]['skill'], 16.50273, 4)
        self.assertEqual(response[2]['rank'], 3)
        self.assertEqual(response[2]['name'], 'kjb')
        self.assertEqual(response[2]['skill'], -12.5)


class GameApi(Tester):
    def test(self):
        response = self._getJson('game.cgi', 'method=view&game=1223308996&view=json')
        self.assertEqual(response['red']['name'], 'jrem')
        self.assertEqual(response['red']['href'], '../../player/jrem/json')
        self.assertEqual(response['red']['score'], 10)
        self.assertAlmostEqual(response['red']['skillChange'], 13.00655, 4)
        self.assertEqual(response['red']['rankChange'], 1)
        self.assertEqual(response['red']['newRank'], 3)
        redAchievements = response['red']['achievements']
        self.assertEqual(len(redAchievements), 3)
        self.assertEqual(redAchievements[0]['name'], "Flawless Victory")
        self.assertEqual(redAchievements[0]['description'], "Beat an opponent 10-0")
        self.assertEqual(redAchievements[1]['name'], "Early Bird")
        self.assertEqual(redAchievements[1]['description'], "Play and win the first game of the day")
        self.assertEqual(redAchievements[2]['name'], "Pok&#233;Master")
        self.assertEqual(redAchievements[2]['description'], "Collect all the scores")

        self.assertEqual(response['blue']['name'], 'kjb')
        self.assertEqual(response['blue']['href'], '../../player/kjb/json')
        self.assertEqual(response['blue']['score'], 0)
        self.assertAlmostEqual(response['blue']['skillChange'], -13.00655, 4)
        self.assertEqual(response['blue']['rankChange'], -2)
        self.assertEqual(response['blue']['newRank'], 5)
        blueAchievements = response['blue']['achievements']
        self.assertEqual(len(blueAchievements), 1)
        self.assertEqual(blueAchievements[0]['name'], "The Worst")
        self.assertEqual(blueAchievements[0]['description'], "Go last in the rankings")

        self.assertEqual(response['positionSwap'], True)
        self.assertEqual(response['date'], 1223308996)

    def testDeleted(self):
        response = self._getJson('game.cgi', 'method=view&game=1430915499&view=json')
        self.assertTrue('deleted' in response)
        self.assertEqual(response['deleted']['by'], 'eu')
        self.assertEqual(response['deleted']['at'], 1430915500)
