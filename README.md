# Magic Square Tic-Tac-Toe

An elegant, unbeatable Tic-Tac-Toe AI bot implemented in Python. Instead of using traditional game-tree search algorithms like Minimax or hundreds of nested `if/then` conditional checks, this project leverages mathematical **isomorphism** using a $3 \times 3$ Magic Square.

---

## The Concept (The Math Behind the Game)

This project formally maps the spatial grid of Tic-Tac-Toe onto the **Lo Shu Magic Square**, where every single row, column, and diagonal sums up to exactly **15**:

```text
 8 | 1 | 6
---+---+---
 3 | 5 | 7
---+---+---
 4 | 9 | 2

```

By introducing this grid, the game of Tic-Tac-Toe becomes perfectly isomorphic to **Number Scrabble** (also known as *Pick15*). The gameplay shift is fascinating:

* Players take turns picking a number from 1 to 9.
* The first player to collect **exactly 3 numbers that sum up to 15** wins.

### Why this approach is highly efficient:

* **Instant Win/Block Analysis:** To check if a player is about to win, the bot doesn't need to scan multi-dimensional arrays or check 8 different lines. It simply evaluates pairs of currently owned numbers ($n_1, n_2$) and checks if the required third number is available using basic subtraction:

$$n_{missing} = 15 - (n_1 + n_2)$$

* **Zero Computational Overhead:** It replaces expensive lookups, game-tree simulations, and heavy recursion with elementary arithmetic operations, making the bot lightweight, fast, and mathematically optimal.

---

## Features

* **Smart AI Opponent:** Plays optimally by prioritizing wins, strategic blocks, and center/corner control using magic square properties.
* **Clean Object-Oriented Code:** Written in modular Python using native libraries (`itertools`).
* **Interactive CLI Interface:** Easy to play directly from your terminal.

---

## Project Structure

```text
├── .gitignore          # Prevents tracking of cache and temporary files
├── LICENSE             # MIT License file
├── README.md           # Project documentation
└── tic_tac_magic.py    # Main Python source code

```

---

## How to Run

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Letto-spa/tris-magic-square.git

```

2. Navigate into the project folder:

```bash
cd tris-magic-square

```

3. Run the game using Python 3:

```bash
python tic_tac_magic.py

```

---

## License

This project is open-source and available under the [MIT License].