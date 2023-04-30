from starlette.convertors import Convertor


class BoolConvertor(Convertor):
    regex = "True|False"

    def convert(self, value: str) -> bool:
        return True if value == "True" else False

    def to_string(self, value: bool) -> str:
        return "True" if value else "False"


class StringConverter(Convertor):
    """
    Custom String Convertor to allow for empty strings for urls
    """

    regex = "[^/]+"

    def convert(self, value: str) -> str:
        return "" if value == "__empty__" else value

    def to_string(self, value: str) -> str:
        return value if value else "__empty__"
