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

import inspect
import typing as t

from .page import Page


class ClassModule:
    pass


def get_page_from_class_module(cls: t.Type) -> Page:
    cls_locals = {}
    valid_func = []
    for i in inspect.getmembers(cls):
        if not i[0].startswith("_") and (inspect.ismethod(i[1]) or inspect.isfunction(i[1])):
            valid_func.append(i[0])
    cls_instance = cls()
    for k, v in cls_instance.__dict__.items():
        cls_locals[k] = v
    for f in valid_func:
        cls_locals[f] = getattr(cls_instance, f).__func__
    if "page" not in cls_locals:
        raise AttributeError(f"Class {get_class_name(cls)} must have a page attribute")
    if not isinstance(cls_locals["page"], Page):
        raise AttributeError(f"Class {get_class_name(cls)} has incorrect type for page attribute")
    page = cls_locals["page"]
    del cls_locals["page"]
    page._set_class_module(get_class_name(cls), cls_locals)
    return page


def get_class_name(cls: t.Type):
    return cls.__name__
