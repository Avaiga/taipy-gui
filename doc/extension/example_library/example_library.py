 
from taipy.gui.extension import ElementLibrary, Element, ElementProperty, PropertyType

class ExampleLibrary(ElementLibrary):
    def get_name(self) -> str:
        return "example"
    def get_elements(self) -> dict:
        return ({
            "label":
            Element("value", {
                "value": ElementProperty(PropertyType.dynamic_string)
                },
                react_component="ExampleLabel"
            )
            })
    def get_scripts(self) -> list[str]:
        # Only one JavaScript bundle for this library.
        return ["example_library/frontend/dist/exampleLibrary.js"]
