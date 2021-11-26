# Game Manager Design 

The game manager is responsible for:
* Registering players, observers, and remote adversaries
* Beginning game play and running game of Snarl
* Requesting moves and sending updates to players amd adversaries
* Validating moves through the Rule Checker

# Game Manager Interface

```python
class GameManager(
  level_jsons: list(dict),
  start_level_num: int,
  combat: bool,
  seed: int,
  local: bool,
  game_id: int
):

```

## Methods

```python
register_player(player: AbstractPlayer) -> None
  """
  Registers the player to the game
  """

register_adversary(adversary: AbstractAdversary) -> None
  """
  Registers the adversary to the game
  """

register_observer(observer: AbstractObserver) -> None
  """
  Registers the observer to the game
  """

move_player(player: AbstractPlayer, row: int, col: int) -> str
  """
  Attempts to move player to given row/col indices and returns result of move
  """

move_adversary(adversary: AbsractAdversary, row: int, col: int) -> None
  """
  Attempts to move adversary to given row/col indices and returns result of move
  """
```