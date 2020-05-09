from types import (
    ModuleType,
    FunctionType,
)
from typing import Union
from unittest.mock import *


def patch_imported(target: str, imported_object: Union[ModuleType, type], autospec: bool = True) -> patch:
    """
    Custom path for imported modules and classes with enabled autospec by default.

    :param target:
    :param namespace_object:
    :param autospec:
    :return:
    """
    if isinstance(imported_object, ModuleType):
        qualified_name = imported_object.__name__
    elif isinstance(imported_object, (type, FunctionType)):
        qualified_name = imported_object.__module__
    else:
        raise TypeError("Wrong type for search qualified name.")

    target = f"{qualified_name}.{target}"
    return patch(target, autospec=autospec)
