from redmage import Component, Redmage, Target
from redmage.elements import Body, Div, Doc, Head, Html, Script, Title

app = Redmage()


class Index(Component, routes=("/",)):
    def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 6"),
                ),
                Body(
                    HoverCount(),
                    Script(src="https://unpkg.com/htmx.org@1.8.5"),
                ),
            )
        )


class HoverCount(Component):
    def __init__(self):
        self.count = 0

    def render(self):
        return Div(
            self.count, target=self.set_count(self.count + 1), trigger="mouseover"
        )

    @Target.post
    def set_count(self, count: int):
        self.count = count
