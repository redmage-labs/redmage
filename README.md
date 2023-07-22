# redmage

[![run-tests](https://github.com/redmage-labs/redmage/actions/workflows/main.yaml/badge.svg)](https://github.com/redmage-labs/redmage/actions/workflows/main.yaml)

Redmage is component based library for building [htmx](https://htmx.org/) powered web applications.

It is built on top of the [starlette](https://www.starlette.io/) web framework.

## Example

Redmage is meant to reduce the complexity of designing htmx powered applications by abstracting the need to explicitly register routes and configure the hx-* attributes for each interaction on your app.

Consider the example below.

```
from redmage import Component, Redmage, Target
from redmage.elements import Button, Div, H1, Script


app = Redmage()


class Counter(Component, routes=("/",)):
    count: int

    def __init__(self):
        self.count = 0

    async def render(self):
        return Div(
            H1(f"Clicked {self.count} times."),
            Button(
                "Add 1",
                click=self.add_one(),
            ),
            Script(src="https://unpkg.com/htmx.org@1.9.2"),
        )

    @Target.post
    def add_one(self):
        self.count += 1
```

The **Counter** component will add one to the count every time the button is clicked. If you're familiar with htmx, you might notice that this would usually require registering a new route in our backend, maybe something like _/add_one_. And in the html, we would have to explicitly add an **hx-post**, **hx-target**, and possibly more **hx-\*** attributes.

Redmage abstracts this using the **Target.post** decorator method. To the developer it simply looks like the _add_one_ method is executed when the button is clicked which updates the component state and causes the component to re-render.

## Installation


Redmage is available on pypi.

```
pip install redmage
```

## Redmage application


The first thing you need to do is create an instance of the Redmage class.

```
from redmage import Redmage


app = Redmage()
```

At this point our app won't do anything because we haven't registered any routes by sublassing Component. But you can start it up using your favorite ASGI server like uvicorn.

```
uvicorn <module>:<filename>:app.starlette
```

### Application Options

You can pass the following keyword arguments to the Redmage constructor which  work as proxies to the underlying Starlette app.

* debug
* middleware

## First Component


Let's create a Component. In the example we just returned a **div** element. This works but we're going to want to create a proper html page with **html**, **header**, **body** tags etc.

```
from redmage import Component, Redmage
from redmage.elements import Body, Doc, H1, Head, Html, Script, Title


app = Redmage()


class Index(Component, routes=("/",)):

    async def render(self):
        return Doc(
            Html(
                Head(
                    Title("Example"),
                ),
                Body(
                    H1("Hello Redmage"),
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
            )
        )
```

This tells our app to register the **Index** component with the route "/". When you navigate to _localhost:8000/_ an instance of **Index** will be created and it's render method will be called to generate the html.

The **Component** class is abstract and has a single abstract base method, **render**, that must be implemented and return and instance of **redmage.elements.Element**.


## Elements

Redmage internally uses python classes associated with each html tag (**Div**, **Body**, **H1** etc.). They can all be imported from **redmage.elements**. Each of these classes subclasses **redmage.elements.Element**. Pass the elements inner html as positional arguments and add attributes with keyword arguments.

```
from redmage.elements import Div


div = Div(
    H1("Title"),
    P("paragraph"),
    my_attribute="a cool attribute value"
    _class="my-class"
)


print(div)


# output
# <div my-attribute="a cool attribute value" class="my-class">
#    <h1>Title</h1>
#    <p>paragraph</p>
# </div>
```

Notice that underscores in keywords are converted to hyphens and leading underscores are stripped so you can avoid conflict with Python keywords like class.

Additionally, a number of htmx specific keywords are supported.

| keyword     | htmx attribute                       | type           | default             | documentation | notes                              |
|-------------|--------------------------------------|----------------|---------------------|---------------|------------------------------------|
| trigger     | hx-trigger                           | str or Trigger | None                |               | See Trigger section below          |
| swap        | hx-swap                              | str            | HTMXSwap.OUTER_HTML |               | redmage.types.HTMXSwap enum        |
| swap_oob    | hx-swap-oob                          | bool           | False               |               |                                    |
| confirm     | hx-confirm                           | bool           | False               |               |                                    |
| boost       | hx-boost                             | bool           | False               |               |                                    |
| on          | hx-on                                | str            | None                |               |                                    |
| indicator   | N/A                                  | bool           | False               |               |                                    |
| target      | hx-target, hx-\<method\>             | Target         | None                |               | See Target section below           |
| click       | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| submit      | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| change      | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| mouse_over  | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| mouse_enter | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| load        | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| intersect   | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |
| revealed    | hx-target, hx-\<method\>, hx-trigger | Target         | None                |               | See Trigger keywords section below |

 > Redmage doesn't have any support for a specific template engine, but it should be pretty easy to build a **Component** subclass to support one, such as Jinja2. See the todo_jinja2 example.


## Nesting Components


Components can be easily nested by using them just like you would use any other html **Element** object.

```
from redmage import Redmage
from redmage.elements import Body, Doc, H1, Head, Html, Script, Title


app = Redmage()


class Index(Component, routes=("/",)):

    async def render(self):
        return Doc(
            Html(
                Head(
                    Title("Todo App"),
                ),
                Body(
                    ChildComponent(),
                    Script(src="https://unpkg.com/htmx.org@1.9.2"),
                ),
            )
        )


class ChildComponent(Component):

    async def render(self):
        return H1("Child Component")

```

> In the following examples I'm going to assume that the components we write are rendered in an **Index** component like above so it will be ommited.


## Targets

[htmx targets](https://htmx.org/docs/#targets)

### Simple Example

Thus far, our components have been static. With Redmage we have the ability to react to events on the frontend and update the state of our component using htmx. To do, this we use **redmage.Target** class. It has decorator attributes associated with the following HTTP methods.

* get
* post
* put
* patch
* delete

These decorators wrap methods of our component. We can pass the output of these methods to an Element's **target** keyword argument. Check out the example below.

```
from redmage import Target


class ClickComponent(Component):

    def __init__(self):
        self.count = 0

    async def render(self):
        return Button(
            self.count,
            target=self.set_count(self.count + 1)
        )

    @Target.post
    def set_count(self, count: int):
        self.count = count
```

When the button is clicked an HTTP POST request is issued to our application. The **set_count** method is ran, updating the component state, and the component is re-rendered and swapped into the DOM.

By default, if the target method returns **None** then **self** is rendered. We could also explicitly return self, another component, or a tuple of components (this can be useful in conjunction with out of bounds swaps).

### Target method arguments

All of the arguments of a render method, except **self**, require type hints so that Redmage can build a route. Positional or keyword (and keyword only) arguments are added to the route as path arguments or query parameters respectively.

If the request has a body, the first argument must be a [positional only argument](https://peps.python.org/pep-0570/). It's type must be a class that de-serializes the body by passing the fields as keyword arguments to it's constructor, like a dataclass.

```
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
```

Redmage (and the underlying starlette app) must know how to convert your types to strings so that they can be encoded in URLs and converted back to your object types.

Use the starlette app to register your custom converters according to it's [documentation](https://www.starlette.io/routing/). Redmage will use these converters.

> Redmage adds a couple of custom convertors that starlette does not provide. One is a boolean converter to convert **bool** type. The other is a custom string converter that is used for **str**. Since Redmage building URLs we need to convert the empty string to _\_\_empty\_\__.

### Component State

The component's state will also be encoded in the url so it can be recreated when the request is issued. Only attributes that have a class annotation will be included. The same converters described above will be used to serialize/de-serialize the component's attributes.

```
@dataclass
class UpdateMessageForm:
    content: str


class MessageAndCounter(Component):
    content: str
    count: int

    def __init__(self, content, count):
        self.content = content
        self.count = count

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
            P(f"{self.count=}"),
            Button("Add 1", click=self.update_count(self.count + 1)),
        )

    @Target.post
    def update_message(self, form: UpdateMessageForm, /):
        self.content = form.content

    @Target.post
    def update_count(self, count: int):
        self.count = count  
```

In this example, if we didn't add the class annotations, when the message was updated the count would not be set and vice versa, breaking our component.

## Triggers

[htmx triggers](https://htmx.org/docs/#triggers)

Redmage provides a very thin abstraction over _hx-trigger_ attributes. An element's **trigger** keyword argument can be used to tell Redamge which event type should trigger a component update. You can just pass a string value of the [event](https://developer.mozilla.org/en-US/docs/Web/Events) name.

```
class HoverCount(Component):
    def __init__(self):
        self.count = 0

    async def render(self):
        return Div(
            self.count,
            target=self.set_count(self.count + 1),
            trigger="mouseover",
        )

    @Target.post
    def set_count(self, count: int):
        self.count = count
```

Now when you mouse over the number the count increases by one. Check the htmx documentation because it provides a number of modifiers that can be used to customize the trigger behavior.

Redmage has built-in classes that can be used to build triggers as well.

* **redmage.triggers.Trigger**
* **redmage.triggers.TriggerModifier**
* **redmage.triggers.DelayTriggerModifier**
* **redmage.triggers.ThrottleTriggerModifier**

> TODO document redmage.triggers.* classes.

Below is an example of using **Trigger** classes to add a delay to a trigger.

```
from redmage.triggers import DelayTriggerModifier, Trigger
from redmage.types import HTMXTrigger


class HoverCount(Component):
    def __init__(self):
        self.count = 0

    async def render(self):
        trigger = Trigger(HTMXTrigger.MOUSEOVER, DelayTriggerModifier(1000))

        return Div(
            self.count, target=self.set_count(self.count + 1), trigger=trigger
        )

    @Target.post
    def set_count(self, count: int):
        self.count = count
```

Now the count will update after one second instead of immediately.

## Trigger keywords

The **Element** class has a number of keyword arguments associated with events that we can pass **Target** objects too. This can simplify our code by not having to add both target and trigger keyword arguments. Below is an example.

```
class HoverCount(Component):
    def __init__(self):
        self.count = 0

    async def render(self):
        return Div(
            self.count,
            mouse_over=self.set_count(self.count + 1),
        )

    @Target.post
    def set_count(self, count: int):
        self.count = count
```

The **Element** class currently provides keyword arguments for the following events:

* click
* submit
* change
* mouse_over
* mouse_enter
* load
* intersect
* revealed


## Render Extensions

We can use render extensions to inject objects as positional arguments to each **render** method in our application.

> TODO give an example of how to register a render extension and when you might use one.


## Examples

> TODO add cool examples.
