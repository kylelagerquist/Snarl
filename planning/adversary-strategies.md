# Adversary Stratergies

## Zombie
The stratergy for zombies is all based around whether or not there is a player in their room. If there is a player in their room, the zombie will move to the tile
closest to that player, or onto them if possible. If there is no player in their room, the zombie will move to a random valid tile.

## Ghost
The stratergy for ghosts is also based around whether or not there is a player in their room. If there is a player in their room, the ghost will move to the tile
closest to that player, or onto them if possible. If there is no player in their room, and it is possible to move to a wall, the ghost will move to that wall and 
be randomly teleported to a valid tile in the level. If there is no wall in the ghost's vicinity, it will move to a random valid tile.
