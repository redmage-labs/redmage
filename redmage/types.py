import importlib

# This is a workaround for Python 3.11 which will have StrEnum
# but breaks the (str, Enum) inheritance
try:  # pragma: no cover
    StrEnum = importlib.import_module("enum").StrEnum
except AttributeError:  # pragma: no cover
    from enum import Enum

    class StrEnum(str, Enum):  # type: ignore
        pass


class HTTPMethod(StrEnum):  # type: ignore
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HTMXSwap(StrEnum):  # type: ignore
    OUTER_HTML = "outerHTML"
    INNER_HTML = "innerHTML"
    AFTER_BEGIN = "afterbegin"
    BEFORE_BEGIN = "beforebegin"
    BEFORE_END = "beforeend"
    AFTER_END = "afterend"
    DELETE = "delete"
    NONE = "none"


class HTMXClass(StrEnum):  # type: ignore
    Indicator = "htmx-indicator"


class HTMXTrigger(StrEnum):  # type: ignore
    EVERY = "every"
    LOAD = "load"
    INTERSECT = "intersect"
    REVEALED = "revealed"
    CLICK = "click"
    CHANGE = "change"
    MOUSEOVER = "mouseover"
    MOUSEENTER = "mouseenter"
    SUBMIT = "submit"
    KEYUP = "keyup"
    SEARCH = "search"


class HTMXTriggerModifier(StrEnum):  # type: ignore
    ONCE = "once"
    CHANGED = "changed"
    THROTTLE = "throttle"
    DELAY = "delay"
    FROM = "from"
    ROOT = "root"
    THRESHHOLD = "threshold"
