# Milestone 6 - Refactoring Report

**Team members:**
Kyle Lagerquist and Christian DiVincenzo

**Github team/repo:**
Londorthel
https://github.ccs.neu.edu/CS4500-S21/Londorthel

## Plan
1. Clean up the level class. Currently this class is responsible for all changes to tiles, all tile 'queries', and updates to all of the players. We decided this is not good code design for many reasons, one of them being when a player is added, they are added to the game manager and then also added to level. We want the level class to just have knowledge of the tile, room, hallway, and object locations.
1. In order to clean the level class up, many of the methods must be moved to the RuleChecker class. It should be the responsibility of the RuleChecker class to check what tiles are traversable, the validity of the moves, and the move outcome.
1. The GameManager class is alsoe repeating some of the responsibilities of the Level and RuleChecker class. This should change so the GameChecker class just 'asks' the RuleChecker about the outcome of a move, and then ensures the level and player are updated accordingly.
1. We noticed that we were using isinstance() alot to check what type of tile or what type of actor. It was decided that this is also not good code design and we should be creating methods to ask what time, so their is less reliance on each class.
1. We would like to solidfy a better method for how the game is actually played (players are iterated over, moves are accepted, updated are delivered).
1. We would like to change the game state JSON that is passed to our view to mimic the state JSON that the milestones are using.
1. We would like to create a level constructor that accepts a state JSON and parses it.


## Changes
1. We are satisfied with our changes to the level class in which now there is no reliance on players or adversaries. The only interaction would be when the game manager calls upon the level class to update the person on a tile. Besides that, players and adversaries to not actually need to be added, removed, or moved with the Level class.
1. The methods used to determine traversable points and its helpers have now been moved to the rule checker class. It is now the sole responsibility of the rule checker to determine whether or not a move is allowed and also figuring out the outcome of the aforementioned move.
1. Many of the game manager methods that were extremly similar to that of the rule checker have been removed (i.e. determing the outcome of the move). Now the game manager 'asks' the rule checker for the move outcome and whether it was valid or not.
1. Much of the use of isinstance() has been removed. The methods get_type() have been added to all dependents of the Tile interface to return the type of the tile ('space', 'wall', 'door'). Also methods were added to the adversary and player interface of is_player() to determine whether an actor in the game was an adversary or player.
1. The build_state() method in the GameManager class was changed to output the state JSON that the milestones have been using.
1. The LevelGenerator class now takes in a Level JSON and can construct all of the rooms, hallways, and valid level from it.

## Future Work
1. We would like to change the view interface to be able to constuct a view solely from a state JSON. Currently there must be an added 'layout' tag with all of the tiles in a nested list to build the entire level view.
1. We still have not yet decided how to implement the best play_game() function. We are still recieving information on how the game is actually played, how the GameManager recieves information from the game users, and how information is relayed back to the game users. In the next milestone, we believe this will be cleared up and we will be able to fully implement the GameManager, and any additonal help from the RuleChecker.
1. We need way more tests on how the game will actually be ran to ensure random bugs don't arise in the game play that crashes the entire program.


## Conclusion

We think our code design is holding very stongly so far. The only thing that is constantly on the back of our mind, as mentioned above, is how the GameManager will actually be accepting moves, and progressing the game. All the framework is built around, but there is just a few issues outstanding that need to be locked in and implemented this week. Overall, we believe this was a very productive week of changes, and were able to catch up on some technical debts that were accumulating.
