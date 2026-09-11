from django.db import models


class Customer(models.Model):
    CUSTOMER_TYPES = (
        ("individual", "Individual"),
        ("business", "Business"),
    )

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPES,
        default="individual",
    )

    name = models.CharField(max_length=255)

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True, 
        null=True,
    )


    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.company_name or self.name