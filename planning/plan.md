TO:​ Growl

FROM:​ Christian DiVincenzo, Kyle Lagerquist 

DATE:​ February 7, 2021

SUBJECT:​ ​ Snarl Project Analysis

## Components
* **Level:** Consists of nested list of Tiles representing a valid level representation.
    * Knowledge: All player/adversary positions, all tile locations, all object locations, level status.
* **Level Generator:** Consists of lists of valid rooms and hallways that do not overlap.
    * Knowledge: Rooms, hallways, and the tile that comprise them. 
* **Room:** A room will be a layout consisting of tiles, on a coordinate plane, containing hallways along some edges, possibly an exit. 
    * Knowledge: Tiles, coordinates
* **Hallway:** A set of tiles connecting one room to another.
    * Knowledge: Start position, end position, list of waypoints, and coordinates.
* **Tile:** A square that may be inhabited by an adversary, an exit, a key, or a player.
     * Knowledge: Whether or not it is inhabited, and what it is inhabitated by, its coordinates, what type.
* **Player(s):** A player will be comprised of a name, a location indicating what tile they are on, and what objects they may hold.
     * Knowledge: Able to see a limited area around them, whether or not they have unlocked the exit, their own location.
* **Adversaries:** An adversary will consist of a location indicating the room that they are in, and a coordinate within the room board.
    * Knowledge: Entire level, including player(s) locations, exit and key locations.
    * Code will be supplied by others, will be automated.
* **Stratergy:** Provided code that will determine how the adversary moves.
    * Knowledge: Entire level, including player(s) locations, exit and key locations.
* **Key:** A key to exit the room will have a location coordinate the room it is in.  This will be be  placed in a room.

* **Exit:** An exit will be  placed in a separate room from the key.
    * Knowledge: Whether or not it is locked.


 
* **Interactive** What the players will interact with, which contains a knowledge of which level a player is on, all the way down.

## Milestones
* **Model** 
* **Command line implementation**
* **Visual GUI** 
* **Interactive GUI** 
* **Local Play** 
* **Stratergy Update Implementation** 
* **Server Connection** 
* **Complete Game** 



