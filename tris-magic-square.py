import itertools

class MagicSquareTicTacToe:
    def __init__(self):
        # Formal mapping between the board grid (0-8) and the magic square values
        self.magic_square = [8, 1, 6, 
                             3, 5, 7, 
                             4, 9, 2]
        
        # Lists to track the moves (numbers chosen by each player)
        self.bot_numbers = []
        self.player_numbers = []
        
        # Available moves left (numbers from 1 to 9 still free)
        self.available_numbers = set(self.magic_square)

    def check_win(self, numbers):
        """Check if a list of numbers contains any triplet that sums up to 15."""
        if len(numbers) < 3:
            return False
        # Check all possible combinations of 3 numbers in the player's set
        for combo in itertools.combinations(numbers, 3):
            if sum(combo) == 15:
                return True
        return False

    def find_winning_move(self, numbers):
        """Find the missing number to reach a sum of 15. Returns it if it's available."""
        if len(numbers) < 2:
            return None
        # Check every pair of already possessed numbers
        for combo in itertools.combinations(numbers, 2):
            missing_number = 15 - sum(combo)
            if missing_number in self.available_numbers:
                return missing_number
        return None

    def bot_move(self):
        """Bot logic based entirely on magic square arithmetic."""
        # Rule 1: Can I win in this move?
        move = self.find_winning_move(self.bot_numbers)
        if move:
            return move
            
        # Rule 2: Is the opponent about to win? Block them!
        move = self.find_winning_move(self.player_numbers)
        if move:
            return move

        # Rule 3: Take the center (the number 5 is crucial in the magic square)
        if 5 in self.available_numbers:
            return 5

        # Rule 4: Choose a strategic move among the remaining ones (prefer corners: even numbers)
        corners = [8, 6, 4, 2]
        for corner in corners:
            if corner in self.available_numbers:
                return corner
                
        # Fallback: take the first available number
        return list(self.available_numbers)[0]

    def print_board(self):
        """Display the classic game grid (X and O) by reading the owned numbers."""
        board = []
        for num in self.magic_square:
            if num in self.bot_numbers:
                board.append("O")
            elif num in self.player_numbers:
                board.append("X")
            else:
                # Show the visual index of the move (1-9) to help the user
                board.append(str(self.magic_square.index(num) + 1))
        
        print(f"\n {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} \n")

    def play(self):
        print("Welcome to Arithmetic Tic-Tac-Toe (Magic Square Isomorphism)!")
        print("You are X, Bot is O. Type the cell number (1-9) to play.")
        
        while self.available_numbers:
            self.print_board()
            
            # Human player's turn
            try:
                user_input = int(input("Choose a free cell (1-9): ")) - 1
                if user_input < 0 or user_input > 8:
                    print("Invalid move. Choose between 1 and 9.")
                    continue
                
                chosen_number = self.magic_square[user_input]
                if chosen_number not in self.available_numbers:
                    print("Cell is already taken! Try again.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            # Register the player's move
            self.player_numbers.append(chosen_number)
            self.available_numbers.remove(chosen_number)

            if self.check_win(self.player_numbers):
                self.print_board()
                print("Player 1 wins!")
                return

            if not self.available_numbers:
                break

            # Bot's turn
            bot_chosen = self.bot_move()
            self.bot_numbers.append(bot_chosen)
            self.available_numbers.remove(bot_chosen)

            if self.check_win(self.bot_numbers):
                self.print_board()
                print("Bot wins!")
                return

        self.print_board()
        print("It's a draw!")

if __name__ == "__main__":
    game = MagicSquareTicTacToe()
    game.play()
