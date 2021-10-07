from .settings import DEFAULT_SETTING_PERMISSIONS
from importlib import import_module
from django.utils.module_loading import import_string


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def get_permission_module(module_name):
    if isinstance(module_name, str):
        return import_string(module_name)
    else:
        return module_name

def has_permission(permission, request):
    if permission is None:
        return True

    module = get_permission_module(permission)

    if hasattr(module, 'has_setting_permission'):
        return module().has_setting_permission(request)
    else:
        raise AttributeError(
            f'{module} doesn\'t contain a has_setting_permission method'
        )


def has_setting_permission(request, permissions=None):
    if permissions is None:
        permissions = DEFAULT_SETTING_PERMISSIONS

    if permissions is None:
        return True

    if DEFAULT_SETTING_PERMISSIONS and has_permission(DEFAULT_SETTING_PERMISSIONS, request):
        return True

    if not isinstance(permissions, (list, tuple)):
        permissions = [permissions]

    results = []
    for permission in permissions:
        results.append(has_permission(permission, request))

    return results and all(results)
