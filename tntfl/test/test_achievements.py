import os
import unittest
from tntfl.player import Player
from tntfl.game import Game
from tntfl.ladder import TableFootballLadder
from tntfl.achievements import *

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def addGame(red, redScore, blue, blueScore, time, skillChangeToBlue=0):
    game = Game(red.name, redScore, blue.name, blueScore, time)
    game.skillChangeToBlue = skillChangeToBlue
    red.game(game)
    blue.game(game)
    return game


class TestAgainstTheOdds(unittest.TestCase):
    def testUnder50(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 49
        game = addGame(player, 10, opponent, 0, 0, -50)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testUnder50_2(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 49
        game = addGame(opponent, 0, player, 10, 0, 10)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testOver50Lose(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 50
        game = addGame(player, 0, opponent, 10, 0, 50)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testOver50(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("baz")
        opponent.elo = 50
        game = addGame(player, 10, opponent, 0, 0, -50)
        result = ach.applies(player, game, opponent, None)
        self.assertTrue(result)

    def testOver50_2(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("baz")
        opponent.elo = 50
        game = addGame(opponent, 0, player, 10, 0, 10)
        result = ach.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestAgainstAllOdds(unittest.TestCase):
    def testUnder100(self):
        ach = AgainstAllOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 99
        game = addGame(player, 10, opponent, 0, 0, -50)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testOver100(self):
        ach = AgainstAllOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 100
        game = addGame(player, 10, opponent, 0, 0, -1)
        result = ach.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestUnstable(unittest.TestCase):
    def test(self):
        sut = Unstable()
        player = Player("foo")
        opponent = Player("bar")

        game = addGame(player, 5, opponent, 5, 0, -5)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

        game = addGame(player, 10, opponent, 0, 0, -5)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

        game = addGame(player, 0, opponent, 10, 1, 5)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertTrue(result)

        game = addGame(player, 0, opponent, 10, 1, 5)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestUpUpAndAway(unittest.TestCase):
    def test(self):
        sut = UpUpAndAway()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(7):
            game = addGame(player, 6, opponent, 4, i, -1)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
            result = sut.applies(opponent, game, player, None)
            self.assertFalse(result)

        game = addGame(player, 6, opponent, 4, 8, -1)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

    def testNonContiguous(self):
        sut = UpUpAndAway()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(7):
            game = addGame(player, 6, opponent, 4, i, -1)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
            result = sut.applies(opponent, game, player, None)
            self.assertFalse(result)

        game = addGame(player, 4, opponent, 6, 8, 1)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

        game = addGame(player, 6, opponent, 4, 9, -1)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestComrades(unittest.TestCase):
    def test(self):
        sut = Comrades()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 99):
            game = addGame(player, 5, opponent, 5, 0)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
            result = sut.applies(opponent, game, player, None)
            self.assertFalse(result)

        game = addGame(player, 5, opponent, 5, 0)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertTrue(result)

        game = addGame(player, 5, opponent, 5, 0)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestDedication(unittest.TestCase):
    def test(self):
        sut = Dedication()
        player = Player("foo")
        opponent = Player("bar")
        timeBetweenGames = 60 * 60 * 24 * 59
        for i in range(0, 7):
            game = addGame(player, 5, opponent, 5, i * timeBetweenGames)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 5, opponent, 5, 7 * timeBetweenGames)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestPokeMaster(unittest.TestCase):
    def test(self):
        sut = PokeMaster()
        player = Player("foo")
        opponent = Player("bar")
        game = addGame(player, 0, opponent, 10, 0)
        for i in range(0, 10):
            game = addGame(player, i, opponent, 10 - i, i)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 10, opponent, 0, 10)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestTheDominator(unittest.TestCase):
    def test(self):
        sut = TheDominator()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 9):
            game = addGame(player, 10, opponent, 0, i, -1)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)

        baz = Player("baz")
        game = addGame(player, 10, baz, 0, 9, -1)
        result = sut.applies(player, game, baz, None)
        self.assertFalse(result)

        game = addGame(player, 10, opponent, 0, 10, -1)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

    def testSwapSides(self):
        sut = TheDominator()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 9):
            game = addGame(player, 10, opponent, 0, i, -1)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)

        baz = Player("baz")
        game = addGame(player, 10, baz, 0, 9, -1)
        result = sut.applies(player, game, baz, None)
        self.assertFalse(result)

        game = addGame(opponent, 0, player, 10, 10, 1)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

    def testInterrupted(self):
        sut = TheDominator()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 9):
            game = addGame(player, 10, opponent, 0, i, -1)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)

        baz = Player("baz")
        game = addGame(player, 10, baz, 0, 9, -1)
        result = sut.applies(player, game, baz, None)
        self.assertFalse(result)

        game = addGame(player, 0, opponent, 10, 10, -1)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestConsistency(unittest.TestCase):
    def test(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = addGame(player, 2, opponent, 8, i)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 2, opponent, 8, 4)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)

    def testInterrupted(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = addGame(player, 2, opponent, 8, i)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 3, opponent, 7, 4)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        game = addGame(player, 2, opponent, 8, 5)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testCont(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = addGame(player, 2, opponent, 8, i)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 2, opponent, 8, 4)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        game = addGame(player, 2, opponent, 8, 5)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testTwice(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = addGame(player, 2, opponent, 8, i)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 2, opponent, 8, 4)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)

        for i in range(5, 9):
            game = addGame(player, 2, opponent, 8, i)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = addGame(player, 2, opponent, 8, 9)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestEarlyBird(unittest.TestCase):
    def test(self):
        ladder = TableFootballLadder(os.path.join(__location__, "testLadder.txt"), False)
        player = Player("foo")
        opponent = Player("baz")
        game = addGame(opponent, 0, player, 10, 6000000003)
        ladder.addGame(game)

        sut = EarlyBird()
        result = sut.applies(player, game, opponent, ladder)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, ladder)
        self.assertFalse(result)

    def testFirstGame(self):
        ladder = TableFootballLadder(os.path.join(__location__, "emptyLadder.txt"), False)
        player = Player("foo")
        opponent = Player("baz")
        game = addGame(opponent, 0, player, 10, 0)
        ladder.addGame(game)

        sut = EarlyBird()
        result = sut.applies(player, game, opponent, ladder)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, ladder)
        self.assertFalse(result)