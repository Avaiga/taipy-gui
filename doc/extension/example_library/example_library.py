 
from taipy.gui.extension import ElementLibrary, Element, ElementProperty, PropertyType

class ExampleLibrary(ElementLibrary):

    def __init__(self) -> None:
        self.elements = {
            # A static element that displays its properties in a fraction
            "fraction": Element("numerator", {
                "numerator": ElementProperty(PropertyType.number),
                "denominator": ElementProperty(PropertyType.number)
                },
                render_xhtml=ExampleLibrary._fraction_render),
            # A dynamic element that decorates its value            
            "label": Element("value", {
                "value": ElementProperty(PropertyType.dynamic_string)
                },
                # The name of the React component (ColoredLabel) that implements this custom
                # element, as exported as ExampleLabel in front-end/src/index.ts
                react_component="ExampleLabel")
            }

    @staticmethod
    def _fraction_render(props: dict) -> str:
        numerator = props.get("numerator")
        denominator = props.get("denominator")
        # No denominator or numerator is 0: display the numerator
        if denominator is None or int(numerator) == 0:
            return f"<span>{numerator}</span>"
        # Denominator is zero: display infinity
        if int(denominator) == 0:
            return "<span style=\"font-size: 1.6em\">&#8734;</span>"
        return f"<span><sup>{numerator}</sup>/<sub>{denominator}</sub></span>"

    def get_name(self) -> str:
        return "example"
    
    def get_elements(self) -> dict:
        return self.elements

    def get_scripts(self) -> list[str]:
        # Only one JavaScript bundle for this library.
        return ["example_library/front-end/dist/exampleLibrary.js"]
