# Copyright 2022 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""# Taipy Graphical User Interface generator.

The Taipy Gui package provides User Interface generation based on
page templates. It can run a Web server that a Web browser can connect
to.

The pages are generated by a Web server that allows Web clients to
connect, display and interact with the page content through visual
elements.

Each page can contain regular text and images, as well
as Taipy controls that are typically linked to some
value that is managed by the whole Taipy application.

Here is how you can create your first Taipy User Interface:

   - Create a Python source file.
     Copy these two lines into a file called _taipy_app.py_.
     ```py
     from taipy import Gui
     Gui("# Hello Taipy!").run()
     ```
   - Install Taipy:
     ```
     pip install taipy
     ```
   - Run your application:
     ```
     python taipy_app.py
     ```

Your browser opens a new page, showing the content of your graphical
application.

!!! Note "Optional packages"

    There are Python packages that you can install in your environment to
    add functionality to Taipy GUI:

    - [`python-magic`](https://pypi.org/project/python-magic/): identifies image format from
      byte buffers so the [`image`](../../gui/viselements/image.md) control can display them,
      and so that [`file_download`](../../gui/viselements/file_download.md) can request
      the browser to display the image content when relevant.<br/>
      You can install that package with the regular `pip install python-magic` command
      (then potentially `pip install python-magic` on Windows),
      or install Taipy GUI using: `pip install taipy-gui[image]`.
    - [`pyarrow`](https://pypi.org/project/pyarrow/): can improve the performance of your
      application by reducing the volume of data transferred between the Web server and the
      clients. This is relevant if your application uses large tabular data.<br/>
      You can install that package with the regular `pip install pyarrow` command,
      or install Taipy GUI using: `pip install taipy-gui[arrow]`.

"""

from .gui import Gui
from .gui_actions import (
    download,
    get_context_id,
    get_module_name_from_state,
    hold_control,
    invoke_state_callback,
    navigate,
    notify,
    resume_control,
)
from .icon import Icon
from .renderers import Html, Markdown
from .state import State
