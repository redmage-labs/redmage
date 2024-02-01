import pytest

from redmage import Component, Redmage, Target
from redmage.elements import Div, Doc
from redmage.utils import astr

app = Redmage()


class TestComponent(Component):
    async def render(self):
        return Div(f"Hello World")

    @property
    def id(self) -> str:
        return f"{self.__class__.__name__}-1"

    @Target.get
    def target_method(self): ...


app.create_routes()


test_component = TestComponent()


@pytest.mark.asyncio
async def test_element():
    div = await astr(Div("test"))
    assert div.strip() == "<div>test</div>"


@pytest.mark.asyncio
async def test_element_helper_keyword():
    div = await astr(Div("test", click=test_component.target_method()))
    assert (
        div.strip()
        == '<div hx-swap="outerHTML" hx-target="#TestComponent-1" hx-get="/TestComponent/1/target_method" hx-trigger="click">test</div>'
    )


@pytest.mark.asyncio
async def test_element_append():
    div = Div()
    div.append("test")
    assert (await astr(div)).strip() == "<div>test</div>"


@pytest.mark.asyncio
async def test_element_push_url():
    div = await astr(Div("test", push_url="/test"))
    assert div.strip() == '<div hx-push-url="/test">test</div>'


@pytest.mark.asyncio
async def test_element_multiple_triggers():
    div = await astr(Div("test", trigger=("click", "mouseover")))
    assert div.strip() == '<div hx-trigger="click, mouseover">test</div>'


@pytest.mark.asyncio
async def test_element_swap_oob():
    div = await astr(Div("test", swap_oob=True))
    assert div.strip() == '<div hx-swap-oob="true">test</div>'


@pytest.mark.asyncio
async def test_element_confirm():
    div = await astr(Div("test", confirm="Are you sure?"))
    assert div.strip() == '<div hx-confirm="Are you sure?">test</div>'


@pytest.mark.asyncio
async def test_element_boost():
    div = await astr(Div("test", boost=True))
    assert div.strip() == '<div hx-boost="true">test</div>'


@pytest.mark.asyncio
async def test_element_on():
    div = await astr(Div("test", on="click"))
    assert div.strip() == '<div hx-on="click">test</div>'


@pytest.mark.asyncio
async def test_doc():
    doc = await astr(Doc(Div("test")))
    assert doc.strip() == "<!DOCTYPE html>\n<div>test</div>"


@pytest.mark.asyncio
async def test_doc_attrs():
    doc = Doc(Div("test"))
    doc.attrs(test="test")
    assert (await astr(doc)).strip() == '<!DOCTYPE html>\n<div test="test">test</div>'
