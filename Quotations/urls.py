from django.urls import path

from .views import (
    QuotationListCreateView,
    QuotationDetailView,
    QuotationItemListCreateView,
    QuotationItemDetailView,
    QuotationApprovalView,
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
    # QUOTATION APPROVAL
    # ========================================================

    path(
        "<int:pk>/approve/",
        QuotationApprovalView.as_view(),
        name="quotation-approve",
    ),

    # ========================================================
    # QUOTATION ITEMS
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