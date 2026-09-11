from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsAdmin, IsAdminOrFrontDesk


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrFrontDesk()]

        return [IsAuthenticated()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def get_permissions(self):

        if self.request.method == "DELETE":
            return [IsAdmin()]

        if self.request.method in ["PUT", "PATCH"]:
            return [IsAdminOrFrontDesk()]

        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        """
        Don't actually delete the product.
        Deactivate it instead.
        """

        instance.is_active = False
        instance.save(update_fields=["is_active"])