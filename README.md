# Using snarlServer

The snarlSever executable starts the server with the following command line 
arguments:

* `--levels FILE`: Where `FILE` is the path and name of a file containting JSON
level specifications. `snarl.levels` is default
* `--clients N`: Where 1 ≤ `N` ≤ 4 is the maximum number of clients the server should wait for before starting the game. `4` is default
* `--wait N`: Where `N` is the number of seconds to wait for the next client to connect. Default is `60`.
* `--observe`: If option is given, an observer view will be seen on terminal running the server.
* `--address IP`: Where `IP` is an IP address on which the server should listen for connections. Default is `127.0.0.1`.
* `--port NUM`: Where `NUM` is the port number the server will listen on. Default is `45678`.
* `--combat`: If option is given, Hit Point system (described below) is used.
* `--games N`: Where `N` is the maximum amount of games of Snarl to run on the server. Games can be run concurrently. Default is `1`.
* `--remote_adv`: If option is given, the server allows for remote adversaries to join while waiting for players to join before a game begins.

Once the executable is ran, it will begin to wait for clients to connect. After first
client connects, it will wait the maximum time specified for another client to connect. The game will start once the wait time is hit, or max clients have joined.
If the observe argument is given, every time there is a game update (player or adversary move) the updated state will be shown.

### Running Multi-Game Server
If `--games N` is greater than 1, then the server will allow for multiple games to be played concurrently. Each game is ran in its own thread, therefore if an error occurs, only the thread will end, not the entire server. The server will continue to run until all threads have been completed. The client registration process is the same as above, however once a game begins, if more games are allowed, the server will repeat the registration process by waiting indefintely for the first client to conenct. To end the server, the administrator can shut it down by passing CTRL-C.

### Using Hit Point System
If the `--combat` flag is given, players are not immidiately ejected on adversary contact. Instead the Hit Point system is used, starting players with 100 HP and zombie contact reduces HP by 60 and ghost contact reduces HP by 40. If contact results in the player's health falling below 0, they are ejected. If contact does not result in enough damage to eject the player, both the adversary and player remain on same tile.

### Using Remote Adversaries
If the `--remote_adv` flag is given, the server accepts remote adversary connections while it is waiting for clients to connect. If a remote adversary connects, they are assigned to whatever game the server is currently accepting clients for. During any level, if there are more remote adveraries registered to the game than there are adversaries required, some remote adversaries may not be used. Vice versa, if there are less remote adversaries registered than required for a level, local adversaries will be used to fill the difference. Remote adversaries follow the same stratergies as local adversaries (automated).

# Using snarlClient

The snarlClient executable starts the player client with the following command line arguments:

* `--address IP`: Where `IP` is an IP address on which the client should connect to. Default is 127.0.0.1.
* `--port NUM`: Where `NUM` is the port number the client will connect to. Default is 45678.

Once connected, the server will add the client to the game they are currently registering clients for. Once the max clients are reached for that game or the timeout is reached, the game will begin and the client will be prompted to enter a name. If the name is invalid or already taken on the server, they will be prompted again up to 5 times.

When it is the player's turn, an updated view of their knowledge of the level will be displayed as seen below with the following mapping:
  
PLAYER (\<PLAYER NAME>) VIEW   
HEALTH: 100  
0 0 0 0 0  
0 1 1 1 0  
2 1 1 1 0  
0 1 1 1 0  
0 0 0 0 0  

*The player is located on the tile in the center of the view

* 0 = wall or void
* 1 = walkable tile
* 2 = door tile
* P = another player
* Z = zombie
* G = ghost
* K = key
* E = exit


The player will then be prompted to enter a row index and a subsequent column index to move to (Zero-based). The player is always located in the center of their view so if they would like to move two tiles to the left, they would enter 2 for row index and 0 for column index. If they wanted to skip their turn, they would enter 2 for row and column index to remain on the same tile. The game will continue following normal Snarl rules.

# Using snarlAdversary

The snarlAdversary executable starts the remote adversary client with the following command line arguments:

* `--address IP`: Where `IP` is an IP address on which the client should connect to. Default is 127.0.0.1.
* `--port NUM`: Where `NUM` is the port number the client will connect to. Default is 45678.

Once connected to the server, the remote adversary is assigned to whichever game the server is currently loading with client connections. Once a level begins, if the adversary is used in the level, they will be sent a JSON telling them their name and what type of adversary they are. During gameplay, they will be provided with an update of the state of the level on their turn be asked to provide a move. Remote adversaries are assigned adversary roles in a level based on the order they joined. If a remote adversary connection is not needed for a level, they will not be provided with any game info.