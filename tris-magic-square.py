import itertools

class MagicSquareTicTacToe:
    def __init__(self):
        # Formal mapping between the board grid (0-8) and the magic square values
        self.magic_square = [8, 1, 6,
                             3, 5, 7,
                             4, 9, 2]

        # Precomputed reverse map: magic square value -> grid index (0-8)
        self.value_to_index = {v: i for i, v in enumerate(self.magic_square)}

        # Lists to track the moves (numbers chosen by each player)
        self.bot_numbers = []
        self.player_numbers = []

        # Available moves left (numbers from 1 to 9 still free)
        self.available_numbers = set(self.magic_square)

    # ------------------------------------------------------------------ #
    #  Core math: all analysis is done via magic square arithmetic only   #
    # ------------------------------------------------------------------ #

    def check_win(self, numbers):
        """Check if a list of numbers contains any triplet that sums to 15."""
        if len(numbers) < 3:
            return False
        for combo in itertools.combinations(numbers, 3):
            if sum(combo) == 15:
                return True
        return False

    def find_winning_moves(self, numbers):
        """
        Return the set of available numbers that would complete a sum-15 triplet
        for the given player. Each such number is a winning (or blocking) move.
        """
        winning = set()
        if len(numbers) < 2:
            return winning
        for combo in itertools.combinations(numbers, 2):
            missing = 15 - sum(combo)
            if 1 <= missing <= 9 and missing in self.available_numbers:
                winning.add(missing)
        return winning

    def find_fork_moves(self, numbers):
        """
        A fork is a move that simultaneously creates TWO different winning threats.
        We test each available number: if adding it to `numbers` produces 2+ winning
        threats (via find_winning_moves on the updated set), it is a fork move.
        Still pure magic-square arithmetic — no board scanning.
        """
        forks = set()
        for candidate in self.available_numbers:
            future_numbers = numbers + [candidate]
            # After taking `candidate`, how many winning threats exist?
            future_available = self.available_numbers - {candidate}
            threats = set()
            for combo in itertools.combinations(future_numbers, 2):
                missing = 15 - sum(combo)
                if 1 <= missing <= 9 and missing in future_available:
                    threats.add(missing)
            if len(threats) >= 2:
                forks.add(candidate)
        return forks

    # ------------------------------------------------------------------ #
    #  Bot decision logic                                                  #
    # ------------------------------------------------------------------ #

    def bot_move(self):
        """
        Bot strategy — strictly ordered, all via magic square arithmetic:
          1. Win immediately
          2. Block opponent's immediate win
          3. Create a fork (two simultaneous threats)
          4. Block opponent's fork
          5. Take center (5)
          6. Take a corner (even numbers: 8, 6, 4, 2)
          7. Take any remaining cell (ordered fallback)
        """
        # Rule 1: win
        winning_moves = self.find_winning_moves(self.bot_numbers)
        if winning_moves:
            return min(winning_moves)  # deterministic choice

        # Rule 2: block
        blocking_moves = self.find_winning_moves(self.player_numbers)
        if blocking_moves:
            return min(blocking_moves)

        # Rule 3: create a fork
        bot_forks = self.find_fork_moves(self.bot_numbers)
        if bot_forks:
            return min(bot_forks)

        # Rule 4: block opponent's fork
        opp_forks = self.find_fork_moves(self.player_numbers)
        if opp_forks:
            return min(opp_forks)

        # Rule 5: center
        if 5 in self.available_numbers:
            return 5

        # Rule 6: corners (even numbers in the Lo Shu square)
        for corner in [8, 6, 4, 2]:
            if corner in self.available_numbers:
                return corner

        # Rule 7: ordered fallback (edges: odd non-center numbers)
        for side in [1, 3, 7, 9]:
            if side in self.available_numbers:
                return side

        # Should never reach here, but just in case
        return min(self.available_numbers)

    # ------------------------------------------------------------------ #
    #  Display                                                             #
    # ------------------------------------------------------------------ #

    def print_board(self):
        """Display the classic grid using the precomputed reverse map."""
        board = []
        for i, num in enumerate(self.magic_square):
            if num in self.bot_numbers:
                board.append("O")
            elif num in self.player_numbers:
                board.append("X")
            else:
                board.append(str(i + 1))   # show cell index (1-9) for the user

        print(f"\n {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} \n")

    # ------------------------------------------------------------------ #
    #  Main game loop                                                      #
    # ------------------------------------------------------------------ #

    def play(self):
        print("Welcome to Arithmetic Tic-Tac-Toe (Magic Square Isomorphism)!")
        print("You are X, Bot is O. Type the cell number (1-9) to play.\n")

        while self.available_numbers:
            self.print_board()

            # --- Human player's turn ---
            try:
                raw = input("Choose a free cell (1-9): ")
                user_input = int(raw)                    # FIX: validate before subtracting
                if user_input < 1 or user_input > 9:
                    print("Invalid move. Choose a number between 1 and 9.")
                    continue
                chosen_number = self.magic_square[user_input - 1]
                if chosen_number not in self.available_numbers:
                    print("Cell already taken! Try again.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            self.player_numbers.append(chosen_number)
            self.available_numbers.remove(chosen_number)

            if self.check_win(self.player_numbers):
                self.print_board()
                print("You win! Congratulations!")
                return

            if not self.available_numbers:
                break

            # --- Bot's turn ---
            bot_chosen = self.bot_move()
            self.bot_numbers.append(bot_chosen)
            self.available_numbers.remove(bot_chosen)
            print(f"Bot plays cell {self.value_to_index[bot_chosen] + 1}.")

            if self.check_win(self.bot_numbers):
                self.print_board()
                print("Bot wins!")
                return

        self.print_board()
        print("It's a draw!")


if __name__ == "__main__":
    game = MagicSquareTicTacToe()
    game.play()
