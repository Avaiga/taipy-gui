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

import typing as t
import warnings
from abc import ABC, abstractmethod
from pathlib import Path

from ..renderers.builder import Builder
from ..renderers.utils import _to_camel_case
from ..types import PropertyType

if t.TYPE_CHECKING:
    from ..gui import Gui


class ElementProperty:
    """
    The declaration of a property of a visual element.

    Each visual element property is described by an instance of `ElementProperty`.
    This class holds the information on the name, type and default value for the
    element property.
    """

    def __init__(
        self,
        name: str,
        property_type: PropertyType,
        default_value: t.Optional[t.Any] = None,
        js_name: t.Optional[str] = None,
    ) -> None:
        """

        Arguments:
            name (str): The attribute name. This must be a valid Python identifier.
            property_type (PropertyType): The type of this property.
            default_value (Optional[Any]): The default value for this property. Default is None.
            js_name (Optional[str]): The name of this property, in the front-end JavaScript code.<br/>
                If unspecified, a camel case version of `name` is generated: for example, if `name` is
                "my_property_name", then this property is referred to as "myPropertyName" in the
                JavaScript code.
        """
        self.name = name
        self.property_type = property_type
        self.default_value = default_value
        self.js_name = js_name if js_name else _to_camel_case(self.name)
        super().__init__()

    def check(self, control: str):
        if not isinstance(self.name, str) or not self.name or not self.name.isidentifier():
            warnings.warn(f"Element '{control}' should have a valid attribute name '{self.name}'")
        if not isinstance(self.property_type, PropertyType):
            warnings.warn(f"Element Property '{control}.{self.name}' should have a valid type '{self.property_type}'")

    def _get_tuple(self) -> tuple:
        return (self.name, self.property_type, self.default_value)


class Element:
    """
    The definition of a custom visual element.

    The definition of an element is made of its names, its properties, and
    the
    TODO
    """

    def __init__(
        self,
        name: str,
        default_property: str,
        properties: t.List[ElementProperty],
        js_name: t.Optional[str] = None,
        render: t.Optional[t.Callable] = None,
    ) -> None:
        """
        Arguments:
            name (str): The name of this element.
            default_property (str): the default property for this element.
            properties (List[ElementProperty]): The list of properties for this element.
            js_name (Optional[str]): The name of the component to be created on the frontend
                If not specified, it is set to a camel case version of `name`.
            render (Optional[callable]): A function that has the same signature as `Element.render`
                and that will replace it if defined.
        """
        self.name = name
        self.default_attribute = default_property
        self.attributes = properties
        self.js_name = js_name
        if callable(render):
            self._render = render
        super().__init__()

    def _get_js_name(self) -> str:
        return self.js_name or _to_camel_case(self.name)

    def check(self):
        if not isinstance(self.name, str) or not self.name or not self.name.isidentifier():
            warnings.warn(f"Element should have a valid name '{self.name}'")
        default_found = False
        for attr in self.attributes or []:
            if isinstance(attr, ElementProperty):
                attr.check(self.name)
                if not default_found:
                    default_found = self.default_attribute == attr.name
            else:
                warnings.warn(f"Attribute should inherit from 'ElementProperty' '{self.name}.{attr}'")
        if not default_found:
            warnings.warn(
                f"User Default Attribute should be describe in the 'properties' List '{self.name}{self.default_property}'"
            )

    def _call_builder(
        self,
        gui: "Gui",
        properties: t.Union[t.Dict[str, t.Any], None],
        lib_name: str,
        is_html: t.Optional[bool] = False,
    ) -> t.Union[t.Any, t.Tuple[str, str]]:
        attributes = properties or {}
        hash_names = Builder._get_variable_hash_names(gui, attributes)
        default_attr: t.Optional[ElementProperty] = None
        default_value = None
        attrs = []
        for ua in self.attributes or []:
            if isinstance(ua, ElementProperty):
                if self.default_attribute == ua.name:
                    default_attr = ua
                    default_value = ua.default_value
                else:
                    attrs.append(ua._get_tuple())
        elt_built = Builder(
            gui=gui,
            control_type=self.name,
            element_name=self._get_js_name(),
            attributes=properties,
            hash_names=hash_names,
            lib_name=lib_name,
            default_value=default_value,
        )
        if default_attr is not None:
            elt_built.set_value_and_default(
                var_name=default_attr.name,
                var_type=default_attr.property_type,
                default_val=default_attr.default_value,
                with_default=default_attr.property_type != PropertyType.data,
            )
        elt_built.set_attributes(attrs)
        # call user render
        self.render(gui, attributes, hash_names, elt_built)
        return elt_built._build_to_string() if is_html else elt_built.el

    def render(self, gui: "Gui", properties: t.Dict[str, t.Any], hash_names: t.Dict[str, str], builder: Builder):
        """
        TODO
        Uses the builder to update the xml node.

        Arguments:

            gui (Gui): The current instance of Gui.
            properties (t.Dict[str, t.Any]): The dict containing a value for each defined property.
            hash_names (t.Dict[str, str]): The dict containing the internal variable name for each
                bound variable.
            builder (Builder): the `Builder^` instance that has been initialized and used by Taipy to
                start the rendering.

        """
        if hasattr(self, "_render") and callable(self._render):
            self._render(gui, properties, hash_names, builder)


class ElementLibrary(ABC):
    """
    A library of user-defined visual elements.

    TODO
    """

    @abstractmethod
    def get_elements(self) -> t.List[Element]:
        """
        Returns the list of all visual element declarations.

        The default implementation returns an empty list, indicating that this library contains
        no custom visual elements.
        """
        return []

    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the library name.

        TODO:
        - What is this name used for?
        - What if two libraries with the same same get added to the Gui?
        """
        return NotImplemented

    def get_js_module_name(self) -> str:
        """
        Returns the name of the Javascript module.

        Typically, Javascript module names use camel case.

        This module name must be unique on the browser window scope.

        Returns:
            The name of the Javascript module.<br/>
            The default implementation returns `self.get_name()`.
        """
        return self.get_name()

    @abstractmethod
    def get_scripts(self) -> t.List[str]:
        """
        Returns the list of resources names for the scripts.

        The default implementation returns an empty list, indicating that this library contains
        no custom visual elements.
        TODO: Clarify - this is wrong:
            May be this should return some <lib_name>.js...
        """
        return []

    @abstractmethod
    def get_styles(self) -> t.List[str]:
        """
        TODO
        Returns the list of resources names for the css stylesheets.
        Defaults to []

        """
        return []

    @abstractmethod
    def get_resource(self, name: str) -> Path:
        """
        TODO
        Defaults to return None?
        Returns a path for a resource name.
        Resource URL should be formed as /taipy-extensions/<library_name>/<resource virtual path> with
        - <resource virtual path> being the `name` parameter
        - <library_name> the value returned by `get_name()`

        Arguments:

            name (str): The name of the resource for which a local Path should be returned.
        """
        return NotImplemented

    @abstractmethod
    def get_register_js_function(self) -> str:
        """
        TODO
        Returns the name of the function that will register new js components.
            signature (libName: string) => Record<string, ComponentType>
        """
        return NotImplemented

    def get_data(self, library_name: str, payload: t.Dict, var_name: str, value: t.Any) -> t.Optional[t.Dict]:
        """
        TODO
        Called if implemented (ie returns a dict).

        Arguments:

            library_name (str): The name of this library.
            payload (t.Dict): The payload send by the `createRequestDataUpdateAction` frontend function.
            var_name (str): The name of the variable holding the data.
            value (t.Any): The current value of the variable identified by `var_name`.
        """
        return None
