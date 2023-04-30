from enum import Enum


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HTMXSwap(str, Enum):
    OUTER_HTML = "outerHTML"
    INNER_HTML = "innerHTML"
    AFTER_BEGIN = "afterbegin"
    BEFORE_BEGIN = "beforebegin"
    BEFORE_END = "beforeend"
    AFTER_END = "afterend"
    DELETE = "delete"
    NONE = "none"


class HTMXClass(str, Enum):
    Indicator = "htmx-indicator"


class HTMXTrigger(str, Enum):
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


class HTMXTriggerModifier(str, Enum):
    ONCE = "once"
    CHANGED = "changed"
    THROTTLE = "throttle"
    DELAY = "delay"
    FROM = "from"
    ROOT = "root"
    THRESHHOLD = "threshold"
