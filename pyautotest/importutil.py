


def import_module(module_path):
    """
    >>> p = import_module('logging.handlers'); p    # doctest: +ELLIPSIS
    <module 'logging.handlers' from ...>

    >>> p = import_module('logging'); p             # doctest: +ELLIPSIS
    <module 'logging' from ...>
    """
    path_parts      = module_path.rsplit('.', 1)
    if len(path_parts) == 1:
        return __import__(module_path)

    package, module = path_parts
    pkg = __import__(package, fromlist=[module])
    return getattr(pkg, module)


def from_config_factory(base_name, mod_getter, name_mapping):
    var_module  = '%s_%s' % (base_name, 'module')
    var_name    = '%s_%s' % (base_name, 'name')

    def from_config(config):
        module_name = config.get(var_module)
        if module_name:
            mod = import_module(module_name)
            return getattr(mod, mod_getter)()

        name = config.get(var_name)
        if name not in name_mapping:
            raise ValueError("Unknown %s: %s" % (var_name, name))
        return name_mapping[name]

    return from_config