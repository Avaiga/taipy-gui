import re
import typing as t
from datetime import datetime

from ..types import AttributeType
from .builder import Builder


class Factory:

    __CONTROL_DEFAULT_PROP_NAME = {
        "button": "label",
        "chart": "data",
        "content": "value",
        "date_selector": "date",
        "dialog": "open",
        "expandable": "title",
        "field": "value",
        "input": "value",
        "layout": "columns",
        "navbar": "value",
        "number": "value",
        "pane": "open",
        "part": "type",
        "selector": "value",
        "slider": "value",
        "status": "value",
        "table": "data",
        "toggle": "value",
        "tree": "value",
    }

    __TEXT_ANCHORS = ["bottom", "top", "left", "right"]
    __TEXT_ANCHOR_NONE = "none"

    CONTROL_BUILDERS = {
        "button": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Button",
            attributes=attrs,
        )
        .set_value_and_default(with_update=False)
        .set_classNames(class_name="taipy-button", config_class="button")
        .set_attributes(
            [
                ("id"),
                ("on_action", AttributeType.string, ""),
                ("active", AttributeType.dynamic_boolean, True),
            ]
        ),
        "chart": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Chart",
            attributes=attrs,
        )
        .set_value_and_default(with_default=False)
        .set_classNames(class_name="taipy-chart", config_class="chart")
        .set_attributes(
            [
                ("id"),
                ("title"),
                ("width", AttributeType.string_or_number, "100vw"),
                ("height", AttributeType.string_or_number, "100vh"),
                ("layout", AttributeType.dict),
                ("range_change"),
                ("active", AttributeType.dynamic_boolean, True),
                ("limit_rows", AttributeType.boolean),
            ]
        )
        .get_chart_config("scatter", "lines+markers")
        .set_propagate()
        .set_refresh_on_update()
        .set_refresh(),
        "content": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="PageContent", attributes=attrs
        ),
        "date_selector": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="DateSelector",
            attributes=attrs,
            default_value=datetime.fromtimestamp(0),
        )
        .set_value_and_default()
        .set_classNames(class_name="taipy-date-selector", config_class="date_selector")
        .set_attributes(
            [
                ("with_time", AttributeType.boolean),
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
            ]
        )
        .set_propagate(),
        "dialog": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Dialog",
            attributes=attrs,
        )
        .set_value_and_default()
        .set_classNames(class_name="taipy-dialog", config_class="dialog")
        .set_attributes(
            [
                ("id"),
                ("title"),
                ("cancel_action"),
                ("cancel_label", AttributeType.string, "Cancel"),
                ("validate_action", AttributeType.string, "validate"),
                ("validate_label", AttributeType.string, "Validate"),
                ("active", AttributeType.dynamic_boolean, True),
                ("width", AttributeType.string_or_number),
                ("height", AttributeType.string_or_number),
            ]
        )
        .set_propagate()
        .set_partial()  # partial should be set before page_id
        .set_page_id(),
        "expandable": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="Expandable", attributes=attrs, default_value=""
        )
        .set_value_and_default()
        .set_classNames(class_name="taipy-expandable", config_class="expandable")
        .set_attributes(
            [
                ("id"),
                ("expanded", AttributeType.dynamic_boolean, True),
            ]
        ),
        "field": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Field",
            attributes=attrs,
        )
        .set_value_and_default(with_update=False)
        .set_classNames(class_name="taipy-field", config_class="field")
        .set_dataType()
        .set_attributes(
            [
                ("format"),
                ("id"),
            ]
        ),
        "input": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Input",
            attributes=attrs,
        )
        .set_type("text")
        .set_value_and_default()
        .set_propagate()
        .set_classNames(class_name="taipy-input", config_class="input")
        .set_attributes(
            [
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
            ]
        ),
        "layout": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="Layout", attributes=attrs, default_value=""
        )
        .set_classNames(class_name="taipy-layout", config_class="layout")
        .set_value_and_default(with_default=False)
        .set_attributes(
            [
                ("id"),
                ("columns[mobile]"),
                ("gap"),
            ]
        ),
        "navbar": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="NavBar", attributes=attrs, default_value=""
        )
        .set_classNames(class_name="taipy-navbar", config_class="navbar")
        .get_adapter("lov", multi_selection=False)  # need to be called before set_lov
        .set_lov()
        .set_attributes(
            [
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
            ]
        ),
        "number": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Input",
            attributes=attrs,
            default_value=0,
        )
        .set_type("number")
        .set_value_and_default()
        .set_classNames(class_name="taipy-number", config_class="input")
        .set_propagate()
        .set_attributes(
            [
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
            ]
        ),
        "pane": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="Pane", attributes=attrs, default_value=""
        )
        .set_value_and_default()
        .set_classNames(class_name="taipy-pane", config_class="pane")
        .set_attributes(
            [
                ("id"),
                ("anchor", AttributeType.string, "left"),
                ("close_action"),
                ("persistent", AttributeType.boolean, False),
                ("active", AttributeType.dynamic_boolean, True),
                ("width", AttributeType.string_or_number, "30vw"),
                ("height", AttributeType.string_or_number, "30vh"),
            ]
        )
        .set_propagate()
        .set_partial()  # partial should be set before page_id
        .set_page_id(),
        "part": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="Part", attributes=attrs, default_value=""
        )
        .set_classNames(class_name="taipy-part", config_class="part")
        .set_attributes([("id"), ("render", AttributeType.dynamic_boolean, True)]),
        "selector": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Selector",
            attributes=attrs,
        )
        .set_value_and_default(with_default=False)
        .set_classNames(class_name="taipy-selector", config_class="selector")
        .get_adapter("lov")  # need to be called before set_lov
        .set_lov()
        .set_attributes(
            [
                ("filter", AttributeType.boolean),
                ("multiple", AttributeType.boolean),
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
                ("height", AttributeType.string_or_number),
                ("width", AttributeType.string_or_number),
            ]
        )
        .set_refresh_on_update()
        .set_propagate(),
        "slider": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Slider",
            attributes=attrs,
            default_value=0,
        )
        .set_value_and_default()
        .set_classNames(class_name="taipy-slider", config_class="slider")
        .set_attributes(
            [
                ("min", AttributeType.number, 0),
                ("max", AttributeType.number, 100),
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
                ("width", AttributeType.string_or_number, 200),
            ]
        )
        .get_adapter("items", "lov")  # need to be called before set_lov
        .set_lov("items", "lov")
        .set_string_with_check("text_anchor", Factory.__TEXT_ANCHORS + [Factory.__TEXT_ANCHOR_NONE], "bottom")
        .set_propagate(),
        "status": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Status",
            attributes=attrs,
        )
        .set_value_and_default(with_update=False)
        .set_classNames(class_name="taipy-status", config_class="status")
        .set_propagate()
        .set_attributes(
            [("id"), ("active", AttributeType.dynamic_boolean, True), ("without_close", AttributeType.boolean, False)]
        ),
        "table": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="Table",
            attributes=attrs,
        )
        .set_value_and_default(with_default=False)
        .set_classNames(class_name="taipy-table", config_class="table")
        .get_dataframe_attributes()
        .set_attributes(
            [
                ("page_size", AttributeType.react, 100),
                ("allow_all_rows", AttributeType.boolean),
                ("show_all", AttributeType.boolean),
                ("auto_loading", AttributeType.boolean),
                ("width", AttributeType.string_or_number, "100vw"),
                ("height", AttributeType.string_or_number, "80vh"),
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
                ("editable", AttributeType.dynamic_boolean, True),
                ("edit_action"),
                ("delete_action"),
                ("add_action"),
            ]
        )
        .set_refresh()
        .set_propagate()
        .get_list_attribute("selected", AttributeType.number)
        .set_refresh_on_update()
        .set_table_pagesize_options(),
        "toggle": lambda control_type, attrs: Builder(
            control_type=control_type, element_name="Toggle", attributes=attrs, default_value=""
        )
        .set_value_and_default(with_default=False)
        .set_classNames(class_name="taipy-toggle", config_class="toggle")
        .get_adapter("lov", multi_selection=False)  # need to be called before set_lov
        .set_lov()
        .set_attributes(
            [
                ("id"),
                ("label"),
                ("active", AttributeType.dynamic_boolean, True),
                ("unselected_value", AttributeType.string, ""),
            ]
        )
        .set_kind()
        .set_refresh_on_update()
        .set_propagate(),
        "tree": lambda control_type, attrs: Builder(
            control_type=control_type,
            element_name="TreeView",
            attributes=attrs,
        )
        .set_value_and_default(with_default=False)
        .set_classNames(class_name="taipy-tree", config_class="tree")
        .get_adapter("lov")  # need to be called before set_lov
        .set_lov()
        .set_attributes(
            [
                ("filter", AttributeType.boolean),
                ("multiple", AttributeType.boolean),
                ("id"),
                ("active", AttributeType.dynamic_boolean, True),
                ("height", AttributeType.string_or_number),
                ("width", AttributeType.string_or_number),
            ]
        )
        .set_refresh_on_update()
        .set_propagate(),
    }

    # TODO: process \" in property value
    _PROPERTY_RE = re.compile(r"\s+([a-zA-Z][\.a-zA-Z_$0-9]*(?:\[(?:.*?)\])?)=\"((?:(?:(?<=\\)\")|[^\"])*)\"")

    @staticmethod
    def get_default_property_name(control_name: str) -> t.Optional[str]:
        return Factory.__CONTROL_DEFAULT_PROP_NAME.get(control_name.split(".", 1)[0])
