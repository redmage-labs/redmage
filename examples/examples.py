from dataclasses import dataclass

import uvicorn

from redmage import Component, Redmage, Target
from redmage.elements import (
    H1,
    Body,
    Button,
    Div,
    Form,
    Hr,
    Html,
    Input,
    Li,
    P,
    Script,
    Table,
    Td,
    Th,
    Tr,
    Ul,
)
from redmage.triggers import DelayTriggerModifier, Trigger, TriggerModifier
from redmage.types import HTMXTrigger

app = Redmage()


class Index(Component, routes=("/",)):
    def render(self):
        return Html(
            Body(
                Examples(),
                Script(src="https://unpkg.com/htmx.org@1.9.2"),
            ),
        )


class Examples(Component):
    def render(self):
        list_component = ListComponent()

        return Div(
            Div(
                H1("Examples"),
                Hr(),
                # counter
                Counter(),
                Hr(),
                # simple form
                Message(),
                Hr(),
                # Add to a list
                list_component,
                Button("Append Item", target=list_component.append(), swap="beforeend"),
                Hr(),
                MouseOverTriggerExample(),
                Hr(),
                MouseOverTriggerExample(
                    message="I have a delay of 2 seconds",
                    delay=2000,
                ),
                Hr(),
                Confirm(),
                Hr(),
                ActiveSearch(),
                Hr(),
                # Reset
                Button("Reset", target=self.reset()),
            )
        )

    @Target.get
    def reset(self):
        # Just do nothing it will cause the component to just rerender
        # Since nothing is stored in the component state it just resets everything
        ...


class Counter(Component):
    n: int

    def __init__(self, n: int = 0):
        self.n = n

    def render(self):
        return Div(
            P(f"count={self.n}"),
            Button("Add 1", target=self.iterate(self.n + 1)),
        )

    @Target.get
    def iterate(self, n: int):
        self.n = n


class Message(Component):
    content: str

    def __init__(self, content: str = "initial message"):
        self.content = content

    @dataclass
    class UpdateMessageForm:
        content: str

    def render(self):
        return Div(
            P(f"{self.content=}" if self.content else "No message has been posted"),
            Form(
                Input(
                    type="text",
                    id="content",
                    name="content",
                ),
                Button("Update message", type="submit"),
                target=self.update_message(),  # keyword arg will be added by the form
            ),
        )

    @Target.post
    def update_message(self, form: UpdateMessageForm, /):
        self.content = form.content


@dataclass
class ListComponent(Component):
    def render(self):
        items = []
        return Ul(*[ListItemComponent(i) for i in items])

    @Target.get
    def append(self):
        item = "List Item"
        return ListItemComponent(item)


@dataclass
class ListItemComponent(Component):
    message: str

    def render(self):
        return Li(self.message)


@dataclass
class MouseOverTriggerExample(Component):
    message: str = "Hover over the button to trigger the event"
    delay: int = 0

    def render(self):
        if self.delay:
            trigger = Trigger(
                HTMXTrigger.MOUSEOVER, DelayTriggerModifier(milliseconds=self.delay)
            )
        else:
            trigger = Trigger(HTMXTrigger.MOUSEOVER)

        return Div(
            P(self.message),
            Button(
                "Trigger Event",
                target=self.trigger_event(),
                trigger=trigger,
            ),
        )

    @Target.get
    def trigger_event(self):
        self.message = "I was triggered!"
        return self


@dataclass
class Confirm(Component):
    message: str = "Click the button to trigger the event"

    def render(self):
        return Div(
            P(self.message),
            Button(
                "Trigger Confirm Event",
                target=self.trigger_event(),
                confirm="Are you sure you want to trigger the event?",
            ),
        )

    @Target.get
    def trigger_event(self):
        self.message = "I was triggered!"
        return self


@dataclass
class SearchCriteria:
    search_string: str


class ActiveSearch(Component):
    def __init__(self):
        self.search_string = ""

    def render(self):
        poeple = [
            ("John", 20),
            ("Jane", 21),
            ("Bob", 22),
            ("Alice", 23),
        ]

        return Div(
            Form(
                Input(
                    type="search",
                    id="search_string",
                    name="search_string",
                    value=self.search_string,
                    target=self.search(),
                    trigger=(
                        Trigger(
                            HTMXTrigger.KEYUP,
                            TriggerModifier(HTMXTrigger.CHANGE),
                            DelayTriggerModifier(milliseconds=500),
                        ),
                        Trigger(HTMXTrigger.SEARCH),
                    ),
                )
            ),
            Table(
                Tr(
                    Th("Name"),
                    Th("Age"),
                ),
                *[
                    Tr(Td(p[0]), Td(p[1]))
                    for p in poeple
                    if p[0].startswith(self.search_string)
                ],
            ),
        )

    @Target.post
    def search(self, search_criteria: SearchCriteria, /):
        self.search_string = search_criteria.search_string


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
