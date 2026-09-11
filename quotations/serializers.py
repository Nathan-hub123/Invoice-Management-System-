from rest_framework import serializers

from .models import Quotation, QuotationItem
from customers.models import Customer
from products.models import Product


class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "customer_type",
            "name",
            "company_name",
            "email",
            "phone",
            "address",
        ]


class QuotationItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = QuotationItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "description",
            "total",
        ]

    def get_total(self, obj):
        return float(obj.quantity * obj.unit_price)


class QuotationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    quotation_items = QuotationItemSerializer(
        source="items",
        many=True,
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = Quotation
        fields = [
            "id",
            "quotation_number",
            "customer",
            "quotation_date",
            "quotation_items",
            "discount",
            "subtotal",
            "total",
            "notes",
            "approved",
            "created_at",
            "created_by",
            "created_by_name",
            "updated_at",
        ]

        read_only_fields = [
            "quotation_number",
            "quotation_date",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_name",
            "subtotal",
            "total",
            "quotation_items",
        ]

    def get_subtotal(self, obj):
        return float(
            sum(
                item.quantity * item.unit_price
                for item in obj.items.all()
            )
        )

    def get_total(self, obj):
        subtotal = sum(
            item.quantity * item.unit_price
            for item in obj.items.all()
        )

        discount = getattr(obj, "discount", 0) or 0

        return float(subtotal - discount)


class QuotationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = [
            "customer",
            "discount",
            "notes",
        ]


class QuotationItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = [
            "product",
            "quantity",
            "unit_price",
            "description",
        ]

    def validate_product(self, product):
        if not product.is_active:
            raise serializers.ValidationError(
                "This product is inactive and cannot be added to a quotation."
            )

        return product