from django.db import models

from customers.models import Customer
from products.models import Product
from quotations.models import Quotation


class ProductionOrder(models.Model):
    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.PROTECT,
        related_name="production_orders",
        null=True,
        blank=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="production_orders",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="production_orders",
    )

    marketer_name = models.CharField(
        max_length=255,
        default="MD's Customer",
        blank=True,
    )

    meter_run = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    bundles = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    length = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    remark = models.TextField(
        blank=True,
        null=True,
    )

    approved = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = ProductionOrder.objects.order_by("-id").first()

            if last_order:
                last_number = int(
                    last_order.order_number.split("-")[-1]
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.order_number = f"PO-{next_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number