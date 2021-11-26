# Rule Checker Design 






&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To perform the role of a game manager in a more efficient manner, we will delegate some of the responsibilities onto a Rule Checker.  The Rule Checker component is responsible for ensuring player and adversary interactions result in a valid game state; the rule checker must reject invalid game states.  To do this, the Rule Checker needs to validate player/adversary movement and interactions.  The Rule Checker must also determine the different end states for Snarl.  This includes disguinishing between the end of a level and the end of game.

# Rule Checker Interface 

```python
class RuleChecker():

# Current Game state
# Level
# list of players and positions
# list of adversaries and positions
# list of objects and positions
# isExitUnlocked field

```
#### Methods

* When a player acts on their turn, their actions will be evaluated by the rulechecker to determine validity.
* valid_move: This method will call the corresponsing helper methods below to evaluate a movement
* valid_player_move(self, tile)
  * This method will ensure that the player is attemping to move to a space that is within 2 cardinal moves away from their current position, and that this position is not a wall.  If not, the game state is rejected.
* valid_player_interaction(self, tile)
  * This method will check the interaction the player will attempt on their tile and ensure that it is valid.  If the tile contains another player, it is an invalid move.  If it contains an enemy, the player will be eliminated.  If the tile contains a key, the exit will be unlocked.  If the tile contains an unlocked exit, all players will win the level and will advance to the next level, or if this is the last level, they will win the game.
* valid_adversary_move(self, tile)
  * This method will ensure that the adversary is attemping to move to a space that is within 2 cardinal moves away from their current position, and that htis position is not a wall.  If the adversary contains special powers such as a ghost, we will create another helper function accordingly.
* valid_adversary_interaction(self, tile)
  * This method will check the interaction the adversary will attempt on their tile and ensure that it is valid.  If the tile contains another adversary, it is an invalid move and the game state is rejected.  If it contains a player, the player will be eliminated.  If the player eliminated is the last player remaining, the game will end.  If the tile contains a key or an exit, nothing happens.
