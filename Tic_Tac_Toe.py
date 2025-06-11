def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_win(board, player):
    """Checks if the given player has won."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return " " not in board

def get_player_move(player, board):
    """Gets a valid move from the current player."""
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == " ":
                return move
            else:
                print("Invalid move or spot already taken. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def tic_tac_toe():
    """Main function to run the Tic-Tac-Toe game."""
    board = [" "] * 9  # Initialize an empty board
    current_player = "X"
    game_over = False

    print("Welcome to Tic-Tac-Toe!")
    print("The board positions are numbered 1-9 like a keypad:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")

    while not game_over:
        print_board(board)
        move = get_player_move(current_player, board)
        board[move] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Congratulations! Player {current_player} wins!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch players
            current_player = "O" if current_player == "X" else "X"

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again == "yes":
        tic_tac_toe() # Recursively call to play again
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    tic_tac_toe()
