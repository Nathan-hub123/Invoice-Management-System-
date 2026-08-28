from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quotation, QuotationItem
from .serializers import (
    QuotationSerializer,
    QuotationCreateSerializer,
    QuotationItemSerializer,
    QuotationItemCreateSerializer,
)


# ============================================================
# QUOTATION LIST + CREATE
# ============================================================

class QuotationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quotations = (
            Quotation.objects
            .select_related("customer", "created_by")
            .prefetch_related("items__product")
            .all()
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

        serializer.is_valid(raise_exception=True)

        quotation = serializer.save(
            created_by=request.user
        )

        # Optional support for creating items together
        items = request.data.get("items", [])

        for item_data in items:
            item_serializer = QuotationItemCreateSerializer(
                data=item_data
            )

            item_serializer.is_valid(raise_exception=True)

            item_serializer.save(
                quotation=quotation
            )

        quotation = (
            Quotation.objects
            .select_related("customer", "created_by")
            .prefetch_related("items__product")
            .get(pk=quotation.pk)
        )

        return Response(
            QuotationSerializer(quotation).data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# QUOTATION DETAIL
# ============================================================

class QuotationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(
            Quotation.objects
            .select_related("customer", "created_by")
            .prefetch_related("items__product"),
            pk=pk,
        )

    def get(self, request, pk):
        quotation = self.get_object(pk)

        serializer = QuotationSerializer(
            quotation
        )

        return Response(serializer.data)

    def patch(self, request, pk):
        quotation = self.get_object(pk)

        serializer = QuotationCreateSerializer(
            quotation,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        quotation = self.get_object(pk)

        return Response(
            QuotationSerializer(quotation).data
        )

    def put(self, request, pk):
        quotation = self.get_object(pk)

        serializer = QuotationCreateSerializer(
            quotation,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        quotation = self.get_object(pk)

        return Response(
            QuotationSerializer(quotation).data
        )

    def delete(self, request, pk):
        quotation = self.get_object(pk)

        quotation.delete()

        return Response(
            {
                "message": "Quotation deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )


# ============================================================
# QUOTATION ITEM LIST + CREATE
# ============================================================

class QuotationItemListCreateView(APIView):
    permission_classes = [IsAuthenticated]

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

        serializer = QuotationItemCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

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
    permission_classes = [IsAuthenticated]

    def get_object(self, quotation_id, item_id):
        return get_object_or_404(
            QuotationItem.objects
            .select_related("product", "quotation"),
            pk=item_id,
            quotation_id=quotation_id,
        )

    def get(self, request, quotation_id, item_id):
        item = self.get_object(
            quotation_id,
            item_id,
        )

        serializer = QuotationItemSerializer(
            item
        )

        return Response(serializer.data)

    def patch(self, request, quotation_id, item_id):
        item = self.get_object(
            quotation_id,
            item_id,
        )

        serializer = QuotationItemCreateSerializer(
            item,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            QuotationItemSerializer(item).data
        )

    def put(self, request, quotation_id, item_id):
        item = self.get_object(
            quotation_id,
            item_id,
        )

        serializer = QuotationItemCreateSerializer(
            item,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            QuotationItemSerializer(item).data
        )

    def delete(self, request, quotation_id, item_id):
        item = self.get_object(
            quotation_id,
            item_id,
        )

        item.delete()

        return Response(
            {
                "message": "Quotation item deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )


# ============================================================
# QUOTATION APPROVAL
# ============================================================

class QuotationApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        quotation = get_object_or_404(
            Quotation,
            pk=pk,
        )

        # ----------------------------------------------------
        # Only accountants and admins can approve quotations
        # ----------------------------------------------------

        if request.user.role not in ["accountant", "admin"]:
            return Response(
                {
                    "detail": (
                        "Only accountants and admins "
                        "can approve quotations."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # ----------------------------------------------------
        # Prevent approving an already approved quotation
        # ----------------------------------------------------

        if quotation.approved:
            return Response(
                {
                    "detail": "Quotation is already approved."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # Approve quotation
        # ----------------------------------------------------

        quotation.approved = True
        quotation.save(
            update_fields=[
                "approved",
                "updated_at",
            ]
        )

        # ----------------------------------------------------
        # Return complete updated quotation
        # ----------------------------------------------------

        quotation = (
            Quotation.objects
            .select_related(
                "customer",
                "created_by",
            )
            .prefetch_related(
                "items__product"
            )
            .get(pk=quotation.pk)
        )

        return Response(
            {
                "message": "Quotation approved successfully.",
                "quotation": QuotationSerializer(
                    quotation
                ).data,
            },
            status=status.HTTP_200_OK,
        )