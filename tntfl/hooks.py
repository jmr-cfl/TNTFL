import requests
import os
import ConfigParser
import urlparse
import tntfl.constants as Constants


def skillField(playerName, skillChange):
    field = None
    if skillChange > 0:
        field = {
            'title': "{}'s skill".format(playerName),
            'value': '{:+.3f}'.format(skillChange),
            'short': True
        }
    return field


def rankChangeField(playerName, posChange, posAfter):
    field = None
    if posChange != 0:
        field = {
            'title': "{}'s rank".format(playerName),
            'value': '{:+d} ({:d})'.format(posChange, posAfter),
            'short': True
        }
    return field


def publishToSlack(game):
    if os.path.exists(Constants.configFile):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(Constants.configFile, 'r'))

        if config.has_option('mattermost', 'mattermost_url') and config.has_option('mattermost', 'api_key') and config.has_option('mattermost', 'tntfl_url'):
            mattermostUrl = config.get('mattermost', 'mattermost_url')
            apiKey = config.get('mattermost', 'api_key')
            tntflUrl = config.get('mattermost', 'tntfl_url')

            webhookUrl = urlparse.urljoin(urlparse.urljoin(mattermostUrl, '/hooks/'), apiKey)
            gameUrl = '{}/game/{}'.format(tntflUrl, game.time)
            title = '{} {}-{} {}'.format(
                game.redPlayer,
                game.redScore,
                game.blueScore,
                game.bluePlayer,
            )

            message = {
                'attachments': [
                    {
                        'fallback': title,
                        'title': title,
                        'title_link': gameUrl,
                        'fields': [f for f in [
                            skillField(game.bluePlayer, game.skillChangeToBlue),
                            skillField(game.redPlayer, -game.skillChangeToBlue),
                            rankChangeField(game.bluePlayer, game.bluePosChange, game.bluePosAfter),
                            rankChangeField(game.redPlayer, game.redPosChange, game.redPosAfter),
                        ] if f is not None],
                    }
                ],
                'username': 'ScoreBot',
                'icon_url': urlparse.urljoin(mattermostUrl, '/static/emoji/26bd.png'),
            }
            requests.post(webhookUrl, json=message)
