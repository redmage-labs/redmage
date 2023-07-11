from typing import Optional, Tuple, Type, Union

import hype

from .targets import Target
from .triggers import Trigger
from .types import HTMXClass, HTMXSwap, HTMXTrigger


class Element:
    el: Type[hype.Element]

    def __init__(
        self,
        *content: Union[str, hype.Element],
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
        self.content = list(content)
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

    def __str__(self) -> str:
        return str(self.render())


class Doc:
    def __init__(self, el: Element):
        self.el = el

    def attrs(self, **kwargs: str) -> None:
        self.el.attrs(**kwargs)

    def __str__(self) -> str:
        return str(hype.Doc(str(self.el)))


class A(Element):
    el = hype.element.A


class Abbr(Element):
    el = hype.element.Abbr


class Address(Element):
    el = hype.element.Address


class Area(Element):
    el = hype.element.Area


class Article(Element):
    el = hype.element.Article


class Aside(Element):
    el = hype.element.Aside


class Audio(Element):
    el = hype.element.Audio


class B(Element):
    el = hype.element.B


class Base(Element):
    el = hype.element.Base


class Bdi(Element):
    el = hype.element.Bdi


class Bdo(Element):
    el = hype.element.Bdo


class Blockquote(Element):
    el = hype.element.Blockquote


class Body(Element):
    el = hype.element.Body


class Br(Element):
    el = hype.element.Br


class Button(Element):
    el = hype.element.Button


class Canvas(Element):
    el = hype.element.Canvas


class Caption(Element):
    el = hype.element.Caption


class Cite(Element):
    el = hype.element.Cite


class Code(Element):
    el = hype.element.Code


class Col(Element):
    el = hype.element.Col


class Colgroup(Element):
    el = hype.element.Colgroup


class Data(Element):
    el = hype.element.Data


class Datalist(Element):
    el = hype.element.Datalist


class Dd(Element):
    el = hype.element.Dd


class Del(Element):
    el = hype.element.Del


class Details(Element):
    el = hype.element.Details


class Dfn(Element):
    el = hype.element.Dfn


class Dialog(Element):
    el = hype.element.Dialog


class Div(Element):
    el = hype.element.Div


class Dl(Element):
    el = hype.element.Dl


class Dt(Element):
    el = hype.element.Dt


class Em(Element):
    el = hype.element.Em


class Embed(Element):
    el = hype.element.Embed


class Fieldset(Element):
    el = hype.element.Fieldset


class Figcaption(Element):
    el = hype.element.Figcaption


class Figure(Element):
    el = hype.element.Figure


class Footer(Element):
    el = hype.element.Footer


class Form(Element):
    el = hype.element.Form


class H1(Element):
    el = hype.element.H1


class H2(Element):
    el = hype.element.H2


class H3(Element):
    el = hype.element.H3


class H4(Element):
    el = hype.element.H4


class H5(Element):
    el = hype.element.H5


class H6(Element):
    el = hype.element.H6


class Head(Element):
    el = hype.element.Head


class Header(Element):
    el = hype.element.Header


class Hgroup(Element):
    el = hype.element.Hgroup


class Hr(Element):
    el = hype.element.Hr


class Html(Element):
    el = hype.element.Html


class I(Element):
    el = hype.element.I


class Iframe(Element):
    el = hype.element.Iframe


class Img(Element):
    el = hype.element.Img


class Input(Element):
    el = hype.element.Input


class Ins(Element):
    el = hype.element.Ins


class Kbd(Element):
    el = hype.element.Kbd


class Label(Element):
    el = hype.element.Label


class Legend(Element):
    el = hype.element.Legend


class Li(Element):
    el = hype.element.Li


class Link(Element):
    el = hype.element.Link


class Main(Element):
    el = hype.element.Main


class Map(Element):
    el = hype.element.Map


class Mark(Element):
    el = hype.element.Mark


class Math(Element):
    el = hype.element.Math


class Menu(Element):
    el = hype.element.Menu


class Menuitem(Element):
    el = hype.element.Menuitem


class Meta(Element):
    el = hype.element.Meta


class Meter(Element):
    el = hype.element.Meter


class Nav(Element):
    el = hype.element.Nav


class Noscript(Element):
    el = hype.element.Noscript


class Object(Element):
    el = hype.element.Object


class Ol(Element):
    el = hype.element.Ol


class Optgroup(Element):
    el = hype.element.Optgroup


class Option(Element):
    el = hype.element.Option


class Output(Element):
    el = hype.element.Output


class P(Element):
    el = hype.element.P


class Param(Element):
    el = hype.element.Param


class Picture(Element):
    el = hype.element.Picture


class Pre(Element):
    el = hype.element.Pre


class Progress(Element):
    el = hype.element.Progress


class Q(Element):
    el = hype.element.Q


class Rb(Element):
    el = hype.element.Rb


class Rp(Element):
    el = hype.element.Rp


class Rt(Element):
    el = hype.element.Rt


class Rtc(Element):
    el = hype.element.Rtc


class Ruby(Element):
    el = hype.element.Ruby


class S(Element):
    el = hype.element.S


class Samp(Element):
    el = hype.element.Samp


class Script(Element):
    el = hype.element.Script


class Section(Element):
    el = hype.element.Section


class Select(Element):
    el = hype.element.Select


class SelfClosingElement(Element):
    el = hype.element.SelfClosingElement


class Slot(Element):
    el = hype.element.Slot


class Small(Element):
    el = hype.element.Small


class Source(Element):
    el = hype.element.Source


class Span(Element):
    el = hype.element.Span


class Strong(Element):
    el = hype.element.Strong


class Style(Element):
    el = hype.element.Style


class Sub(Element):
    el = hype.element.Sub


class Summary(Element):
    el = hype.element.Summary


class Sup(Element):
    el = hype.element.Sup


class Svg(Element):
    el = hype.element.Svg


class Table(Element):
    el = hype.element.Table


class Tbody(Element):
    el = hype.element.Tbody


class Td(Element):
    el = hype.element.Td


class Template(Element):
    el = hype.element.Template


class Textarea(Element):
    el = hype.element.Textarea


class Tfoot(Element):
    el = hype.element.Tfoot


class Th(Element):
    el = hype.element.Th


class Thead(Element):
    el = hype.element.Thead


class Time(Element):
    el = hype.element.Time


class Title(Element):
    el = hype.element.Title


class Tr(Element):
    el = hype.element.Tr


class Track(Element):
    el = hype.element.Track


class U(Element):
    el = hype.element.U


class Ul(Element):
    el = hype.element.Ul


class Var(Element):
    el = hype.element.Var


class Video(Element):
    el = hype.element.Video


class Wbr(Element):
    el = hype.element.Wbr
