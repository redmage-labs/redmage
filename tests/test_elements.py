from redmage import Component, Redmage, Target
from redmage.elements import Div, Doc

app = Redmage()


class TestComponent(Component):
    def render(self):
        return Div(f"Hello World")

    @property
    def id(self) -> str:
        return f"{self.__class__.__name__}-1"

    @Target.get
    def target_method(self):
        ...


app.create_routes()


test_component = TestComponent()


def test_element():
    div = Div("test")
    assert str(div).strip() == "<div>test</div>"


def test_element_helper_keyword():
    div = Div("test", click=test_component.target_method())
    assert (
        str(div).strip()
        == '<div hx-swap="outerHTML" hx-target="#TestComponent-1" hx-get="/TestComponent/1/target_method" hx-trigger="click">test</div>'
    )


def test_element_append():
    div = Div()
    div.append("test")
    assert str(div).strip() == "<div>test</div>"


def test_element_push_url():
    div = Div("test", push_url="/test")
    assert str(div).strip() == '<div hx-push-url="/test">test</div>'


def test_element_multiple_triggers():
    div = Div("test", trigger=("click", "mouseover"))
    assert str(div).strip() == '<div hx-trigger="click, mouseover">test</div>'


def test_element_swap_oob():
    div = Div("test", swap_oob=True)
    assert str(div).strip() == '<div hx-swap-oob="true">test</div>'


def test_element_confirm():
    div = Div("test", confirm="Are you sure?")
    assert str(div).strip() == '<div hx-confirm="Are you sure?">test</div>'


def test_element_boost():
    div = Div("test", boost=True)
    assert str(div).strip() == '<div hx-boost="true">test</div>'


def test_element_on():
    div = Div("test", on="click")
    assert str(div).strip() == '<div hx-on="click">test</div>'


def test_doc():
    doc = Doc(Div("test"))
    assert str(doc).strip() == "<!DOCTYPE html>\n<div>test</div>"


def test_doc_attrs():
    doc = Doc(Div("test"))
    doc.attrs(test="test")
    assert str(doc).strip() == '<!DOCTYPE html>\n<div test="test">test</div>'
