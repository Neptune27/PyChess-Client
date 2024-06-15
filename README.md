PyChess is a Python implementation of the game Chess. It allows you to play against computer (Stockfish), and player (in both offline and online). It features all chess rules with my own implementations without using chess packages.

# Feature:
 - Play chess against Stockfish
 - Play chess in offline and online mode
 - Play random chess puzzle game
 - Standard ruleset of chess
 - All pieces movements with move hints
 - All special movements ([En passant](https://en.wikipedia.org/wiki/En_passant), 
[Castling](https://en.wikipedia.org/wiki/Castling), [Pawn Promotion](https://en.wikipedia.org/wiki/Promotion_(chess)))
 - All win conditions (Resign, checkmate)
 - All draw
 - Have both FEN and PGN
 - Have GUI with pieces move show for each pieces

# Prerequisites:
 - Python 3.11 or below
 - Necessary libraries (`pip install -m requirement.txt`)
 - [Stockfish binary](https://stockfishchess.org/download/)

# Installations
1. Rename stockfish binary to `stockfish` (Linux) or `stockfish.exe` (Windows) and move it into `stockfish/linux` if you're using linux, `stockfish/windows` if you're using windows. 
2. If you're want to play multiplayer, see [Multiplayer](#multiplayer)
3. Run `python main.py` in the root directory.

# Multiplayer
 - Download or clone [PyChess-Server](https://github.com/Neptune27/PyChess-Server)
 - Run `python main.py` in a separate process
 - Go to Online and change the address to `localhost:9999` and connect

# To be Added
 - Evaluation bar
 - See previous move without undo
 - More graceful multiplayer handle
 - More game modes

# License
PyChess is licensed under the MIT License. See the LICENSE file for details.