import inspect
import pytest

from taipy.gui import Gui, Markdown


def test_du_table_data_fetched(gui: Gui, helpers, csvdata):
    # Bind test variables
    csvdata = csvdata

    # set gui frame
    gui._set_frame(inspect.currentframe())

    # Bind a page so that the variable will be evaluated as expression
    gui.add_page(
        "test",
        Markdown(
            "<|{csvdata}|table|page_size=10|page_size_options=10;30;100|columns=Day;Entity;Code;Daily hospital occupancy|date_format=eee dd MMM yyyy|>"
        ),
    )
    gui.run(run_server=False)
    flask_client = gui._server.test_client()
    # WS client and emit
    ws_client = gui._server._ws.test_client(gui._server.get_flask())
    sid = helpers.create_scope_and_get_sid(gui)
    # Get the jsx once so that the page will be evaluated -> variable will be registered
    flask_client.get(f"/taipy-jsx/test/?client_id={sid}")
    ws_client.emit(
        "message",
        {
            "client_id": sid,
            "type": "DU",
            "name": "_TpD_csvdata",
            "payload": {
                "columns": ["Day", "Entity", "Code", "Daily hospital occupancy"],
                "pagekey": "0-100--asc",
                "start": 0,
                "end": 10,
                "orderby": "",
                "sort": "asc",
            },
        },
    )
    # assert for received message (message that would be sent to the frontend client)
    received_messages = ws_client.get_received()
    assert received_messages
    helpers.assert_outward_ws_message(
        received_messages[0],
        "MU",
        "_TpD_csvdata",
        {
            "data": [
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-01T00:00:00.000000Z",
                    "Daily hospital occupancy": 856,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-02T00:00:00.000000Z",
                    "Daily hospital occupancy": 823,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-03T00:00:00.000000Z",
                    "Daily hospital occupancy": 829,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-04T00:00:00.000000Z",
                    "Daily hospital occupancy": 826,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-05T00:00:00.000000Z",
                    "Daily hospital occupancy": 712,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-06T00:00:00.000000Z",
                    "Daily hospital occupancy": 824,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-07T00:00:00.000000Z",
                    "Daily hospital occupancy": 857,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-08T00:00:00.000000Z",
                    "Daily hospital occupancy": 829,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-09T00:00:00.000000Z",
                    "Daily hospital occupancy": 820,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-10T00:00:00.000000Z",
                    "Daily hospital occupancy": 771,
                    "Entity": "Austria",
                },
                {
                    "Code": "AUT",
                    "Day_str": "2020-04-11T00:00:00.000000Z",
                    "Daily hospital occupancy": 790,
                    "Entity": "Austria",
                },
            ],
            "rowcount": 14477,
            "start": 0,
            "format": "JSON",
        },
    )
