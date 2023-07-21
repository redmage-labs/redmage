from typing import Optional, Tuple, Type, Union

import hype.asyncio as hype

from . import Component
from .targets import Target
from .triggers import Trigger
from .types import HTMXClass, HTMXSwap, HTMXTrigger
from .utils import astr


class Element:
    el: Type[hype.Element]

    def __init__(
        self,
        *content: Union[str, hype.Element, Component],
        # hx-* attributes
        swap: str = HTMXSwap.OUTER_HTML,
        target: Optional[Target] = None,
        trigger: Union[Trigger, Tuple[Trigger, ...]] = (),
        swap_oob: bool = False,
        confirm: Optional[str] = None,
        boost: bool = False,
        push_url: Optional[str] = None,
        indicator: bool = False,
        on: Optional[str] = None,
        # helper target+trigger combos
        click: Optional[Target] = None,
        submit: Optional[Target] = None,
        change: Optional[Target] = None,
        mouse_over: Optional[Target] = None,
        mouse_enter: Optional[Target] = None,
        load: Optional[Target] = None,
        intersect: Optional[Target] = None,
        revealed: Optional[Target] = None,
        **kwargs: str,
    ):
        # use the render method if it's component
        def _async_helper(foo):  # type: ignore
            async def inner() -> str:
                return await astr(foo)

            return inner

        self.content = list(
            [
                _async_helper(c)
                if isinstance(c, Element) or isinstance(c, Component)
                else c
                for c in content
            ]
        )
        self.swap = swap
        self.target = target
        self.trigger = trigger
        self.swap_oob = swap_oob
        self.confirm = confirm
        self.boost = boost
        self.push_url = push_url
        self.indicator = indicator
        self.on = on
        self.kwargs = kwargs
        self.click = click
        self.submit = submit
        self.change = change
        self.mouse_over = mouse_over
        self.mouse_enter = mouse_enter
        self.load = load
        self.intersect = intersect
        self.revealed = revealed

        helper_keywords = {
            "click": HTMXTrigger.CLICK,
            "submit": HTMXTrigger.SUBMIT,
            "change": HTMXTrigger.CHANGE,
            "mouse_over": HTMXTrigger.MOUSEOVER,
            "mouse_enter": HTMXTrigger.MOUSEENTER,
            "load": HTMXTrigger.LOAD,
            "intersect": HTMXTrigger.INTERSECT,
            "revealed": HTMXTrigger.REVEALED,
        }

        for k, v in helper_keywords.items():
            if getattr(self, k, None):
                self.target = getattr(self, k)
                self.trigger = Trigger(v)

    def append(self, el: Union[str, hype.Element]) -> None:
        self.content.append(el)

    def attrs(self, **kwargs: str) -> None:
        self.kwargs = {**self.kwargs, **kwargs}

    def render(self) -> hype.Element:
        _class = self.kwargs.pop("_class", "")
        if self.indicator:
            _class += HTMXClass.Indicator

        el = self.el(
            *self.content,
            _class=_class,
            **self.kwargs,
        )

        if self.target:
            el.attrs(
                hx_swap=self.swap,
                hx_target=f"#{self.target.instance.id}",
                **{f"hx_{self.target.http_method.lower()}": self.target.path},
            )

        if self.push_url:
            el.attrs(hx_push_url=self.push_url)

        if self.trigger:
            if isinstance(self.trigger, tuple):
                el.attrs(hx_trigger=", ".join([str(t) for t in self.trigger]))
            else:
                el.attrs(hx_trigger=str(self.trigger))

        if self.swap_oob:
            el.attrs(hx_swap_oob="true")

        if self.confirm:
            el.attrs(hx_confirm=self.confirm)

        if self.boost:
            el.attrs(hx_boost="true")

        if self.on:
            el.attrs(hx_on=self.on)

        return el

    async def _astr_(self) -> str:
        return await self.render().render()


class Doc:
    def __init__(self, el: Element):
        self.el = el

    def attrs(self, **kwargs: str) -> None:
        self.el.attrs(**kwargs)

    async def _astr_(self) -> str:
        doc = await hype.Doc(await astr(self.el)).render()
        return str(doc)


class A(Element):
    el = hype.A


class Abbr(Element):
    el = hype.Abbr


class Address(Element):
    el = hype.Address


class Area(Element):
    el = hype.Area


class Article(Element):
    el = hype.Article


class Aside(Element):
    el = hype.Aside


class Audio(Element):
    el = hype.Audio


class B(Element):
    el = hype.B


class Base(Element):
    el = hype.Base


class Bdi(Element):
    el = hype.Bdi


class Bdo(Element):
    el = hype.Bdo


class Blockquote(Element):
    el = hype.Blockquote


class Body(Element):
    el = hype.Body


class Br(Element):
    el = hype.Br


class Button(Element):
    el = hype.Button


class Canvas(Element):
    el = hype.Canvas


class Caption(Element):
    el = hype.Caption


class Cite(Element):
    el = hype.Cite


class Code(Element):
    el = hype.Code


class Col(Element):
    el = hype.Col


class Colgroup(Element):
    el = hype.Colgroup


class Data(Element):
    el = hype.Data


class Datalist(Element):
    el = hype.Datalist


class Dd(Element):
    el = hype.Dd


class Del(Element):
    el = hype.Del


class Details(Element):
    el = hype.Details


class Dfn(Element):
    el = hype.Dfn


class Dialog(Element):
    el = hype.Dialog


class Div(Element):
    el = hype.Div


class Dl(Element):
    el = hype.Dl


class Dt(Element):
    el = hype.Dt


class Em(Element):
    el = hype.Em


class Embed(Element):
    el = hype.Embed


class Fieldset(Element):
    el = hype.Fieldset


class Figcaption(Element):
    el = hype.Figcaption


class Figure(Element):
    el = hype.Figure


class Footer(Element):
    el = hype.Footer


class Form(Element):
    el = hype.Form


class H1(Element):
    el = hype.H1


class H2(Element):
    el = hype.H2


class H3(Element):
    el = hype.H3


class H4(Element):
    el = hype.H4


class H5(Element):
    el = hype.H5


class H6(Element):
    el = hype.H6


class Head(Element):
    el = hype.Head


class Header(Element):
    el = hype.Header


class Hgroup(Element):
    el = hype.Hgroup


class Hr(Element):
    el = hype.Hr


class Html(Element):
    el = hype.Html


class I(Element):
    el = hype.I


class Iframe(Element):
    el = hype.Iframe


class Img(Element):
    el = hype.Img


class Input(Element):
    el = hype.Input


class Ins(Element):
    el = hype.Ins


class Kbd(Element):
    el = hype.Kbd


class Label(Element):
    el = hype.Label


class Legend(Element):
    el = hype.Legend


class Li(Element):
    el = hype.Li


class Link(Element):
    el = hype.Link


class Main(Element):
    el = hype.Main


class Map(Element):
    el = hype.Map


class Mark(Element):
    el = hype.Mark


class Math(Element):
    el = hype.Math


class Menu(Element):
    el = hype.Menu


class Menuitem(Element):
    el = hype.Menuitem


class Meta(Element):
    el = hype.Meta


class Meter(Element):
    el = hype.Meter


class Nav(Element):
    el = hype.Nav


class Noscript(Element):
    el = hype.Noscript


class Object(Element):
    el = hype.Object


class Ol(Element):
    el = hype.Ol


class Optgroup(Element):
    el = hype.Optgroup


class Option(Element):
    el = hype.Option


class Output(Element):
    el = hype.Output


class P(Element):
    el = hype.P


class Param(Element):
    el = hype.Param


class Picture(Element):
    el = hype.Picture


class Pre(Element):
    el = hype.Pre


class Progress(Element):
    el = hype.Progress


class Q(Element):
    el = hype.Q


class Rb(Element):
    el = hype.Rb


class Rp(Element):
    el = hype.Rp


class Rt(Element):
    el = hype.Rt


class Rtc(Element):
    el = hype.Rtc


class Ruby(Element):
    el = hype.Ruby


class S(Element):
    el = hype.S


class Samp(Element):
    el = hype.Samp


class Script(Element):
    el = hype.Script


class Section(Element):
    el = hype.Section


class Select(Element):
    el = hype.Select


class SelfClosingElement(Element):
    el = hype.SelfClosingElement


class Slot(Element):
    el = hype.Slot


class Small(Element):
    el = hype.Small


class Source(Element):
    el = hype.Source


class Span(Element):
    el = hype.Span


class Strong(Element):
    el = hype.Strong


class Style(Element):
    el = hype.Style


class Sub(Element):
    el = hype.Sub


class Summary(Element):
    el = hype.Summary


class Sup(Element):
    el = hype.Sup


class Svg(Element):
    el = hype.Svg


class Table(Element):
    el = hype.Table


class Tbody(Element):
    el = hype.Tbody


class Td(Element):
    el = hype.Td


class Template(Element):
    el = hype.Template


class Textarea(Element):
    el = hype.Textarea


class Tfoot(Element):
    el = hype.Tfoot


class Th(Element):
    el = hype.Th


class Thead(Element):
    el = hype.Thead


class Time(Element):
    el = hype.Time


class Title(Element):
    el = hype.Title


class Tr(Element):
    el = hype.Tr


class Track(Element):
    el = hype.Track


class U(Element):
    el = hype.U


class Ul(Element):
    el = hype.Ul


class Var(Element):
    el = hype.Var


class Video(Element):
    el = hype.Video


class Wbr(Element):
    el = hype.Wbr
