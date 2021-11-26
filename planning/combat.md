# Combat System

## Description
* All players in the game now begin each level with 100 health points. 
* Upon contact with an adversary, the player is no longer ejected from the level.
* Instead, each adversary type has a predetermined amount of damage they can inflict, and upon contact with a player the player's health will be reduced by the damage amount. 
* If the player's health falls below 0, they are ejected from the level. 
* At the beginning of each level, each player's health resets to 100.
* Player moves onto an adversary on their turn:
    * If the adversary inflicts enough damage to eject them, they are ejected.
    * If not, their health is reduced by the adversary's damage amount and they return to their tile.
* Adversary moves onto a player on their turn:
    * If they inflict enough damage to eject the player, the player is ejected adn they take the tile.
    * If they do not inflict enough damage to eject the player, they distribute the damage and return to their tile.
* Zombies inflict 60 damage points and Ghosts inflict 40 damage points.
    * Because Zombies have less move opportunities than ghosts, they were given more damage power and enough damage such that it only takes two hits to eject the player.
    * With more move opportunities, Ghosts were given less damage power, requiring three hits from a ghost to eject a player. There is a possibility that a ghost randomly teleports onto a player, inflicts damage, and returns to the tile they were previously at (a true "ghost" attack).
    * However, a combination of one hit each from a Zombie and a Ghost is enough power to eject the player.
***

## Snarl: Remote Protocol Changes
Now, a (result) is one of:
* "OK", meaning “the move was valid, nothing happened”
* "Key", meaning “the move was valid, player collected the key”
* "Exit", meaning “the move was valid, player exited”
* "Eject", meaning “the move was valid, player was ejected”
* "Invalid", meaning “the move was invalid”
* "Damage-X", meaning “the player made contact with an adversary and X damage was recieved”

A (player-update-message) is now:
```ruby
{"type": "player-update",
"layout": (tile-layout),
"position": (point),
"objects": (object-list),
"actors": (actor-position-list),
"message": (maybe-string),
"health": (natural)
}
```
Where health is the player's remaining health points.

## Implementaton Changes
* Changes to players:
    * Players now have a `_health` attribute with additional methods `get_health()` and `reduce_health(points_to_remove: int)` to retrieve their health remaining and reduce their health after an attack.
* Changes to adversaries:
    * Adversaries now have a `_damage` attribute with an additional methods `get_damage()` to retrieve their damage they can disburse.
* Changes in rule_checker.py:
    * The constructor now takes in a `combat` boolean where if False, the game is played without the combat system (player ejected on contact), and if true the combat system is used.
    * For `player_move_result(player: AbstractPlayer, row: int, col: int)`, the function now checks whether a player is truly ejected or just damage is given, same in `adversary_move_result(player: AbstractAdversary, row: int, col: int)`
    * If just damage is given *Damage-X* is returned, where X is a natural number representing the amount of damage recieved
* Changes in game_manager.py
    * In `move_player(player_name: str, row: int, col: int)`, if the move result was  *Damage-X*, then the player is not moved and *X* health is removed.
    * In `move_player(adversary: AbsrtactAdversary, row: int, col: int)`, if the move is to a player the adversary will only move to the tile if they can disburse enough damage to eject the player. If not, then they will dish out the damage and remain put.
    * In `get_player_update(player_name: str)`, a *health* key is added to the player-update-message dict with the players current health
* Changes in player_client.py:
    * In `run()`, there is now a check for if the move-result is *Damage-X* and displays this to the client.
* Changes in local_player.py:
    * For `render_view()`, the player's health is displayed


