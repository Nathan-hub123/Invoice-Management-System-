from django.urls import path

from .views import (
    ProductionOrderListCreateView,
    ProductionOrderDetailView,
    ProductionOrderApprovalView,
    CreateProductionOrderFromQuotationView,
    ProductionOrderPrintView,
)


urlpatterns = [

    # ========================================================
    # LIST + CREATE
    # ========================================================

    path(
        "",
        ProductionOrderListCreateView.as_view(),
        name="production-order-list-create",
    ),

    # ========================================================
    # CREATE FROM QUOTATION
    # ========================================================

    path(
        "from-quotation/<int:quotation_id>/",
        CreateProductionOrderFromQuotationView.as_view(),
        name="production-order-from-quotation",
    ),

    # ========================================================
    # APPROVAL
    # ========================================================

    path(
        "<int:pk>/approve/",
        ProductionOrderApprovalView.as_view(),
        name="production-order-approve",
    ),

    # ========================================================
    # PRINT
    # ========================================================

    path(
        "<int:pk>/print/",
        ProductionOrderPrintView.as_view(),
        name="production-order-print",
    ),

    # ========================================================
    # DETAIL
    # ========================================================

    path(
        "<int:pk>/",
        ProductionOrderDetailView.as_view(),
        name="production-order-detail",
    ),
]