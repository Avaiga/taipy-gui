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
from taipy.gui import Gui

data = [
    {
        "Temperatures": [
            [17.2, 27.4, 28.6, 21.5],
            [5.6, 15.1, 20.2, 8.1],
            [26.6, 22.8, 21.8, 24.0],
            [22.3, 15.5, 13.4, 19.6],
            [3.9, 18.9, 25.7, 9.8],
        ],
        "Cities": ["Hanoi", "Paris", "Rio", "Sydney", "Washington"],
    },
    {"Seasons": ["Winter", "Spring", "Summer", "Autumn"]},
]

page = """
# Heatmap - Unbalanced

<|{data}|chart|type=heatmap|z=0/Temperatures|x=1/Seasons|y=0/Cities|>
"""

Gui(page).run()
