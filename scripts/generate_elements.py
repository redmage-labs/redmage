from inspect import getmembers, isclass

import hype
from jinja2 import Template

if __name__ == "__main__":
    # generate the source code for all the Element classes
    template_string = """class {{ name }}(Element):
    el = hype.element.{{ name }}"""

    template = Template(template_string)
    class_strings = []
    for member in getmembers(hype.element):
        if isclass(member[1]) and issubclass(member[1], hype.Element):
            class_strings.append(template.render(name=member[0]))

    with open("elements_temp.py", "w") as f:
        f.write("\n\n\n".join(class_strings))
