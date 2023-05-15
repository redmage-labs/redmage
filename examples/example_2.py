import uvicorn

from redmage import Component, Redmage
from redmage.elements import H1, Body, Doc, Head, Html, Script, Title

app = Redmage()


class Index(Component, routes=("/",)):
    def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 2"),
                ),
                Body(
                    ChildComponent(),
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
            )
        )


class ChildComponent(Component):
    def render(self):
        return H1("Child Component")


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
