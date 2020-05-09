def get_nested_dict(dict_, *args, fallback_value=None):
    if not isinstance(dict_, dict):
        return fallback_value

    args = list(args)
    first_key = args.pop(0)
    try:
        nested_value = dict_[first_key]
    except KeyError:
        return fallback_value
    if not len(args):
        return nested_value

    return get_nested_dict(nested_value, *args, fallback_value=fallback_value)


def get_name_or_empty(dict_: dict, key: str):
    """
    Get value from nested dict with predifined arguments.
    :param dict_:
    :param key:
    :return:
    """
    return get_nested_dict(dict_, key, 'name', fallback_value='')