class ConfigClear:
    REPLACE_PAIRS = {
        r'.*'   : 'jira.example.com',
        r'..*'  : 'chernyaksergey@gmail.com',
        r'...*' : 'sergey',
        r'....*': 'Ideal inc.',

    }
    """key is a patter for re.sub, a dict value is a replacement."""
