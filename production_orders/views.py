from django.shortcuts import get_object_or_404, render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quotations.models import Quotation

from .models import ProductionOrder
from .serializers import (
    ProductionOrderSerializer,
    ProductionOrderCreateSerializer,
)
# ============================================================
# ROLE HELPERS
# ============================================================

ACCOUNTANT_ROLES = ["accountant", "admin"]

VIEW_ROLES = [
    "front_desk",
    "accountant",
    "admin",
]

PRINT_ROLES = [
    "front_desk",
    "accountant",
    "admin",
]


# ============================================================
# PRODUCTION ORDER LIST + CREATE
# ============================================================

class ProductionOrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in VIEW_ROLES:
            return Response(
                {
                    "detail": (
                        "You do not have permission "
                        "to view production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        orders = (
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            )
            .all()
            .order_by("-created_at")
        )

        serializer = ProductionOrderSerializer(
            orders,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        # ----------------------------------------------------
        # ONLY ACCOUNTANTS AND ADMINS
        # ----------------------------------------------------

        if request.user.role not in ACCOUNTANT_ROLES:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can create production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        quotation_id = request.data.get("quotation")

        if not quotation_id:
            return Response(
                {
                    "quotation": [
                        "Quotation is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        quotation = get_object_or_404(
            Quotation.objects.select_related(
                "customer"
            ),
            pk=quotation_id,
        )

        # ----------------------------------------------------
        # QUOTATION MUST BE APPROVED
        # ----------------------------------------------------

        if not quotation.approved:
            return Response(
                {
                    "detail": (
                        "Production order can only be "
                        "created from an approved quotation."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # PREVENT DUPLICATE
        # ----------------------------------------------------

        if ProductionOrder.objects.filter(
            quotation=quotation
        ).exists():

            return Response(
                {
                    "detail": (
                        "A production order already exists "
                        "for this quotation."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductionOrderCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        order = serializer.save(
            quotation=quotation,
            customer=quotation.customer,
        )

        order = (
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            )
            .get(pk=order.pk)
        )

        return Response(
            ProductionOrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# PRODUCTION ORDER DETAIL
# ============================================================

class ProductionOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            ),
            pk=pk,
        )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def get(self, request, pk):

        if request.user.role not in VIEW_ROLES:
            return Response(
                {
                    "detail": (
                        "You do not have permission "
                        "to view production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object(pk)

        return Response(
            ProductionOrderSerializer(order).data
        )

    # --------------------------------------------------------
    # PATCH
    # --------------------------------------------------------

    def patch(self, request, pk):

        if request.user.role not in ACCOUNTANT_ROLES:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can edit production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object(pk)

        if order.approved:
            return Response(
                {
                    "detail": (
                        "Approved production orders "
                        "cannot be edited."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductionOrderCreateSerializer(
            order,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        order = self.get_object(pk)

        return Response(
            ProductionOrderSerializer(order).data
        )

    # --------------------------------------------------------
    # PUT
    # --------------------------------------------------------

    def put(self, request, pk):

        if request.user.role not in ACCOUNTANT_ROLES:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can edit production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object(pk)

        if order.approved:
            return Response(
                {
                    "detail": (
                        "Approved production orders "
                        "cannot be edited."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductionOrderCreateSerializer(
            order,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        order = self.get_object(pk)

        return Response(
            ProductionOrderSerializer(order).data
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete(self, request, pk):

        if request.user.role not in ACCOUNTANT_ROLES:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can delete production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object(pk)

        if order.approved:
            return Response(
                {
                    "detail": (
                        "Approved production orders "
                        "cannot be deleted."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================
# PRODUCTION ORDER APPROVAL
# ============================================================

class ProductionOrderApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if request.user.role not in ACCOUNTANT_ROLES:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can approve production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        order = get_object_or_404(
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            ),
            pk=pk,
        )

        if order.approved:
            return Response(
                {
                    "detail": (
                        "Production order is already approved."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            order.quotation
            and not order.quotation.approved
        ):
            return Response(
                {
                    "detail": (
                        "The quotation must be approved "
                        "before approving the production order."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.approved = True

        order.save(
            update_fields=[
                "approved",
                "updated_at",
            ]
        )

        order = (
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            )
            .get(pk=order.pk)
        )

        return Response(
            {
                "message": (
                    "Production order approved successfully."
                ),
                "production_order": ProductionOrderSerializer(
                    order
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# CREATE PRODUCTION ORDER FROM QUOTATION
# ============================================================

class CreateProductionOrderFromQuotationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quotation_id):

        if request.user.role not in ACCOUNTANT_ROLES:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can create production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        quotation = get_object_or_404(
            Quotation.objects.select_related(
                "customer"
            ),
            pk=quotation_id,
        )

        if not quotation.approved:
            return Response(
                {
                    "detail": (
                        "This quotation must be approved "
                        "before a production order can be created."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_order = (
            ProductionOrder.objects
            .filter(quotation=quotation)
            .select_related(
                "quotation",
                "customer",
                "product",
            )
            .first()
        )

        if existing_order:
            return Response(
                {
                    "detail": (
                        "A production order already exists "
                        "for this quotation."
                    ),
                    "production_order": ProductionOrderSerializer(
                        existing_order
                    ).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_id = request.data.get("product")

        if not product_id:
            return Response(
                {
                    "product": [
                        "Product is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "product": product_id,
            "marketer_name": request.data.get(
                "marketer_name",
                "MD's Customer",
            ),
            "remark": request.data.get(
                "remark"
            ),
        }

        if "meter_run" in request.data:
            data["meter_run"] = request.data.get(
                "meter_run"
            )

        if "bundles" in request.data:
            data["bundles"] = request.data.get(
                "bundles"
            )

        if "length" in request.data:
            data["length"] = request.data.get(
                "length"
            )

        serializer = ProductionOrderCreateSerializer(
            data=data
        )

        serializer.is_valid(
            raise_exception=True
        )

        order = serializer.save(
            quotation=quotation,
            customer=quotation.customer,
        )

        order = (
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            )
            .get(pk=order.pk)
        )

        return Response(
            {
                "message": (
                    "Production order created successfully."
                ),
                "production_order": ProductionOrderSerializer(
                    order
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# PRODUCTION ORDER PRINT
# ============================================================

class ProductionOrderPrintView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # ----------------------------------------------------
        # FRONT DESK + ACCOUNTANT + ADMIN CAN PRINT
        # ----------------------------------------------------

        if request.user.role not in PRINT_ROLES:
            return Response(
                {
                    "detail": (
                        "You do not have permission "
                        "to print production orders."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        order = get_object_or_404(
            ProductionOrder.objects
            .select_related(
                "quotation",
                "customer",
                "product",
            ),
            pk=pk,
        )

        # ----------------------------------------------------
        # ONLY APPROVED ORDERS CAN BE PRINTED
        # ----------------------------------------------------

        if not order.approved:
            return Response(
                {
                    "detail": (
                        "Only approved production orders "
                        "can be printed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return render(
            request,
            "production_orders/production_order_print.html",
            {
                "order": order,
            },
        )