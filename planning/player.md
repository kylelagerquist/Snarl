# Player Design 

Tha player class is a subclass of the `AbstractActor` class and is a data representation of a player in Snarl. It is responsible for storing the player's name, location, knowledge of the game, and providing a move.

# Player Interface

```python
class AbstractPlayer(AbstractActor):
    _player_state # Knowledge of game state
    _ejected # Whether player is ejected from the level
    _exited # Whether player has exited the level
    _times_exited # Number of times player has exited a level
    _times_ejected # Number of times player has been ejected from a level
    _keys_found # Number of times player has found a key
    _health # Player's health

```
## Methods
```python
update_state(state: dict) -> None
    """
    Updates the players knowledge of the game state
    """

request_move() -> (int, int)
    """
    Requests the user to input a move to be sent to manager to be handled
    """

render_view() -> None
    """
    Render's the player's current knowledge of the state
    """

send_message(msg: str) -> None 
    """
    Send the given message to the player
    """

reduce_health(points_to_remove: int) -> None
    """
    Remove the given amount of health points from the player
    """

get_health() -> int
    """
    Retrieve the players health
    """

eject() -> None
    """
    Change the player's ejected status
    """

is_ejected() -> bool
    """
    Return whether the player has been ejected from the level
    """

exit() -> None
    """
    Change the player's status to exited
    """

is_exited() -> bool
    """
    Return whether the player has exited from the level
    """

found_key() -> None
    """
    Increase number of keys the player has found
    """

return_to_game() -> None
    """
    Returns the player to the game
    """

is_active() -> bool
    """
    Retrieve whether a player's active in the game
    """

get_player_score_json() -> dict
    """
    Retrieves the (player-score) JSON object
    """
```