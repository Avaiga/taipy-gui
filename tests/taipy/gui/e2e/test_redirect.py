from importlib import util

import pytest

if util.find_spec("playwright"):
    from playwright._impl._page import Page

from taipy.gui import Gui


@pytest.mark.teste2e
def test_redirect(page: "Page", gui: Gui, helpers):
    page_md = """
<|Redirect Successfully|id=text1|>
"""
    gui.add_page(name="test", page=page_md)
    helpers.run_e2e(gui)
    page.goto("/")
    page.expect_websocket()
    page.wait_for_selector("#text1")
    text1 = page.query_selector("#text1")
    assert text1.inner_text() == "Redirect Successfully"


@pytest.mark.teste2e
def test_redirect_with_prefix(page: "Page", gui_prefix: Gui, helpers):
    page_md = """
<|Redirect Successfully|id=text1|>
"""
    gui_prefix.add_page(name="test", page=page_md)
    helpers.run_e2e(gui_prefix)
    page.goto("/prefix")
    page.expect_websocket()
    page.wait_for_selector("#text1")
    text1 = page.query_selector("#text1")
    assert text1.inner_text() == "Redirect Successfully"
