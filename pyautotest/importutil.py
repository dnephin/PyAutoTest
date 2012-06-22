


def import_module(module_path):
    """
    >>> p = import_module('logging.handlers'); p    # doctest: +ELLIPSIS
    <module 'logging.handlers' from ...>

    >>> p = import_module('logging'); p             # doctest: +ELLIPSIS
    <module 'logging' from ...>
    """
    path_parts      = module_path.rsplit('.')
    if len(path_parts) == 1:
        return __import__(module_path)

    package, module = path_parts
    pkg = __import__(package, fromlist=[module])
    return getattr(pkg, module)