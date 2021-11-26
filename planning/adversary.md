# Adversary Design 






&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Adversary is representing the adversary componenet in Snarl.  This Adversary recieves the game state and communicates actions back to the game manager. The adversary_json passed in allows for extendable rules.

# Adversary Interface

```python
class Adversary(adversary_json):

# Current Game state
# All Player locations
# Other Adversary locations
# Exit and object locations
# Level tile layout
# Full Level information including all tiles
# Acceptable moves for them
# Possible items in their inventory

```
#### Methods


;; A method for the Adversary to receive current game state. The game state contains data on all of the tiles, where objects are, where they are, where the players and other adversaries are, and all of the tiles on the level. When it is their turn, the manager will be responsible for sending updates to the adversaries.
* update_game_state(state_json)

;; Retrieves the next move for this adversary, this method will be unique for each adversary because their own rules will define what their next move is. The manager will request a move from an adversary on their turn.
* get_next_move()

;; Exit out of the game
*  eject()

;; Retrieve the type of the adversary
* get_type()
