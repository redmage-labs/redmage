from enum import Enum


class Players(str, Enum):
    X = "X"
    O = "O"


class TicTacToeGameState:
    def __init__(self):
        self.reset()

    def change_turn(self):
        self.current_turn = Players.X if self.current_turn != Players.X else Players.O

    def take_turn(self, x, y):
        self.board_state[int(x)][int(y)] = self.current_turn
        game_over = self.is_over()
        draw = self.is_draw()
        if not game_over and not draw:
            self.change_turn()

        return game_over, draw

    def is_over(self):
        return any(
            [
                all([self.board_state[0][x] == self.current_turn for x in range(3)]),
                all([self.board_state[1][x] == self.current_turn for x in range(3)]),
                all([self.board_state[2][x] == self.current_turn for x in range(3)]),
                all([self.board_state[x][0] == self.current_turn for x in range(3)]),
                all([self.board_state[x][1] == self.current_turn for x in range(3)]),
                all([self.board_state[x][2] == self.current_turn for x in range(3)]),
                all([self.board_state[x][x] == self.current_turn for x in range(3)]),
                all(
                    [self.board_state[x][2 - x] == self.current_turn for x in range(3)]
                ),
            ]
        )

    def is_draw(self):
        return all(all(v for v in row) for row in self.board_state)

    def reset(self):
        self.current_turn = Players.X
        self.board_state = [["" for _ in range(3)] for _ in range(3)]
