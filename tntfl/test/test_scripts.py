import json
import os
import shutil
import subprocess
import tntfl.test.shared_get as Get


class Deployment(Get.TestRunner):
    def setUp(self):
        if 'QUERY_STRING' in os.environ:
            del(os.environ['QUERY_STRING'])

        if os.path.exists('ladder.txt'):
            os.rename('ladder.txt', 'ladder.actual')
        shutil.copyfile(os.path.join('tntfl', 'test', 'jrem.ladder'), 'ladder.txt')

    def tearDown(self):
        if os.path.exists('ladder.txt'):
            os.remove('ladder.txt')
        if os.path.exists('ladder.actual'):
            os.rename('ladder.actual', 'ladder.txt')

    def _getJson(self, page, query=None):
        response = self._get(page, query)
        # Strip content type
        response = ''.join(response.split('\n')[2:])
        self.assertTrue(len(response) > 0)
        return json.loads(response)

    def _page(self, page):
        return os.path.join(os.getcwd(), page)

    def _get(self, page, query):
        self._setQuery(query)
        return subprocess.check_output(['python', self._page(page)])

    def _setQuery(self, query):
        if query is not None:
            os.environ['QUERY_STRING'] = query


class AddGame(Get.Tester, Deployment):
    def testAddGame(self):
        self._testPageReachable('game.cgi', 'method=add&redPlayer=foo&redScore=5&bluePlayer=bar&blueScore=5')

    def testAddGameApi(self):
        self._testPageReachable('game.cgi', 'method=add&view=json&redPlayer=foo&redScore=5&bluePlayer=bar&blueScore=5')


class Pages(Get.Pages, Deployment):
    pass


class SpeculatePage(Get.SpeculatePage, Deployment):
    pass


class LadderPage(Get.LadderPage, Deployment):
    pass


class RecentPage(Get.RecentPage, Deployment):
    pass


class GamesApi(Get.GamesApi, Deployment):
    pass


class LegacyPlayerApi(Get.LegacyPlayerApi, Deployment):
    pass


class LegacyHeadToHeadApi(Get.LegacyHeadToHeadApi, Deployment):
    pass


class LegacyRecentApi(Get.LegacyRecentApi, Deployment):
    pass


class LegacyLadderApi(Get.LegacyLadderApi, Deployment):
    pass


class LegacyGameApi(Get.LegacyGameApi, Deployment):
    pass


class LegacyGamesApi(Get.LegacyGamesApi, Deployment):
    pass
