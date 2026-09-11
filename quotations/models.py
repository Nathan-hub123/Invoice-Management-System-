from django.db import models

from customers.models import Customer
from products.models import Product


class Quotation(models.Model):
    quotation_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="quotations",
    )

    quotation_date = models.DateField(
        auto_now_add=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    discount = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=0,
    )

    approved = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    created_by = models.ForeignKey(
    "users.User",
    on_delete=models.PROTECT,
    related_name="created_quotations",
    null=True,
    blank=True,
)

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.quotation_number:
            last_quotation = Quotation.objects.order_by("-id").first()

            if last_quotation:
                last_number = int(
                    last_quotation.quotation_number.split("-")[-1]
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.quotation_number = f"QT-{next_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.quotation_number


class QuotationItem(models.Model):
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="quotation_items",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.product.name}"