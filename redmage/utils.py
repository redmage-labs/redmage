import inspect
from inspect import Parameter, _ParameterKind
from typing import Any, Dict, List


def group_signature_param_by_kind(
    sig: inspect.Signature,
) -> Dict[_ParameterKind, List[Parameter]]:
    # TODO fix type hints here
    # Need VAR_POSITIONAL and VAR_KEYWORD?
    grouped: Dict[_ParameterKind, List[Parameter]] = {
        Parameter.POSITIONAL_ONLY: [],
        Parameter.POSITIONAL_OR_KEYWORD: [],
        Parameter.KEYWORD_ONLY: [],
    }
    for param in sig.parameters.values():
        grouped[param.kind].append(param)
    return grouped


async def astr(astringable: Any) -> str:
    return await astringable._astr_()
