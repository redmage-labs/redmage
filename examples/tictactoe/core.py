from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from redmage import Component, Redmage, Target
from redmage.elements import Body, Button, Div, Head, Html, Link, P, Script

from .game import Players, TicTacToeGameState

app = Redmage()


app.routes.append(
    Mount(
        "/static",
        app=StaticFiles(directory="./examples/tictactoe/static"),
        name="static",
    )
)


game = TicTacToeGameState()


class Index(Component, routes=("/",)):
    def render(self):
        return Html(
            Head(
                Link(
                    rel="stylesheet",
                    href="static/ttt.css",
                ),
            ),
            Body(
                Board(),
                Script(src="https://unpkg.com/htmx.org@1.9.2"),
            ),
        )


class Board(Component):
    def __init__(self):
        self.game_over = False
        self.draw = False

    def render(self):
        squares = []
        for i, row in enumerate(game.board_state):
            for j, cell in enumerate(row):
                squares.append(square(self, i, j, cell, self.game_over or self.draw))

        if self.game_over:
            message_content = f"game over, {game.current_turn} won!"
        elif self.draw:
            message_content = f"Game is a draw!"
        else:
            message_content = f"current turn: {game.current_turn}"

        el = Div(
            Div(
                *squares,
                _class="board",
            ),
            P(message_content),
        )

        if self.game_over or self.draw:
            el.append(Button("Restart Game", target=self.reset()))

        return el

    @Target.get
    def reset(self):
        self.game_over = False
        self.draw = False
        game.reset()

    @Target.get
    def move(self, x: int, y: int):
        game_over, draw = game.take_turn(x, y)
        self.game_over = game_over
        self.draw = draw


def square(board, x, y, val, disable):
    disable = True if disable or val in (Players.X, Players.O) else False
    cell_style = f"grid-row: {x + 1}; grid-column: {y + 1};"
    cell_val = f"{val}"

    div = Div(
        cell_val,
        style=cell_style,
        _class="square",
    )

    if not disable:
        div.target = board.move(x, y)

    return div
