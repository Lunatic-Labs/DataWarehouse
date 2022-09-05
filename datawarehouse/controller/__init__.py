from pkgutil import walk_packages
from flask import Blueprint
from collections import defaultdict

__blueprint_map__ = defaultdict(list)
for loader, module_name, is_pkg in walk_packages(__path__):
    _module = loader.find_module(module_name).load_module(module_name)
    for k, v in vars(_module).items():
        if isinstance(v, Blueprint):
            parent_module, *child_module = module_name.split(".")
            if child_module:
                __blueprint_map__[parent_module].append(v)
            else:
                __blueprint_map__[parent_module].insert(0, v)


def register_blueprints(app):
    for k, v in __blueprint_map__.items():
        _parent, *_children = v
        for _child in _children:
            _parent.register_blueprint(_child)
        app.register_blueprint(_parent)
