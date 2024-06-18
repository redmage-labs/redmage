import uvicorn

from redmage import Component, Redmage
from redmage.elements import H1, Body, Doc, Head, Html, Script, Title

app = Redmage()


class Index(Component, routes=("/",)):
    async def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 1"),
                ),
                Body(
                    H1("Hello Redmage"),
                    Script(src="https://unpkg.com/htmx.org@2.0.0/dist/htmx.min.js"),
                ),
            )
        )


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
