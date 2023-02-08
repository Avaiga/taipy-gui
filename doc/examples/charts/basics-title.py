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

layout = {
  "xaxis": {
    # Force the title of the x axis
    "title": "Values for x"
  }
}

page = """
# Basics - Title
<|toggle|theme|>

<|{[x*x for x in range(0, 11)]}|chart|title=Plotting x squared|layout={layout}|height=300px|>
"""

Gui(page).run(run_browser=False)
