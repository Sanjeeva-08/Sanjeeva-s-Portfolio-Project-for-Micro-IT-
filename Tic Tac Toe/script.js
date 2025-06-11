// Get DOM elements
const gameBoardElement = document.getElementById('gameBoard');
const gameStatusElement = document.getElementById('gameStatus');
const resetButton = document.getElementById('resetButton');
const cells = document.querySelectorAll('.cell'); // Get all individual cell elements

// Game state (client-side representation - kept in sync with backend)
let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameOver = false;

// Base URL for your Python http.server backend
// This should match the PORT defined in your app.py
const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Initializes a new game by calling the backend /new_game endpoint.
 */
async function initGame() {
    try {
        const response = await fetch(`${API_BASE_URL}/new_game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if (response.ok) {
            updateUI(data.board, data.message, data.winner, data.draw);
            // Update client-side state based on backend response
            board = data.board;
            currentPlayer = data.current_player;
            gameOver = data.game_over;
            // Re-enable cells if they were disabled (e.g., after a previous game ended)
            cells.forEach(cell => {
                cell.style.pointerEvents = 'auto';
            });
        } else {
            console.error("Failed to start new game:", data.error);
            gameStatusElement.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error("Network error starting new game:", error);
        gameStatusElement.textContent = "Could not connect to game server. Please ensure the Python backend (app.py) is running.";
    }
}

/**
 * Handles a click on a Tic-Tac-Toe cell.
 * Sends the selected move to the backend and updates the UI based on the response.
 * @param {Event} event - The click event object.
 */
async function handleCellClick(event) {
    const clickedCell = event.target;
    // Get the index of the clicked cell from its data-cell-index attribute
    const cellIndex = parseInt(clickedCell.dataset.cellIndex);

    // Prevent making a move if the game is already over or the cell is not empty
    if (gameOver || board[cellIndex] !== "") {
        return;
    }

    try {
        // Send the move data to the backend
        const response = await fetch(`${API_BASE_URL}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Send the cell index and the current player
            body: JSON.stringify({ cell_index: cellIndex, player: currentPlayer })
        });

        const data = await response.json();

        if (response.ok) {
            // Update the UI with the new game state from the backend
            updateUI(data.board, data.message, data.winner, data.draw);
            // Update client-side state
            board = data.board;
            currentPlayer = data.current_player;
            gameOver = data.game_over;

            // If the game is over (win or draw), disable further cell clicks
            if (gameOver) {
                 cells.forEach(cell => {
                    cell.style.pointerEvents = 'none'; // Disable interaction after game ends
                });
            }
        } else {
            // Log and display error message from the backend
            console.error("Error making move:", data.error);
            gameStatusElement.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        // Log and display network error message
        console.error("Network error making move:", error);
        gameStatusElement.textContent = "Could not connect to game server. Please ensure the Python backend (app.py) is running.";
    }
}

/**
 * Updates the visual representation of the game board and status message.
 * @param {Array<string>} newBoard - The updated board state (e.g., ["X", "", "O", ...]).
 * @param {string} message - The status message to display (e.g., "Player X's turn!").
 * @param {string | null} winner - The winning player ('X' or 'O') or null if no winner yet.
 * @param {boolean} draw - True if the game is a draw, false otherwise.
 */
function updateUI(newBoard, message, winner, draw) {
    // Iterate over each cell element and update its content and styling
    cells.forEach((cell, index) => {
        cell.textContent = newBoard[index]; // Set X or O
        cell.classList.remove('x', 'o'); // Remove old player classes
        if (newBoard[index] === 'X') {
            cell.classList.add('x'); // Add 'x' class for styling X
        } else if (newBoard[index] === 'O') {
            cell.classList.add('o'); // Add 'o' class for styling O
        }
    });

    // Update the game status message
    gameStatusElement.textContent = message;

    // Apply specific styling for win/draw messages
    gameStatusElement.classList.remove('text-green-400', 'text-yellow-400', 'text-gray-300'); // Clear all state colors
    if (winner) {
        gameStatusElement.classList.add('text-green-400'); // Green for winner
    } else if (draw) {
        gameStatusElement.classList.add('text-yellow-400'); // Yellow for draw
    } else {
        gameStatusElement.classList.add('text-gray-300'); // Default color for ongoing game
    }
}

// Add event listeners to each cell for click events
cells.forEach(cell => cell.addEventListener('click', handleCellClick));
// Add event listener to the reset button to start a new game
resetButton.addEventListener('click', initGame);

// Initialize the game automatically when the page loads
window.onload = initGame;
