# TNTFL

A Table Football Ladder website.

## API
A JSON API is available for ladder data.

In the JSON returned, links to other resources are represented by an object with an 'href' property. The value of this property is the URI of the linked resource.

### Player Info
`player/<playername>/json`

### Game Info
`game/<gameid>/json`

Where `gameid` is the epoch of when the game was played.

### Game list
`games.cgi`

Returns a list of games. Can be limited to a player or limited to head to head games between two players.

Arguments:

* `player` (optional) specifies the player to return games for.

* `player1` (optional) specifies the first player to return head to head games for.

* `player2` (optional) specifies the second player to return head to head games for.

* `from` (optional) specifies the epoch to start at.

* `to` (optional) specifies the epoch to stop at.

* `includeDeleted` (optional) specifies whether to include deleted games. Can be 0 or 1, defaults to 0.

* `limit` (optional) specifies the maximum number of games to return. Defaults to 10.

Examples:

* `games.cgi?player=<player>&from=<time>&to=<time>`

* `games.cgi?player1=<player>&player2=<player>&limit=100`

### Add Game
`game/add/json` (POST)

Request should be a POST containing the following fields:

* `redPlayer`

* `redScore`

* `bluePlayer`

* `blueScore`

Returns a game resource representing the added game.

### Ladder
`ladder/json`

Arguments:

* `gamesFrom` (optional) epoch to start at

* `gamesTo` (optional) epoch to end at

Specifying `gamesFrom` and `gamesTo` calculates a ladder for the given time range.
