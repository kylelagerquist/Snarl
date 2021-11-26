# Snarl Remote Adversary

## Description
The remote adversary component was implemented with a remote proxy design pattern, similar to the remote user implementation. The main difference is that a player-client uses the same `LocalPlayer` instance for the entire game, where an adversary-client may switch between a `LocalZombie` and a `LocalGhost` throughout levels. A remote adversary operates in the following way:

1. When an adversary client establishes a TCP connection it immidiately sends the message `"adversary"` to identify itself and differentiate from player-clients 
1. While the server is waiting for the max number of clients to connect to the current game, if an adversary-client connects, it will be assigned to that game.
1. The `GameManager` then stores the socket connection of all the adversary-clients connected to the game.
1. When each level begins the number of zombies and ghosts are as specified in Milestone 8
    1. Zombies are added first, if there are unassigned adversary-clients then they will become zombies. Ghosts are then created with the same process.
    1. If there are less adversaries in the level then there are adversary-clients connected to the game, the extra clients will not be used on that level
    1. If there are more adversaries in the level then there are adversary-clients, the remaining adversaries will be filled by local instances.
***

## Snarl: Remote Protocol Changes
* When the server accepts a new connection, it immediately sends the JSON string `identify` to the client connection
    * If player-client connects to the server, `"client"` is returned
    * If adversary-client connects to the server, `"adversary"` is returned
* If an adversary-client is chosen to be an adversary in the level, a `(declare-adversary)` JSON object is sent
* Before a move is requested, an `(adversary-update-message)` JSON object is sent
* To request a move, the word `"move"` is sent to the remote adversary
* When `"move"` is requested, the adversary client responds with sending an `(adversary-move)` JSON object

A `(declare-adversary)` is the following JSON object:
```ruby
{"type": "declare-adversary",
"adversary-type": (adversary-type),
"name": (adversary-name)
}
```

A `(adversary-type)` is one of:
* "zombie"
* "ghost"

An `(adversary-update-message)`is the following JSON object, same as `(state)`:
```ruby
{"type": "state",
"level": (tile-layout),
"players": (point),
"adversaries": (object-list),
"exit-locked": (actor-position-list)
}
```
***

## Backward Compatibility
The `LocalZombie` and `LocalGhost` are the same implementation as before, however the `RemoteAdversary` class is just used as a wrapper to allow for the local components to connect remotely. The adversaries are added to each level as they were before, the only addition is that if there is a adversary-client connected, a remote adversary is instantiated instead.
***

## Implementaton Changes
* Created adversary_client.py file which is very similar to the `player_client.py` file which is responsible for connecting to server, identifying itself as a remote adversary, and recieving/sending messages to server.
    * The big difference is that `player_client.py` intialized a single `LocalPlayer` to be used the entire session, where the remote client initializes a new `LocalZombie` or `LocalGhost` every time a `(declare-adversary)` is received.
* Altered player_client.py to identify itself as a `"player"` when the server sends a `"identify"` message
* New class remote_adversary.py that implements `AbstractAdversary`
    * This class is almost identical to remote_player.py in which its purpose is to facilite sending and recieving data from the remote client
* Changes to `LocalZombie` and `LocalGhost` where now their `_row` and `_col` are updated when they recieve an updated state
* Change to rule_checker.py so that the adversaries move is checked for validity again, even though stratergy implementation remains unchanged.




