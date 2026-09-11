
from django.urls import path

from .views import (
    QuotationListCreateView,
    QuotationDetailView,
    QuotationItemListCreateView,
    QuotationItemDetailView,
    QuotationApprovalView,
    QuotationPrintView,
)


urlpatterns = [

    # ========================================================
    # QUOTATIONS
    # ========================================================

    path(
        "",
        QuotationListCreateView.as_view(),
        name="quotation-list-create",
    ),

    path(
        "<int:pk>/",
        QuotationDetailView.as_view(),
        name="quotation-detail",
    ),

    # ========================================================
    # APPROVAL
    # ========================================================

    path(
        "<int:pk>/approve/",
        QuotationApprovalView.as_view(),
        name="quotation-approve",
    ),

    # ========================================================
    # PRINT
    # ========================================================

    path(
        "<int:pk>/print/",
        QuotationPrintView.as_view(),
        name="quotation-print",
    ),

    # ========================================================
    # ITEMS
    # ========================================================

    path(
        "<int:quotation_id>/items/",
        QuotationItemListCreateView.as_view(),
        name="quotation-item-list-create",
    ),

    path(
        "<int:quotation_id>/items/<int:item_id>/",
        QuotationItemDetailView.as_view(),
        name="quotation-item-detail",
    ),
]
