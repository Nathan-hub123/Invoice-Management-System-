from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsAccountant(BasePermission):
    """
    Allows access only to accountant users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "accountant"
        )


class IsFrontDesk(BasePermission):
    """
    Allows access only to front desk users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "front_desk"
        )


class IsAdminOrAccountant(BasePermission):
    """
    Allows access to admins and accountants.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "admin",
                "accountant",
            ]
        )


class IsAdminOrFrontDesk(BasePermission):
    """
    Allows access to admins and front desk users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "admin",
                "front_desk",
            ]
        )
    

class IsDocumentPrinter(BasePermission):
    """
    Front Desk, Accountant and Admin can print documents.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "front_desk",
                "accountant",
                "admin",
            ]
        )
