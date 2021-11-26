# Observerable Design 


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The observerable class will be an interface that allows for viewing of a game in progress. This component will store who is observing what game and will be responsible for registering observers and notifying observers when there are updates to the game.

# Observerable Interface

```python
class Observerable:
	"""
	Interface responsible for storing observers of games, registering aforementioned observers,
	and updating the observers as they come through.

	Parameters
	----------
	host_ip_address : str
		IP address to host the server
	port : int
		Port for others to connect to
	"""


```
#### Methods

;; This allows for observers to be registered to observe the game
* register_observer(observer: Observer)

;; This allows for observers to be notfied when there are updates to the game. The notifcation will be an updated game state JSON that will be parsed by their viewing interface.
* notify_observers()

;; This allows for observers to be removed once they leave the viewing interface
* remove_observer(observer: Observer)


# Observer Design 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The observer will be an interface that allows for viewing of a game in progress. This observing component is different than the user interface for the players, for there is no actual interaction, just viewing updates to the game.

```python
class Observer:
	"""
	Interface allowing for users to observer a game in progress. Once they are registered, they will be automatically updated with game states as they come through.

	Parameters
	----------
	obvervable : Observerable
		Observerable object to register to
	"""

```
#### Methods

;; This allows for the observer to notify their observable object, such as leaving the game they are observing.
* notify()


