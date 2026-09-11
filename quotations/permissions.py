from rest_framework.permissions import BasePermission


# ============================================================
# QUOTATION VIEWER
# ============================================================

class IsQuotationViewer(BasePermission):
    """
    Users who are allowed to view quotations.
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


# ============================================================
# FRONT DESK OR ADMIN
# ============================================================

class IsFrontDeskOrAdmin(BasePermission):
    """
    Front Desk can create/edit/delete quotations.
    Admin can also perform these actions.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "front_desk",
                "admin",
            ]
        )


# ============================================================
# ACCOUNTANT OR ADMIN
# ============================================================

class IsAccountantOrAdmin(BasePermission):
    """
    Accountants and Admins can approve quotations
    and manage production orders.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "accountant",
                "admin",
            ]
        )


# ============================================================
# DOCUMENT PRINTER
# ============================================================

class IsDocumentPrinter(BasePermission):
    """
    Front Desk, Accountants and Admins can print
    approved quotations and production orders.
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