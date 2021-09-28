class SampleDenyPermission:
    def has_setting_permission(self, request):
        return False


class SampleAllowPermission:
    def has_setting_permission(self, request):
        return True
