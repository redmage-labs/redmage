import inspect

from redmage.utils import group_signature_param_by_kind


def test_group_signature_param_by_kind():
    class ExampleClass:
        def method(self, a, /, b, c=None, *, d=None):
            pass

    sig = inspect.signature(ExampleClass.method)
    grouped = group_signature_param_by_kind(sig)
    assert len(grouped[inspect.Parameter.POSITIONAL_ONLY]) == 2
    assert len(grouped[inspect.Parameter.POSITIONAL_OR_KEYWORD]) == 2
    assert len(grouped[inspect.Parameter.KEYWORD_ONLY]) == 1
