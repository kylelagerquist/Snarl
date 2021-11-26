TO:​ Growl

FROM:​ Christian DiVincenzo, Kyle Lagerquist

DATE:​ February 15, 2021

SUBJECT:​ ​ Game States


# Game State 

A Game State consists of the following components. 

1. a level consisting of multiple rooms and hallways connecting said rooms.
2. Enemy and player placement.
   * This will include the location of moves attempted.
3. Object placement and status of the exit.
    * exit status handles level progression.
4. Keeping track of turn progression, delegate when each client should input actions
5. Players that have exited vs. ejected.
    * Status of players will trigger either failure or game progression.


## Game States Interface For Game Manager

The game manager must be provided with the full scope of information pertaining to Snarl.  This includes:

* A representation of the full level, including rooms, and hallways.  This will include all entities and objects within.
* Generate a random level from a random seed
* add_player() -- This will handle a client joining the game, and add them to the level.
* remove_player() -- this will remove a player from the game.
* #### recieve_action(...) -- This will serve as the main action handler for the game manager.  When something interacts with the game, recieveAction will in turn trigger modification of the game state accordingly.
* update_state() -- updates games states and sends game state to players
* The location of all players
* Which players have exited the level or have been eliminated.
* is_exit_unlocked() This will be determined based on the recieveAction handler.  When a key is found, the exit is marked as unlocked.  The game manager will need this information throughout the game.
* is_valid_move() When the action handler recieves a movement, this will determine if the movement is accepted by the game state.
## Game States Interface For Players

Players will interact with the interface in a limited way.  They will perform the following actions, which will be handled by recieveAction(...)

* Move(tile to move to)
* getGameState() -- which will allow players to see a limited number of tiles around them, as well as whether they are still in the level.
* disconnect() -- This will allow a player to disconnect from the game.


