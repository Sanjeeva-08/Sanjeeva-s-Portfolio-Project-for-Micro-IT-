import http.server
import socketserver
import json
from urllib.parse import urlparse
import os # Import os module to handle file paths

# Global variables to maintain game state on the server
# This state will reset when the server restarts.
game_board = ["", "", "", "", "", "", "", "", ""]
current_player = "X"
game_over = False
winner = None
draw = False

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
    # A draw occurs if no empty cells left and no one has won
    return "" not in board and not check_win(board, "X") and not check_win(board, "O")

def reset_game_state():
    """Resets the global game state variables."""
    global game_board, current_player, game_over, winner, draw
    game_board = ["", "", "", "", "", "", "", "", ""]
    current_player = "X"
    game_over = False
    winner = None
    draw = False

class TicTacToeHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler for Tic-Tac-Toe game logic.
    Handles POST requests for game moves and starting new games.
    Includes CORS headers for frontend communication.
    """
    def end_headers(self):
        # Add CORS headers to allow requests from the frontend
        self.send_header('Access-Control-Allow-Origin', '*') # Allow all origins for development
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def _send_json_response(self, status_code, data):
        """
        Helper method to send a JSON response to the client.
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """
        Handles CORS preflight requests.
        Browsers send an OPTIONS request before actual POST requests to check permissions.
        """
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        """
        Handles POST requests for game logic.
        Routes requests based on the URL path.
        """
        global game_board, current_player, game_over, winner, draw

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Read the content length from headers and then the request body
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        except ValueError:
            self._send_json_response(400, {"error": "Invalid Content-Length header."})
            return

        try:
            request_data = json.loads(post_body.decode('utf-8'))
        except json.JSONDecodeError:
            self._send_json_response(400, {"error": "Invalid JSON in request body."})
            return

        if path == '/new_game':
            reset_game_state()
            self._send_json_response(200, {
                "board": game_board,
                "current_player": current_player,
                "game_over": game_over,
                "winner": winner,
                "draw": draw,
                "message": "New game started. Player X's turn!"
            })
        elif path == '/move':
            if game_over:
                self._send_json_response(400, {"error": "Game is already over. Please reset the game."})
                return

            cell_index = request_data.get('cell_index')
            player_making_move = request_data.get('player')

            if not isinstance(cell_index, int) or not (0 <= cell_index <= 8):
                self._send_json_response(400, {"error": "Invalid cell index."})
                return
            if player_making_move not in ["X", "O"]:
                self._send_json_response(400, {"error": "Invalid player."})
                return
            if game_board[cell_index] != "":
                self._send_json_response(400, {"error": "Cell already taken."})
                return
            if player_making_move != current_player:
                self._send_json_response(400, {"error": f"It's not {player_making_move}'s turn. It's {current_player}'s turn."})
                return

            game_board[cell_index] = current_player

            if check_win(game_board, current_player):
                winner = current_player
                game_over = True
                message = f"Player {winner} wins!"
            elif check_draw(game_board):
                draw = True
                game_over = True
                message = "It's a draw!"
            else:
                current_player = "O" if current_player == "X" else "X"
                message = f"Player {current_player}'s turn."

            self._send_json_response(200, {
                "board": game_board,
                "current_player": current_player,
                "game_over": game_over,
                "winner": winner,
                "draw": draw,
                "message": message
            })
        else:
            self._send_json_response(404, {"error": "Not Found"})

    def do_GET(self):
        """
        Handles GET requests. This is mainly to serve the static HTML, CSS, JS files.
        """
        # Ensure the path is safe
        if ".." in self.path:
            self.send_error(403, "Forbidden")
            return

        # Serve files from the current directory
        f = None
        try:
            if self.path == '/':
                # Serve index.html when root is requested
                filepath = os.path.join(os.getcwd(), 'index.html')
            else:
                filepath = os.path.join(os.getcwd(), self.path.lstrip('/'))

            if not os.path.exists(filepath) or not os.path.isfile(filepath):
                self.send_error(404, "File not found")
                return

            # Determine content type
            ctype = self.guess_type(filepath)
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.end_headers()

            f = open(filepath, 'rb')
            self.copyfile(f, self.wfile)
        except Exception as e:
            self.send_error(500, f"Error serving file: {e}")
        finally:
            if f:
                f.close()


# --- Server Setup ---
PORT = 8000 # Choose a port for your server
Handler = TicTacToeHandler

# Create a TCP server with the custom handler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving Tic-Tac-Toe backend and static files at http://127.0.0.1:{PORT}")
    print("To run this, open your terminal in the directory where app.py, index.html, style.css, and script.js are located and run: python app.py")
    print(f"Then open http://127.0.0.1:{PORT} in your web browser.")
    # Start the server and keep it running indefinitely
    httpd.serve_forever()
