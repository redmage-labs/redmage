from dataclasses import dataclass

import uvicorn

from redmage import Component, Redmage, Target
from redmage.elements import (
    Body,
    Button,
    Div,
    Doc,
    Form,
    Head,
    Html,
    Input,
    P,
    Script,
    Title,
)

app = Redmage()


class Index(Component, routes=("/",)):
    def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 5"),
                ),
                Body(
                    MessageAndCounter("Initial message", 0),
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
            )
        )


@dataclass
class UpdateMessageForm:
    content: str


class MessageAndCounter(Component):
    content: str
    count: int

    def __init__(self, content, count):
        self.content = content
        self.count = count

    def render(self):
        return Div(
            P(f"{self.content=}"),
            Form(
                Input(
                    type="text",
                    id="content",
                    name="content",
                ),
                Button("Update message", type="submit"),
                target=self.update_message(),
            ),
            P(f"{self.count=}"),
            Button("Add 1", click=self.update_count(self.count + 1)),
        )

    @Target.post
    def update_message(self, form: UpdateMessageForm, /):
        self.content = form.content

    @Target.post
    def update_count(self, count: int):
        self.count = count


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
