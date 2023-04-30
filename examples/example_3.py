from redmage import Component, Redmage, Target
from redmage.elements import Body, Button, Doc, Head, Html, Script, Title

app = Redmage()


class Index(Component, routes=("/",)):
    def render(self):
        return Doc(
            Html(
                Head(Title("Redmage | Example 3")),
                Body(
                    ClickComponent(),
                    Script(src="https://unpkg.com/htmx.org@1.8.5"),
                ),
            )
        )


class ClickComponent(Component):
    def __init__(self):
        self.count = 0

    def render(self):
        return Button(self.count, target=self.set_count(self.count + 1))

    @Target.post
    def set_count(self, count: int):
        self.count = count
