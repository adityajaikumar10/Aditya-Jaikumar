class Player:
    """Stores details about a player: their name, their symbol (X, O, etc.),
    and whether they are human or computer-controlled."""

    def __init__(self, name, symbol, is_computer=False):
        self.name = name
        self.symbol = symbol
        self.is_computer = is_computer


class TicTacToe:
    """Manages the game board, player moves, rules, and score tracking."""

    def __init__(self):
        # A list of 9 empty spaces representing the 3x3 board
        self.board = [" "] * 9

        # Keeps track of scores across multiple rounds
        self.scores = {"player1": 0, "player2": 0, "draws": 0}

        self.player1 = None
        self.player2 = None

    def display_board(self):
        """Prints the current state of the board in a friendly grid format."""
        print("\n")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("\n")

    def setup_game(self):
        """Asks players to choose game mode, names, and custom symbols."""
        print("=" * 30)
        print("    Welcome to Tic-Tac-Toe!   ")
        print("=" * 30)
        print("1. Single Player (vs Computer)")
        print("2. Two Players (vs Friend)")

        # Validate game mode choice
        while True:
            mode = input("\nChoose a game mode (1 or 2): ").strip()
            if mode in ["1", "2"]:
                break
            print("Please enter either 1 or 2.")

        # Set up Player 1
        p1_name = input("\nEnter Player 1's name (default: Player 1): ").strip() or "Player 1"
        while True:
            p1_symbol = input(f"Choose a symbol for {p1_name} (e.g. X, O, *, @): ").strip().upper()
            if len(p1_symbol) == 1 and not p1_symbol.isspace():
                break
            print("Please enter a single non-space character.")

        self.player1 = Player(p1_name, p1_symbol)

        # Set up Player 2 (Human or Computer)
        if mode == "2":
            p2_name = input("\nEnter Player 2's name (default: Player 2): ").strip() or "Player 2"
            while True:
                p2_symbol = input(f"Choose a symbol for {p2_name}: ").strip().upper()
                if len(p2_symbol) == 1 and not p2_symbol.isspace() and p2_symbol != p1_symbol:
                    break
                print(f"Invalid symbol! Must be one character and different from '{p1_symbol}'.")
            self.player2 = Player(p2_name, p2_symbol)
        else:
            # Auto-assign symbol for the computer
            p2_symbol = "O" if p1_symbol == "X" else "X"
            self.player2 = Player("Computer", p2_symbol, is_computer=True)
            print(f"\nThe computer will play as '{p2_symbol}'.")

    def get_player_move(self, player):
        """Asks a human player for a move (1-9) and validates the input."""
        while True:
            user_input = input(f"{player.name}'s turn ({player.symbol}). Enter cell (1-9): ").strip()

            # Check if input is empty
            if not user_input:
                print("Don't leave it blank! Please enter a number between 1 and 9.")
                continue

            # Check if input is an actual number
            try:
                move_number = int(user_input)
            except ValueError:
                print("Oops! That's not a number. Please pick a number from 1 to 9.")
                continue

            # Check if number is in range
            if move_number < 1 or move_number > 9:
                print("Out of range! Pick a number between 1 and 9.")
                continue

            # Convert 1-9 to 0-8 list index
            index = move_number - 1

            # Check if spot is free
            if self.board[index] != " ":
                print("That spot is already taken! Pick another one.")
                continue

            return index

    def get_computer_move(self):
        """
        Determines the computer's move using simple logic (no imports required):
        1. If computer can win right now -> take that spot.
        2. If human is about to win -> block that spot.
        3. Otherwise -> pick center, then corners, then edges.
        """
        print(f"\n{self.player2.name} is making a move...")

        # Step 1: Check if computer can win this turn
        for spot in range(9):
            if self.board[spot] == " ":
                self.board[spot] = self.player2.symbol
                if self.check_win(self.player2.symbol):
                    self.board[spot] = " "  # Undo test move
                    return spot
                self.board[spot] = " "      # Undo test move

        # Step 2: Check if player can win on their next turn, and block them
        for spot in range(9):
            if self.board[spot] == " ":
                self.board[spot] = self.player1.symbol
                if self.check_win(self.player1.symbol):
                    self.board[spot] = " "  # Undo test move
                    return spot
                self.board[spot] = " "      # Undo test move

        # Step 3: Pick the best available spot:
        # Center (4) -> Corners (0, 2, 6, 8) -> Edges (1, 3, 5, 7)
        priority_order = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for spot in priority_order:
            if self.board[spot] == " ":
                return spot

    def check_win(self, symbol):
        """Checks if a given symbol has 3 in a row across any line."""
        winning_combinations = [
            # Horizontal rows
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            # Vertical columns
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            # Diagonals
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] == symbol:
                return True
        return False

    def check_draw(self):
        """Checks if all 9 cells are full with no winner."""
        return " " not in self.board

    def display_scores(self):
        """Prints the current multi-round score tally."""
        print("\n" + "-" * 22)
        print("     SCOREBOARD       ")
        print("-" * 22)
        print(f" {self.player1.name}: {self.scores['player1']}")
        print(f" {self.player2.name}: {self.scores['player2']}")
        print(f" Ties: {self.scores['draws']}")
        print("-" * 22 + "\n")

    def play_round(self):
        """Runs one full round of Tic-Tac-Toe."""
        # Reset the board to empty
        self.board = [" "] * 9
        current_turn = self.player1

        # Show keypad helper for reference
        print("\nPositions correspond to a standard keypad (1-9):")
        print(" 1 | 2 | 3 \n---+---+---\n 4 | 5 | 6 \n---+---+---\n 7 | 8 | 9 ")

        while True:
            self.display_board()

            # Get move from either computer or human
            if current_turn.is_computer:
                move = self.get_computer_move()
                print(f"{current_turn.name} chose position {move + 1}.")
            else:
                move = self.get_player_move(current_turn)

            # Mark move on the board
            self.board[move] = current_turn.symbol

            # Check if this move wins the round
            if self.check_win(current_turn.symbol):
                self.display_board()
                print(f"🎉 {current_turn.name} wins the round! 🎉")
                if current_turn == self.player1:
                    self.scores["player1"] += 1
                else:
                    self.scores["player2"] += 1
                break

            # Check if this move results in a draw
            if self.check_draw():
                self.display_board()
                print("It's a draw! Nobody wins this round.")
                self.scores["draws"] += 1
                break

            # Switch to the other player's turn
            current_turn = self.player2 if current_turn == self.player1 else self.player1

    def run(self):
        """Main game loop with play-again functionality."""
        self.setup_game()

        while True:
            self.play_round()
            self.display_scores()

            # Ask to play again
            replay = input("Would you like to play another round? (y/n): ").strip().lower()
            if replay not in ["y", "yes"]:
                print("\nThanks for playing! Final scores are above. Goodbye! 👋")
                break


if __name__ == "__main__":
    game = TicTacToe()
    game.run()