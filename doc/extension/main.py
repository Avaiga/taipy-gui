from taipy.gui import Gui
from example_library import ExampleLibrary
import random
import string

value = "Here is some text"

page = """  
# Custom elements example

## Fraction:

No denominator: <|123|example.fraction|>

Denominator is 0: <|321|example.fraction|denominator=0|>

Regular: <|355|example.fraction|denominator=113|>

## Custom label:

Colored text: <|{value}|example.label|>

<|Add a character|button|>
"""

def on_action(state):
  state.value = state.value + random.choice(string.ascii_letters)

Gui(page, libraries=[ExampleLibrary()]).run(debug=True)
