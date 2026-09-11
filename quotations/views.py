from decimal import Decimal

from django.shortcuts import get_object_or_404, render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quotation, QuotationItem

from .serializers import (
    QuotationSerializer,
    QuotationCreateSerializer,
    QuotationItemSerializer,
    QuotationItemCreateSerializer,
)

from .permissions import (
    IsQuotationViewer,
    IsFrontDeskOrAdmin,
    IsAccountantOrAdmin,
    IsDocumentPrinter,
)

# ============================================================
# QUOTATION LIST + CREATE
# ============================================================

class QuotationListCreateView(APIView):

    def get_permissions(self):

        # Everyone involved in quotations can VIEW
        if self.request.method == "GET":
            return [IsQuotationViewer()]

        # Only Front Desk and Admin can CREATE
        return [IsFrontDeskOrAdmin()]

    def get(self, request):

        quotations = (
            Quotation.objects
            .select_related(
                "customer",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            )
            .all()
            .order_by("-quotation_date")
        )

        serializer = QuotationSerializer(
            quotations,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = QuotationCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        quotation = serializer.save(
            created_by=request.user
        )

        # ----------------------------------------------------
        # CREATE ITEMS
        # ----------------------------------------------------

        items = request.data.get("items", [])

        for item_data in items:

            item_serializer = QuotationItemCreateSerializer(
                data=item_data
            )

            item_serializer.is_valid(
                raise_exception=True
            )

            item_serializer.save(
                quotation=quotation
            )

        # ----------------------------------------------------
        # RELOAD
        # ----------------------------------------------------

        quotation = (
            Quotation.objects
            .select_related(
                "customer",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            )
            .get(pk=quotation.pk)
        )

        return Response(
            QuotationSerializer(
                quotation
            ).data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# QUOTATION DETAIL
# ============================================================

class QuotationDetailView(APIView):

    def get_permissions(self):

        # Everyone can view
        if self.request.method == "GET":
            return [IsQuotationViewer()]

        # Only Front Desk/Admin can modify
        return [IsFrontDeskOrAdmin()]

    def get_object(self, pk):

        return get_object_or_404(
            Quotation.objects
            .select_related(
                "customer",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            ),
            pk=pk,
        )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def get(self, request, pk):

        quotation = self.get_object(pk)

        serializer = QuotationSerializer(
            quotation
        )

        return Response(serializer.data)

    # --------------------------------------------------------
    # PATCH
    # --------------------------------------------------------

    def patch(self, request, pk):

        quotation = self.get_object(pk)

        # Do not modify approved quotations
        if quotation.approved:

            return Response(
                {
                    "detail": (
                        "Approved quotations cannot be edited."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuotationCreateSerializer(
            quotation,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        quotation = self.get_object(pk)

        return Response(
            QuotationSerializer(
                quotation
            ).data
        )

    # --------------------------------------------------------
    # PUT
    # --------------------------------------------------------

    def put(self, request, pk):

        quotation = self.get_object(pk)

        if quotation.approved:

            return Response(
                {
                    "detail": (
                        "Approved quotations cannot be edited."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuotationCreateSerializer(
            quotation,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        quotation = self.get_object(pk)

        return Response(
            QuotationSerializer(
                quotation
            ).data
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete(self, request, pk):

        quotation = self.get_object(pk)

        if quotation.approved:

            return Response(
                {
                    "detail": (
                        "Approved quotations cannot be deleted."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        quotation.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================
# QUOTATION ITEMS
# ============================================================

class QuotationItemListCreateView(APIView):

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsQuotationViewer()]

        return [IsFrontDeskOrAdmin()]

    def get_quotation(self, quotation_id):

        return get_object_or_404(
            Quotation,
            pk=quotation_id,
        )

    def get(self, request, quotation_id):

        quotation = self.get_quotation(
            quotation_id
        )

        items = (
            quotation.items
            .select_related("product")
            .all()
        )

        serializer = QuotationItemSerializer(
            items,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, quotation_id):

        quotation = self.get_quotation(
            quotation_id
        )

        if quotation.approved:

            return Response(
                {
                    "detail": (
                        "Items cannot be added to "
                        "an approved quotation."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuotationItemCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        item = serializer.save(
            quotation=quotation
        )

        return Response(
            QuotationItemSerializer(item).data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# QUOTATION ITEM DETAIL
# ============================================================

class QuotationItemDetailView(APIView):

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsQuotationViewer()]

        return [IsFrontDeskOrAdmin()]

    def get_object(
        self,
        quotation_id,
        item_id,
    ):

        return get_object_or_404(
            QuotationItem.objects
            .select_related(
                "product",
                "quotation",
            ),
            pk=item_id,
            quotation_id=quotation_id,
        )

    def get(
        self,
        request,
        quotation_id,
        item_id,
    ):

        item = self.get_object(
            quotation_id,
            item_id,
        )

        return Response(
            QuotationItemSerializer(
                item
            ).data
        )

    def patch(
        self,
        request,
        quotation_id,
        item_id,
    ):

        item = self.get_object(
            quotation_id,
            item_id,
        )

        if item.quotation.approved:

            return Response(
                {
                    "detail": (
                        "Items in an approved quotation "
                        "cannot be edited."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuotationItemCreateSerializer(
            item,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            QuotationItemSerializer(
                item
            ).data
        )

    def put(
        self,
        request,
        quotation_id,
        item_id,
    ):

        item = self.get_object(
            quotation_id,
            item_id,
        )

        if item.quotation.approved:

            return Response(
                {
                    "detail": (
                        "Items in an approved quotation "
                        "cannot be edited."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuotationItemCreateSerializer(
            item,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            QuotationItemSerializer(
                item
            ).data
        )

    def delete(
        self,
        request,
        quotation_id,
        item_id,
    ):

        item = self.get_object(
            quotation_id,
            item_id,
        )

        if item.quotation.approved:

            return Response(
                {
                    "detail": (
                        "Items in an approved quotation "
                        "cannot be deleted."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        item.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================
# QUOTATION APPROVAL
# ============================================================

class QuotationApprovalView(APIView):

    permission_classes = [
        IsAccountantOrAdmin
    ]

    def post(self, request, pk):

        quotation = get_object_or_404(
            Quotation,
            pk=pk,
        )

        if quotation.approved:

            return Response(
                {
                    "detail": (
                        "Quotation is already approved."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        quotation.approved = True

        quotation.save(
            update_fields=[
                "approved",
                "updated_at",
            ]
        )

        quotation = (
            Quotation.objects
            .select_related(
                "customer",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            )
            .get(pk=quotation.pk)
        )

        return Response(
            {
                "message": (
                    "Quotation approved successfully."
                ),
                "quotation": QuotationSerializer(
                    quotation
                ).data,
            }
        )



# ============================================================
# QUOTATION PRINT
# ============================================================

class QuotationPrintView(APIView):
    permission_classes = [IsDocumentPrinter]

    def get(self, request, pk):

        quotation = get_object_or_404(
            Quotation.objects
            .select_related(
                "customer",
                "created_by",
            )
            .prefetch_related(
                "items__product",
            ),
            pk=pk,
        )

        # ----------------------------------------------------
        # ONLY APPROVED QUOTATIONS CAN BE PRINTED
        # ----------------------------------------------------

        if not quotation.approved:
            return Response(
                {
                    "detail": (
                        "Only approved quotations "
                        "can be printed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # CALCULATE ITEMS + SUBTOTAL
        # ----------------------------------------------------

        subtotal = Decimal("0.00")

        items = []

        for item in quotation.items.all():

            quantity = item.quantity or Decimal("0.00")
            unit_price = item.unit_price or Decimal("0.00")

            line_total = quantity * unit_price

            subtotal += line_total

            items.append({
                "item": item,
                "line_total": line_total,
            })

        # ----------------------------------------------------
        # DISCOUNT
        # ----------------------------------------------------

        discount = (
            quotation.discount
            or Decimal("0.00")
        )

        # Never allow a negative discount
        if discount < Decimal("0.00"):
            discount = Decimal("0.00")

        # ----------------------------------------------------
        # FINAL TOTAL
        # ----------------------------------------------------

        total = subtotal - discount

        # Never allow negative quotation total
        if total < Decimal("0.00"):
            total = Decimal("0.00")

        # ----------------------------------------------------
        # RENDER PRINT PAGE
        # ----------------------------------------------------

        return render(
            request,
            "quotations/quotation_print.html",
            {
                "quotation": quotation,
                "items": items,
                "subtotal": subtotal,
                "discount": discount,
                "total": total,
            },
        )
