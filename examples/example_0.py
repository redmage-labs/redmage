import uvicorn

from redmage import Component, Redmage, Target
from redmage.elements import H1, Button, Div, Script

app = Redmage()


class Counter(Component, routes=("/",)):
    count: int

    def __init__(self):
        self.count = 0

    async def render(self):
        return Div(
            H1(f"Clicked {self.count} times."),
            Button(
                "Add 1",
                click=self.add_one(),
            ),
            Script(src="https://unpkg.com/htmx.org@1.9.2"),
        )

    @Target.post
    def add_one(self):
        self.count += 1


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
