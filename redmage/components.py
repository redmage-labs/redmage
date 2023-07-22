import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from inspect import Parameter, signature
from typing import Any, Dict, Optional
from typing import OrderedDict as OrderedDictType
from typing import Tuple
from uuid import uuid1

from starlette.convertors import CONVERTOR_TYPES as starlette_convertors
from starlette.requests import Request
from starlette.responses import HTMLResponse

from .utils import astr, group_signature_param_by_kind

logger = logging.getLogger("redmage")


class Component(ABC):
    app: "Redmage"  # type: ignore
    request = None  # type: ignore
    render_extensions: Dict[str, Any] = {}

    def __init_subclass__(cls, routes: Optional[Tuple[str]] = None, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        cls.app.register_component(cls, routes=routes)

    @classmethod
    def set_app(cls, app: "Redmage") -> None:  # type: ignore
        cls.app = app

    @classmethod
    def add_render_extension(cls, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            cls.render_extensions[key] = value

    @classmethod
    def get_base_path(cls, instance: Optional["Component"] = None) -> str:
        def get_uuid(instance: "Component") -> str:
            parts = instance.id.split("-")
            return "-".join(parts[1:])

        uuid = get_uuid(instance) if instance else "{id:str}"
        path = f"/{cls.__name__}/{uuid}"

        if getattr(cls, "__annotations__", None):
            annotations = cls.__annotations__
            annotations.pop("app", None)
            annotations.pop("render_extensions", None)

            for field, field_type in annotations.items():
                convertor = starlette_convertors[
                    field_type if isinstance(field_type, str) else field_type.__name__
                ]
                value = (
                    convertor.to_string(getattr(instance, field, None))
                    if instance
                    else f"{{{field}:{field_type.__name__}}}"
                )
                path += f"/{field}/{value}"
        return path

    @classmethod
    def get_target_path(
        cls,
        method_name: str,
        *args: Any,
        instance: Optional["Component"] = None,
        **kwargs: Any,
    ) -> str:
        # TODO refactor
        # This method behaves in two different ways
        # depending on whether the instance is passed or not
        # because once the method is bound the signature is different
        # Nice to have it in one spot though
        method_fn = getattr(cls, method_name)
        path = f"/{method_name}"

        if instance:
            # We want the developer to be able to pass the args as positional or keywords
            # like a normal python function but still know if it's path param or query param
            # it just depends on the order of the params in the signature
            positional_or_keyword_params = list(args) + list(kwargs.values())
            grouped_params = group_signature_param_by_kind(method_fn.target_signature)

            # self could be position only or postion_or_keyword
            # so set an offset to account for it
            if grouped_params[Parameter.POSITIONAL_OR_KEYWORD]:
                offset = (
                    1
                    if grouped_params[Parameter.POSITIONAL_OR_KEYWORD][0].name == "self"
                    else 0
                )

            for n, param_value in enumerate(
                grouped_params[Parameter.POSITIONAL_OR_KEYWORD]
            ):
                if (
                    param_value.default == Parameter.empty
                    and param_value.name != "self"
                    and len(positional_or_keyword_params) >= n
                ):
                    convertor = starlette_convertors[param_value.annotation.__name__]
                    value = convertor.to_string(
                        positional_or_keyword_params[n - offset]
                    )
                    path += f"/{value}"

            path += "?"

            for n, param_value in enumerate(
                grouped_params[Parameter.POSITIONAL_OR_KEYWORD]
                + grouped_params[Parameter.KEYWORD_ONLY]
            ):
                if (
                    param_value.default != Parameter.empty
                    and param_value.kind != Parameter.POSITIONAL_ONLY
                    and param_value.name != "self"
                    and len(positional_or_keyword_params) >= n
                ):
                    ann = (
                        param_value.annotation
                        if isinstance(param_value.annotation, str)
                        else param_value.annotation.__name__
                    )
                    convertor = starlette_convertors[ann]
                    value = convertor.to_string(
                        positional_or_keyword_params[n - offset]
                    )
                    path += f"{method_name}__{param_value.name}="
                    path += f"{value}&"

            path = path[:-1]  # Have to remove whatever the last character is

        else:
            params = signature(method_fn).parameters
            for param_value in params.values():
                if (
                    param_value.default == Parameter.empty
                    and param_value.kind != Parameter.POSITIONAL_ONLY
                    and param_value.name != "self"
                ):
                    ann = (
                        param_value.annotation
                        if isinstance(param_value.annotation, str)
                        else param_value.annotation.__name__
                    )
                    path += f"/{{{method_name}__{param_value.name}:{ann}}}"

        return path

    @property
    def id(self) -> str:
        if not hasattr(self, "_id"):
            self._id = f"{self.__class__.__name__}-{str(uuid1())}"
        return self._id

    @abstractmethod
    async def render(self, **exts: Any) -> "Element":  # type: ignore
        ...  # pragma: no cover

    def _filter_render_extensions(self) -> OrderedDictType[str, Any]:
        args = OrderedDict()
        params = signature(self.render).parameters
        for param in params.values():
            if param.name in self.render_extensions.keys():
                args[param.name] = self.render_extensions[param.name]
            if param.kind == Parameter.VAR_KEYWORD:
                args.update(self.render_extensions)
        return args

    def set_element_id(self, el: "Element") -> None:  # type: ignore
        el.attrs(_id=self.id)

    def build_response(self, content: Any) -> HTMLResponse:
        return HTMLResponse(content)

    async def _astr_(self) -> str:
        render_extentions = self._filter_render_extensions()
        el = await self.render(**render_extentions)
        self.set_element_id(el)
        return await astr(el)
