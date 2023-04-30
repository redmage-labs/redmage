from redmage import Component, Redmage, Target
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
                    Script(src="https://unpkg.com/htmx.org@1.8.5"),
                ),
            )
        )


class ChildComponent(Component):
    def render(self):
        return H1("Child Component")
