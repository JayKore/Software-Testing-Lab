# Author: aqeelanwar
# Modified to support custom player names

from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50

# Player colours
symbol_X_color = '#EE4035'   # Red
symbol_O_color = '#0492CF'   # Blue
Green_color = '#7BC043'


class Tic_Tac_Toe():

    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------

    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.resizable(False, False)

        # Default player names
        self.player_X_name = "Player 1"
        self.player_O_name = "Player 2"

        # Scores
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        # Game state
        self.player_X_starts = True
        self.player_X_turns = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        # Ask for player names before starting the game
        self.create_name_screen()

    # ------------------------------------------------------------------
    # Player Name Screen:
    # ------------------------------------------------------------------

    def create_name_screen(self):

        self.name_frame = Frame(self.window, padx=40, pady=40)
        self.name_frame.pack()

        title = Label(
            self.name_frame,
            text="Tic-Tac-Toe",
            font=("Arial", 28, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Player X
        Label(
            self.name_frame,
            text="Player 1 (X)",
            font=("Arial", 16, "bold"),
            fg=symbol_X_color
        ).grid(row=1, column=0, pady=10, padx=10)

        self.X_name_entry = Entry(
            self.name_frame,
            font=("Arial", 14),
            width=20
        )
        self.X_name_entry.grid(row=1, column=1, pady=10)

        # Player O
        Label(
            self.name_frame,
            text="Player 2 (O)",
            font=("Arial", 16, "bold"),
            fg=symbol_O_color
        ).grid(row=2, column=0, pady=10, padx=10)

        self.O_name_entry = Entry(
            self.name_frame,
            font=("Arial", 14),
            width=20
        )
        self.O_name_entry.grid(row=2, column=1, pady=10)

        # Start button
        start_button = Button(
            self.name_frame,
            text="Start Game",
            font=("Arial", 14, "bold"),
            command=self.start_game,
            width=15
        )
        start_button.grid(row=3, column=0, columnspan=2, pady=(25, 10))

        Label(
            self.name_frame,
            text="Leave a name empty to use Player 1 / Player 2",
            font=("Arial", 10),
            fg="gray"
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # Put cursor in first field
        self.X_name_entry.focus()

    def start_game(self):

        # Get names entered by the users
        X_name = self.X_name_entry.get().strip()
        O_name = self.O_name_entry.get().strip()

        # Use default names if fields are empty
        self.player_X_name = X_name if X_name else "Player 1"
        self.player_O_name = O_name if O_name else "Player 2"

        # Remove name screen
        self.name_frame.destroy()

        # Create the game canvas
        self.canvas = Canvas(
            self.window,
            width=size_of_board,
            height=size_of_board
        )
        self.canvas.pack()

        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        # Initialize game
        self.initialize_board()

        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False

        self.update_window_title()

    # ------------------------------------------------------------------
    # Game Setup:
    # ------------------------------------------------------------------

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):

        for i in range(2):
            self.canvas.create_line(
                (i + 1) * size_of_board / 3,
                0,
                (i + 1) * size_of_board / 3,
                size_of_board
            )

        for i in range(2):
            self.canvas.create_line(
                0,
                (i + 1) * size_of_board / 3,
                size_of_board,
                (i + 1) * size_of_board / 3
            )

    def update_window_title(self):

        if self.player_X_turns:
            self.window.title(
                f"Tic-Tac-Toe - {self.player_X_name} (X) Turn"
            )
        else:
            self.window.title(
                f"Tic-Tac-Toe - {self.player_O_name} (O) Turn"
            )

    def play_again(self):

        self.initialize_board()

        # Alternate who starts each round
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts

        self.board_status = np.zeros(shape=(3, 3))

        self.X_wins = False
        self.O_wins = False
        self.tie = False

        self.update_window_title()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):

        logical_position = np.array(logical_position)

        grid_position = self.convert_logical_to_grid_position(
            logical_position
        )

        self.canvas.create_oval(
            grid_position[0] - symbol_size,
            grid_position[1] - symbol_size,
            grid_position[0] + symbol_size,
            grid_position[1] + symbol_size,
            width=symbol_thickness,
            outline=symbol_O_color
        )

    def draw_X(self, logical_position):

        grid_position = self.convert_logical_to_grid_position(
            logical_position
        )

        self.canvas.create_line(
            grid_position[0] - symbol_size,
            grid_position[1] - symbol_size,
            grid_position[0] + symbol_size,
            grid_position[1] + symbol_size,
            width=symbol_thickness,
            fill=symbol_X_color
        )

        self.canvas.create_line(
            grid_position[0] - symbol_size,
            grid_position[1] + symbol_size,
            grid_position[0] + symbol_size,
            grid_position[1] - symbol_size,
            width=symbol_thickness,
            fill=symbol_X_color
        )

    # ------------------------------------------------------------------
    # Game Over Display:
    # ------------------------------------------------------------------

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = f'Winner: {self.player_X_name} (X)'
            color = symbol_X_color

        elif self.O_wins:
            self.O_score += 1
            text = f'Winner: {self.player_O_name} (O)'
            color = symbol_O_color

        else:
            self.tie_score += 1
            text = "It's a tie"
            color = "gray"

        self.canvas.delete("all")

        # Winner message
        self.canvas.create_text(
            size_of_board / 2,
            size_of_board / 3,
            font="Arial 40 bold",
            fill=color,
            text=text
        )

        # Score heading
        self.canvas.create_text(
            size_of_board / 2,
            5 * size_of_board / 8,
            font="Arial 30 bold",
            fill=Green_color,
            text="Scores"
        )

        # Player scores
        score_text = (
            f'{self.player_X_name} (X): {self.X_score}\n'
            f'{self.player_O_name} (O): {self.O_score}\n'
            f'Ties: {self.tie_score}'
        )

        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 4,
            font="Arial 24 bold",
            fill=Green_color,
            text=score_text
        )

        self.reset_board = True

        # Play again message
        self.canvas.create_text(
            size_of_board / 2,
            15 * size_of_board / 16,
            font="Arial 18 bold",
            fill="gray",
            text="Click anywhere to play again"
        )

    # ------------------------------------------------------------------
    # Logical Functions:
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):

        logical_position = np.array(
            logical_position,
            dtype=int
        )

        return (
            (size_of_board / 3) * logical_position
            + size_of_board / 6
        )

    def convert_grid_to_logical_position(self, grid_position):

        grid_position = np.array(grid_position)

        return np.array(
            grid_position // (size_of_board / 3),
            dtype=int
        )

    def is_grid_occupied(self, logical_position):

        if self.board_status[
            logical_position[0]
        ][
            logical_position[1]
        ] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Check rows and columns
        for i in range(3):

            if (
                self.board_status[i][0]
                == self.board_status[i][1]
                == self.board_status[i][2]
                == player
            ):
                return True

            if (
                self.board_status[0][i]
                == self.board_status[1][i]
                == self.board_status[2][i]
                == player
            ):
                return True

        # Check diagonals
        if (
            self.board_status[0][0]
            == self.board_status[1][1]
            == self.board_status[2][2]
            == player
        ):
            return True

        if (
            self.board_status[0][2]
            == self.board_status[1][1]
            == self.board_status[2][0]
            == player
        ):
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)

        if len(r) == 0:
            return True

        return False

    def is_gameover(self):

        self.X_wins = self.is_winner('X')

        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = (
            self.X_wins
            or self.O_wins
            or self.tie
        )

        return gameover

    # ------------------------------------------------------------------
    # Click Function:
    # ------------------------------------------------------------------

    def click(self, event):

        grid_position = [event.x, event.y]

        logical_position = self.convert_grid_to_logical_position(
            grid_position
        )

        # Make sure click is inside the board
        if (
            logical_position[0] < 0
            or logical_position[0] > 2
            or logical_position[1] < 0
            or logical_position[1] > 2
        ):
            return

        if not self.reset_board:

            # Player X's turn
            if self.player_X_turns:

                if not self.is_grid_occupied(logical_position):

                    self.draw_X(logical_position)

                    self.board_status[
                        logical_position[0]
                    ][
                        logical_position[1]
                    ] = -1

                    self.player_X_turns = False

            # Player O's turn
            else:

                if not self.is_grid_occupied(logical_position):

                    self.draw_O(logical_position)

                    self.board_status[
                        logical_position[0]
                    ][
                        logical_position[1]
                    ] = 1

                    self.player_X_turns = True

            # Update the title to show whose turn it is
            self.update_window_title()

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()

        else:

            # Start a new round
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


# ------------------------------------------------------------------
# Start Game
# ------------------------------------------------------------------

game_instance = Tic_Tac_Toe()
game_instance.mainloop()