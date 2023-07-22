from starlette.convertors import Convertor, register_url_convertor
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from examples.todo import db
from redmage import Component, Redmage, Target
from redmage.elements import (
    A,
    Body,
    Button,
    Div,
    Doc,
    Form,
    Head,
    Html,
    Img,
    Input,
    Li,
    Link,
    Nav,
    S,
    Script,
    Strong,
    Textarea,
    Title,
    Ul,
)

app = Redmage()


app.routes.append(
    Mount(
        "/static",
        app=StaticFiles(directory="./examples/todo/static"),
        name="static",
    )
)


class RouteConvertor(Convertor):
    regex = "add|edit|list"

    def convert(self, value: str) -> str:
        return value

    def to_string(self, value: str) -> str:
        return value


register_url_convertor("route", RouteConvertor())


class TodoAppComponent(
    Component,
    routes=(
        "/",
        "/{route:route}",
        "/{route:route}/{todo_id:int}",
    ),
):
    def __init__(self, route: str = "list", todo_id: int = 0):
        self.todo_id = todo_id
        self.route = route
        self.router_component = TodoRouterComponent(self.route, self.todo_id)

    async def render(self):
        return Doc(
            Html(
                Head(
                    Title("Todo App"),
                    Link(
                        rel="stylesheet",
                        href="https://unpkg.com/@picocss/pico@1.*/css/pico.min.css",
                    ),
                ),
                Body(
                    self.router_component,
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
                data_theme="dark",
            )
        )


class TodoRouterComponent(Component):
    def __init__(self, route: str, todo_id: int = 0) -> None:
        self.route = route
        self.todo_id = todo_id
        Component.add_render_extension(router=self.router)

    @classmethod
    def get_route(cls, route: str, todo_id: int = 0):
        if route == "list":
            route_comp = TodoListComponent()
        elif route == "edit":
            route_comp = TodoEditComponent(todo_id)
        elif route == "add":
            route_comp = TodoAddComponent()
        else:
            raise RuntimeError(f"Unknown route: {route}")

        return route_comp

    async def render(self):
        return Div(
            TodoHeaderComponent(),
            self.get_route(self.route, self.todo_id),
            _class="container",
        )

    @Target.get
    def router(self, route: str, todo_id: int = 0):
        self.route = route
        self.todo_id = todo_id
        return self


class TodoHeaderComponent(Component):
    async def render(self, router):
        return Nav(
            Ul(
                Li(Strong("Todo App")),
            ),
            Ul(
                Li(
                    A(
                        "Todo List",
                        href="javascript:void(0);",
                        click=router("list"),
                        push_url="/",
                    ),
                ),
                Li(
                    A(
                        "Add Todo",
                        href="javascript:void(0);",
                        click=router("add"),
                        push_url="/add",
                    ),
                ),
            ),
        )


class TodoListComponent(Component):
    async def render(self, router):
        return Ul(
            *[
                Li(
                    Form(
                        Input(
                            type="checkbox",
                            checked=todo.finished,
                            click=self.toggle(todo.id),
                        ),
                        style="display: inline;",
                    ),
                    A(
                        todo.message if not todo.finished else S(todo.message),
                        href="javascript:void(0);",
                        click=router("edit", todo_id=todo.id),
                        push_url=f"/edit/{todo.id}",
                        style="display: inline;",
                    ),
                    A(
                        Img(src="/static/images/trash-2.svg"),
                        href="javascript:void(0);",
                        click=self.delete_todo(todo.id),
                        style="display: inline;",
                        confirm="Are you sure you want to delete this todo?",
                    ),
                )
                for todo in db.get_todos()
            ],
        )

    @Target.delete
    def delete_todo(self, todo_id: int):
        db.delete_todo(todo_id)
        return TodoRouterComponent.get_route("list")

    @Target.put
    def toggle(self, /, todo_id: int):
        todo = db.get_todo(todo_id)
        db.update_todo(todo.id, todo.message, not todo.finished)
        return TodoRouterComponent.get_route("list")


class TodoAddComponent(Component):
    async def render(self):
        return Form(
            Textarea(type="text", name="message", rows=5),
            Button("Add", type="submit", click=self.add_todo(), push_url="/"),
        )

    @Target.post
    def add_todo(self, todo: db.Todo, /):
        db.create_todo(todo.message, False)
        return TodoRouterComponent.get_route("list")


class TodoEditComponent(Component):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id

    @property
    def todo(self):
        if not hasattr(self, "_todo"):
            self._todo = db.get_todo(self.todo_id)
        return self._todo

    async def render(self):
        return Form(
            Textarea(self.todo.message, type="text", name="message", rows=5),
            Button(
                "Edit", type="submit", click=self.edit_todo(self.todo_id), push_url="/"
            ),
        )

    @Target.put
    def edit_todo(self, todo: db.Todo, /, todo_id: int):
        self.todo_id = todo_id
        db.update_todo(todo_id, todo.message, self.todo.finished)
        return TodoRouterComponent.get_route("list")
