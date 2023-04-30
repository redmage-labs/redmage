from abc import ABC, abstractmethod

from jinja2 import Template
from starlette.convertors import Convertor, register_url_convertor
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from examples.todo import db
from redmage import Component, Redmage, Target, elements

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


class Jinja2Component(Component, ABC):
    template: str
    jinja2_components = {}

    def __init_subclass__(cls, routes=None, **kwargs):
        Jinja2Component.jinja2_components[cls.__name__] = cls
        return super().__init_subclass__(routes=routes, **kwargs)

    @abstractmethod
    def template(self) -> str:
        ...

    def set_element_id(self, el):
        # Manually add the id in the template
        return el

    def render(self, **exts):
        template = Template(self.template)
        output = template.render(
            component=self,
            db=db,
            **{**exts, **elements.__dict__, **Jinja2Component.jinja2_components},
        )
        return output


class TodoAppComponent(
    Jinja2Component,
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

    template = """
        <html id="{{ component.id }}" data-theme="dark">
            <head>
                <title>Todo Jinja2 App</title>
                <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@1.*/css/pico.min.css">
            </head>
            <body>
                {{ component.router_component }}
            </body>
            <script src="https://unpkg.com/htmx.org@1.8.5"></script>
        </html>
    """


class TodoRouterComponent(Jinja2Component):
    def __init__(self, route: str, todo_id: int = 0) -> None:
        self.route = route
        self.todo_id = todo_id
        Component.add_render_extension(router=self.router)

    @classmethod
    def get_route(cls, route: str, todo_id: int = 0):
        match route:
            case "list":
                route = TodoListComponent()
            case "edit":
                route = TodoEditComponent(todo_id)
            case "add":
                route = TodoAddComponent()
            case _:
                raise RuntimeError(f"Unknown route: {route}")

        return route

    template = """
        <div id="{{ component.id }}" class="container">
            {{ TodoHeaderComponent() }}
            {{ component.get_route(component.route, component.todo_id) }}
        </div>
    """

    @Target.get
    def router(self, route: str, todo_id: int = 0):
        self.route = route
        self.todo_id = todo_id
        return self


class TodoHeaderComponent(Jinja2Component):
    template = """
        <nav id="{{ component.id }}">
            <ul>
                <li><strong>Todo App</strong></li>
            </ul>
            <ul>
                <li>
                    {{ A("Todo List", href="javascript:void(0);", click=router("list"), push_url="/") }}
                </li>
                <li>
                    {{ A("Add Todo", href="javascript:void(0);", click=router("add"), push_url="/add") }}
                </li>
            </ul>
        </nav>
    """


class TodoListComponent(Jinja2Component):
    template = """
        <ul id="{{ component.id }}">
        {% for todo in db.get_todos() %}
            <li>
                <form style="display: inline;">
                    {{ Input(type="checkbox", checked=todo.finished, target=component.toggle(todo.id)) }}
                </form>
                {{ 
                  A(
                    todo.message if not todo.finished else S(todo.message),
                    href="javascript:void(0);",
                    click=router("edit", todo_id=todo.id),
                    push_url="/edit/" ~ todo.id,
                    style="display: inline;",
                )
                }}
                {{
                  A(
                    Img(src="/static/images/trash-2.svg"),
                    href="javascript:void(0);",
                    click=component.delete_todo(todo.id),
                    style="display: inline;",
                    confirm="Are you sure you want to delete this todo?",
                  )
                }}
            </li>
        {% endfor %}
        </ul>
    """

    @Target.delete
    def delete_todo(self, todo_id: int):
        db.delete_todo(todo_id)
        return TodoRouterComponent.get_route("list")

    @Target.put
    def toggle(self, /, todo_id: int):
        todo = db.get_todo(todo_id)
        db.update_todo(todo.id, todo.message, not todo.finished)
        return TodoRouterComponent.get_route("list")


class TodoAddComponent(Jinja2Component):
    template = """
        <form id="{{ component.id }}">
            {{ Textarea(type="text", name="message", rows=5) }}
            {{ Button("Add", type="submit", target=component.add_todo(), push_url="/") }}
        </form>
    """

    @Target.post
    def add_todo(self, todo: db.Todo, /):
        db.create_todo(todo.message, False)
        return TodoRouterComponent.get_route("list")


class TodoEditComponent(Jinja2Component):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id

    @property
    def todo(self):
        if not hasattr(self, "_todo"):
            self._todo = db.get_todo(self.todo_id)
        return self._todo

    template = """
        <form id="{{ component.id }}">
            {{ Textarea(component.todo.message, type="text", name="message", rows=5) }}
            {{ Button("Edit", type="submit", click=component.edit_todo(component.todo_id), push_url="/") }}
        </div>
    """

    @Target.put
    def edit_todo(self, todo: db.Todo, /, todo_id: int):
        self.todo_id = todo_id
        db.update_todo(todo_id, todo.message, self.todo.finished)
        return TodoRouterComponent.get_route("list")
