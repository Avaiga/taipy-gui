import time
from importlib import util

import pytest

if util.find_spec("playwright"):
    from playwright._impl._page import Page

from taipy.gui import Gui


@pytest.mark.teste2e
def test_selector_action(page: "Page", gui: Gui, helpers):
    page_md = """
<|{x}|selector|lov=Item 1;Item 2;Item 3|id=selector1|>
"""
    x = "Item 1"
    gui.add_page(name="test", page=page_md)
    helpers.run_e2e(gui)
    page.goto("/test")
    page.expect_websocket()
    page.wait_for_selector("#selector1")
    assert gui._bindings().x == "Item 1"
    page.click('#selector1 ul > div[data-id="Item 3"]')
    page.wait_for_function(
        "document.querySelector('#selector1 ul > div[data-id=\"Item 3\"]').classList.contains('Mui-selected')"
    )
    retry = 0
    while retry < 20 and gui._bindings().x == "Item 1":
        time.sleep(0.2)
    assert gui._bindings().x == "Item 3"


@pytest.mark.teste2e
def test_selector_action_with_prefix(page: "Page", gui_prefix: Gui, helpers):
    page_md = """
<|{x}|selector|lov=Item 1;Item 2;Item 3|id=selector1|>
"""
    x = "Item 1"
    gui_prefix.add_page(name="test", page=page_md)
    helpers.run_e2e(gui_prefix)
    page.goto("/prefix/test")
    page.expect_websocket()
    page.wait_for_selector("#selector1")
    assert gui_prefix._bindings().x == "Item 1"
    page.click('#selector1 ul > div[data-id="Item 3"]')
    page.wait_for_function(
        "document.querySelector('#selector1 ul > div[data-id=\"Item 3\"]').classList.contains('Mui-selected')"
    )
    retry = 0
    while retry < 20 and gui_prefix._bindings().x == "Item 1":
        time.sleep(0.2)
    assert gui_prefix._bindings().x == "Item 3"
