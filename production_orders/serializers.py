from rest_framework import serializers

from .models import ProductionOrder


class ProductionOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True,
    )

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    quotation_number = serializers.CharField(
        source="quotation.quotation_number",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = ProductionOrder

        fields = [
            "id",
            "order_number",
            "quotation",
            "quotation_number",
            "customer",
            "customer_name",
            "product",
            "product_name",
            "marketer_name",
            "meter_run",
            "bundles",
            "length",
            "remark",
            "approved",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "order_number",
            "quotation_number",
            "customer",
            "customer_name",
            "approved",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "meter_run": {
                "required": False,
                "allow_null": True,
            },
            "bundles": {
                "required": False,
                "allow_null": True,
            },
            "length": {
                "required": False,
                "allow_null": True,
            },
            "remark": {
                "required": False,
                "allow_null": True,
            },
            "marketer_name": {
                "required": False,
                "allow_blank": True,
            },
        }


class ProductionOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder

        fields = [
            "quotation",
            "customer",
            "product",
            "marketer_name",
            "meter_run",
            "bundles",
            "length",
            "remark",
        ]

        read_only_fields = [
            "quotation",
            "customer",
        ]

        extra_kwargs = {
            "meter_run": {
                "required": False,
                "allow_null": True,
            },
            "bundles": {
                "required": False,
                "allow_null": True,
            },
            "length": {
                "required": False,
                "allow_null": True,
            },
            "remark": {
                "required": False,
                "allow_null": True,
            },
            "marketer_name": {
                "required": False,
                "allow_blank": True,
            },
        }