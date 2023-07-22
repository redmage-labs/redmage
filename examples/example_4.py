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
    async def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 4"),
                ),
                Body(
                    Message("Initial message"),
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
            )
        )


@dataclass
class UpdateMessageForm:
    content: str


class Message(Component):
    def __init__(self, content):
        self.content = content

    async def render(self):
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
        )

    @Target.post
    def update_message(self, form: UpdateMessageForm, /):
        self.content = form.content


if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
