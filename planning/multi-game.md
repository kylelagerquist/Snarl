# Multi-Game Snarl Server

## Clients Joining
The new server waits indefinitely for the first client to join. After this, the server waits for clients to join until either the max clients (specified by `--clients`) join, or there is longer than a `N` (specified by `--wait`) seconds wait after a client connects. Once either these conditions are met, the server creates a new thread to instantiate the GameManager object, register the clients, and begin the game.

After the new thread is created, the server returns to waiting indefinitely for a client to join and repeats the aforementioned process.

If a thread errors, then that game is forfieted and the other games and server continue running. The server runs until all games specified by `--games` are completed.
***

## Use of Threading
Pythons `threading` module is used to be able run a multi-threaded server. Each GameManager is generated on its own thread so multiple games can run concurrently and independently of one another. If one game ends there is no impact on the rest of the games being played.
***

## Storing Names and Leaderboard
In order for there to be a sever-wide leaderboard, there needed to be way to track all players scores. When the server is ran, a new JSON file called `server_log.json` is created with fields to store player names and player-score JSONs. 

Everytime a player is registered in a GameManager, the `server_log` file is read to parse what names already are in use across the server. The client will then be continuously asked to provide a name until their name is unique across the entire server. Their name is then added to the `server_log.json` 

Everytime a game is completed (all players ejected from level or last level completed successfully), all of the player's player-score JSON objects are added to `server_log.json` and all player-score JSON objects from the file are then sent to the client to render the server's leaderboard.

Because names are unique across the server, each player will know exactly where they stand on the leaderboard
***

## Snarl: Remote Protocol Changes
As in the protocol, when a game of Snarl ends, an `(end-game)` JSON object is sent to each client in the game. Now, immediately after these are sent, a new `(server-scores)` JSON object is sent to each client in the game. This is necessary to provide leaderboard updates for all players that have completed games on the server.

A `(server-scores) `is the following JSON object:
```ruby
{ "type": "server-scores",
"scores": (player-score-list)
}
```
A `(player-score-list)` is a JSON array of `(player-score)`, as in the initial protocol.
***

## Implementation 
* The server file, `server.py`, was updated to wrap logic for the `run()` function in a loop so that instead of creating one GameManager after players joined, a new thread is created for the GameManager.
    * The server will continue to accept client connections and beginning new games until the max games specified by `--games` have been reached
* The client file, player_client.py, was updated for `run()` to handle the `(server-scores)` JSON object.
* The game manager file, game_manager.py, was updated so that the `register_user(user: AbstractPlayer)` function checks if the provided name is unique and adds to `server_log.json` if so. Also, `send_end_game()` was updated to write all the player scores to the log, and read in the server-wide scores to send the `(server-scores` object.



