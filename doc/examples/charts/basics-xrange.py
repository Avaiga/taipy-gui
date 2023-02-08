# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
# -----------------------------------------------------------------------------------------
# To execute this script, make sure that the taipy-gui package is installed in your
# Python environment and run:
#     python <script>
# -----------------------------------------------------------------------------------------
from taipy import Gui

# x values are [-10..10]
x_range = range(-10, 11)

# The data set that holds both the x and the y values
data = {
    "X": x_range,
    "Y": [x*x for x in x_range]
}

page = """
# Basics - X range
<|toggle|theme|>

<|{data}|chart|x=X|y=Y|height=300px|>
"""

Gui(page).run(run_browser=False)
