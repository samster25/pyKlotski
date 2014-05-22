pyKlotski
=========
The goal is to get the large red block to the white bar on the bottum of the window.
Game play consists of mouse clicks only. You select the piece and the slot you want to
move it to. For the case of the Rectangle and the Big Square you can click any part of the piece 
and it will register to move the whole piece. The game has a move counter that increments up 
after every single move and it also counts moving a piece over two spaces as 1 move. When 
moving a piece a slot down, in the case of the bigger pieces, you can click any portion of that
piece and click the square under or below to move it once. If you want to move it two spaces, the 
same concept in selecting the piece applies, you click the second block to where you're moving 
the piece to.

Implementation
--------------
For the game logic I used Python 2.7 and the User Interface is handled by a python library called [Pygame](http://www.pygame.org/wiki/about). For the logic I first created a hash table dictionary that holds a game piece. This game piece can be a small, tall, wide, big or even empty piece. I used an abstract class for the piece which all the real pieces inherit from. I then created another table that holds a game piece for every tile in the board by row and column. So a tall tile which takes two spots would have one spot in the piece table and take up two spots in the tile table. When the game first starts, the pieces are loaded to their default location. when a piece is requested to move, it checks if it has enough space in the new spot and if there is a path there. if there is, the empty tiles swap with the requested move piece and adds 1 to the total move count. When the big piece gets to the white bar, the user has won the game and the game resets. I used pygame for the UI. for that I run a game loop which checks for user input and corresponds mouse location to a game piece. When the user selects a piece, the pieces "selected" method becomes True. When a new tile has been selected it trys to swap with it if it's an empty tile else it selects that one as the new selected tile.

