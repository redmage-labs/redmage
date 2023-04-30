import logging
from typing import Any, Callable

from redmage.components import Component

from .types import HTTPMethod

logger = logging.getLogger("redmage")


class Target:
    @staticmethod
    def _decorator(fn: Callable, method: str = HTTPMethod.GET) -> Callable:
        setattr(fn, "is_target", True)
        setattr(fn, "target_method", method)
        return fn

    @classmethod
    def get(cls, fn: Callable) -> Callable:
        return cls._decorator(fn, HTTPMethod.GET)

    @classmethod
    def post(cls, fn: Callable) -> Callable:
        return cls._decorator(fn, HTTPMethod.POST)

    @classmethod
    def put(cls, fn: Callable) -> Callable:
        return cls._decorator(fn, HTTPMethod.PUT)

    @classmethod
    def delete(cls, fn: Callable) -> Callable:
        return cls._decorator(fn, HTTPMethod.DELETE)

    @classmethod
    def patch(cls, fn: Callable) -> Callable:
        return cls._decorator(fn, HTTPMethod.PATCH)

    def __init__(
        self,
        instance: Component,
        method_name: str,
        http_method: HTTPMethod,
        *args: Any,
        **kwargs: Any
    ):
        self.instance = instance
        self.method_name = method_name
        self.http_method = http_method
        self.args = args
        self.kwargs = kwargs

    @property
    def path(self) -> str:
        path = self.instance.get_base_path(instance=self.instance)
        path += self.instance.get_target_path(
            self.method_name,
            *self.args,
            instance=self.instance,
            **self.kwargs,
        )
        return path
