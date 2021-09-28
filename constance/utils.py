from .settings import DEFAULT_SETTING_PERMISSIONS
from importlib import import_module
from django.utils.module_loading import import_string


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def has_setting_permission(request, permissions=None):
    if permissions is None:
        permissions = DEFAULT_SETTING_PERMISSIONS

    if permissions is None:
        return True

    modules = []
    if not isinstance(permissions, (list, tuple)):
        permissions = [permissions]

    for permission in permissions:
        if isinstance(permission, str):
            modules.append(import_string(permission))
        else:
            modules.append(permission)

    results = []
    for module in modules:
        if hasattr(module, 'has_setting_permission'):
            results.append(module().has_setting_permission(request))
        else:
            raise AttributeError(
                f'{module} doesn\'t contain a has_setting_permission method'
            )

    return results and all(results)
