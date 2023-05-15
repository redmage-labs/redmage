import uvicorn

from redmage import Component, Redmage, Target
from redmage.elements import Body, Div, Doc, Head, Html, Script, Title
from redmage.triggers import DelayTriggerModifier, Trigger
from redmage.types import HTMXTrigger

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
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
            )
        )


class HoverCount(Component):
    def __init__(self):
        self.count = 0

    def render(self):
        trigger = Trigger(HTMXTrigger.MOUSEOVER, DelayTriggerModifier(1000))

        return Div(self.count, target=self.set_count(self.count + 1), trigger=trigger)

    @Target.post
    def set_count(self, count: int):
        self.count = count


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
