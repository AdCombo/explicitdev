from sqlalchemy.ext.declarative import DeclarativeMeta

def get_attrs_dict_include_parents(bases: list, current_class_attrs: dict) -> dict:
    """
    Возвращает Dict со всеми атрибутами класса, включая атрибуты его родителей.
    Учитывается порядок наследования. Не учитывается глубина наследования больше двух,
    т.е. в этом словаре не будет атрибутов родителей родителя класса
    :param bases: список из классов-родителей
    :param current_class_attrs: dict с атрибутами current_class
    :return: Dict
    """
    attrs_dict = {}

    for parent_class in reversed(bases):
        attrs_dict.update(parent_class.__dict__)

    attrs_dict.update(current_class_attrs)
    return attrs_dict

class AutoNamedClassAttrs(type):

    def __new__(mcs, name, bases, dict_):
        attrs_dict = get_attrs_dict_include_parents(bases, dict_)
        for key, value in attrs_dict.items():
            if key.startswith('__') or callable(value):
                continue
            attrs_dict[key] = key
        return type.__new__(mcs, name, (), attrs_dict)


class AutoNamedModelAttrs(AutoNamedClassAttrs, DeclarativeMeta):

    def __init__(cls, classname, bases, dict_):
        type.__init__(cls, classname, bases, dict_)

    def __setattr__(cls, key, value):
        type.__setattr__(cls, key, value)