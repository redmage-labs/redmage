import logging
from inspect import Parameter, getmembers, isfunction, signature
from types import FunctionType
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union

from starlette.applications import Starlette
from starlette.convertors import CONVERTOR_TYPES as starlette_convertors
from starlette.datastructures import FormData, QueryParams
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from redmage.exceptions import RedmageError

from .components import Component
from .targets import Target
from .types import HTTPMethod
from .utils import astr

logger = logging.getLogger("redmage")


ComponentClass = Type[Component]


class Redmage:
    def __init__(
        self, middleware: Optional[Sequence[Middleware]] = None, debug: bool = False
    ):
        self.debug = debug
        self.middleware = middleware
        self.routes: List[Route] = []
        self.components: List[Tuple[ComponentClass, Optional[Tuple[str]]]] = []
        # Could cause problems if multiple apps are created
        Component.set_app(self)

    @property
    def starlette(self) -> Starlette:
        if not hasattr(self, "_starlette"):
            self.create_routes()
            if self.middleware:
                self._starlette = Starlette(
                    debug=self.debug,
                    routes=self.routes,
                    middleware=self.middleware,
                )
            else:
                self._starlette = Starlette(debug=self.debug, routes=self.routes)
        return self._starlette

    def create_routes(self) -> None:
        for cls, routes in self.components:
            if routes:
                self._register_routes(cls, routes)
            self._register_targets(cls)

    def register_component(
        self, cls: ComponentClass, routes: Optional[Tuple[str]] = None
    ) -> None:
        self.components.append((cls, routes))

    def _get_explicit_route_function(self, cls: ComponentClass) -> Callable:
        async def route_function(request: Request) -> HTMLResponse:
            attrs = {**request.path_params, **request.query_params}
            instance = cls(**attrs)
            instance.request = request  # type: ignore
            return instance.build_response(await astr(instance))

        return route_function

    def _get_route_function(
        self, cls: ComponentClass, name: str, fn: Callable
    ) -> Callable:
        async def route_function(request: Request) -> HTMLResponse:
            # Starlette should validate and convert the path params
            instance_params, comp_params = self._split_params(
                request.path_params,
                name,
                fn,
            )
            # query params need to be validated and converted
            # to the correct type
            instance_query_params, comp_query_params = self._split_params(
                request.query_params,
                name,
                fn,
            )
            # body serializer object should validate the form data and
            # convert it to the correct type
            body = self._process_form(
                await request.form(), fn
            )  # always passed to the method
            instance = cls.__new__(cls)
            attrs = {**instance_params, **instance_query_params}
            attrs["_id"] = f"{cls.__name__}-{attrs['id']}"
            instance.__dict__.update(attrs)
            if body:
                components = fn(
                    instance,
                    body,
                    **{**comp_params, **comp_query_params},
                )
            else:
                components = fn(
                    instance,
                    **{**comp_params, **comp_query_params},
                )
            if isinstance(components, tuple):
                return instance.build_response(
                    "\n".join([await astr(c) for c in components])
                )
            elif components:
                return instance.build_response(await astr(components))
            return instance.build_response(await astr(instance))

        return route_function

    def _convert_value(self, key: str, value: str, fn: Callable) -> Any:
        params = signature(fn).parameters
        if key in params:
            ann = (
                params[key].annotation
                if isinstance(params[key].annotation, str)
                else params[key].annotation.__name__
            )
            type_name = ann
            value = starlette_convertors[type_name].convert(value)
        return value

    def _split_params(
        self,
        params: Union[Dict[str, Any], QueryParams],
        method_name: str,
        method_fn: Callable,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        comp_params = {}
        method_params = {}

        for k, v in params.items():
            if k.startswith(f"{method_name}__"):
                k = k.replace(f"{method_name}__", "")
                method_params[k] = self._convert_value(k, v, method_fn)
            else:
                comp_params[k] = self._convert_value(k, v, method_fn)

        return comp_params, method_params

    def _process_form(self, form_data: FormData, fn: Callable) -> Any:
        serializer = self._get_body_serializer_class(fn)
        body = {}
        for k, v in form_data.items():
            body[k] = v
        if body and not serializer:
            raise RedmageError("The request has a body but no serializer was provided")
        if body and serializer:
            return serializer(**body) if body else None
        return body

    def _get_body_serializer_class(self, fn: Callable) -> Optional[Type]:
        params = signature(fn).parameters
        for param_name, param_value in params.items():
            if (
                param_name != "self"
                and param_value.default == Parameter.empty
                and param_value.kind == Parameter.POSITIONAL_ONLY
            ):
                return param_value.annotation
        return None

    def _get_target_method(self, name: str, fn: Callable) -> Callable[..., Target]:
        def target_method(instance: Component, *args: Any, **kwargs: Any) -> Target:
            return Target(instance, name, fn.target_method, *args, **kwargs)  # type: ignore

        setattr(target_method, "target_signature", signature(fn))
        return target_method

    def _register_routes(
        self, cls: ComponentClass, routes: Tuple[str]
    ) -> ComponentClass:
        for route in routes:
            logger.debug(route)
            self.routes.append(
                Route(
                    route,
                    self._get_explicit_route_function(cls),
                    methods=[
                        HTTPMethod.GET,
                    ],
                )
            )

        return self._register_targets(cls)

    def _register_targets(self, cls: ComponentClass) -> ComponentClass:
        methods = filter(
            lambda m: hasattr(m[1], "is_target"), getmembers(cls, predicate=isfunction)
        )

        for method in methods:
            self._register_target(cls, method)
        return cls

    def _register_target(
        self, cls: ComponentClass, method: Tuple[str, FunctionType]
    ) -> None:
        method_name, method_fn = method
        path = cls.get_base_path()
        path += cls.get_target_path(method_name)
        logger.debug(path)
        route_function = self._get_route_function(cls, method_name, method_fn)

        self.routes.append(
            Route(
                path,
                route_function,
                name=method_name,
                methods=[method_fn.target_method],  # type: ignore
            )
        )

        target_method = self._get_target_method(method_name, method_fn)
        setattr(cls, method_name, target_method)
