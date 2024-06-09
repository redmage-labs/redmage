import uvicorn

from redmage import Component, Redmage, Target
from redmage.elements import Body, Div, Doc, Head, Html, Script, Title

app = Redmage()


class Index(Component, routes=("/",)):
    async def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 6"),
                ),
                Body(
                    HoverCount(),
                    Script(src="https://unpkg.com/htmx.org@2.0.0-beta4"),
                ),
            )
        )


class HoverCount(Component):
    def __init__(self):
        self.count = 0

    async def render(self):
        return Div(
            self.count,
            mouse_over=self.set_count(self.count + 1),
        )

    @Target.post
    def set_count(self, count: int):
        self.count = count


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
