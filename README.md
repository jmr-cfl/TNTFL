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

### Recent games
`games/recent`

`games/recent/limit/<limit>`

### Player games
`games/player/<playername>/`

### Head to Head games
`games/headtohead/<playername>/<playername>/`

### All Games
`games`

`games/limit/<limit>/`

`games/between/<epoch>/<epoch>/`

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
