from taipy.gui import Gui
from example_library import ExampleLibrary
import random
import string

value = "a"

page = """
# Demonstrating the example custom elements

*My custom label:* <|{value}|example.label|>

<|Add a character|button|>
"""

def on_action(state):
  state.value = state.value + random.choice(string.ascii_letters)

Gui(page, libraries=[ExampleLibrary()]).run()
