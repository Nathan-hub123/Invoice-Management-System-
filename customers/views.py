from django.db.models import Q
from rest_framework import generics

from .models import Customer
from .serializers import CustomerSerializer
from users.permissions import IsAdminOrFrontDesk


class CustomerListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrFrontDesk]

    def get_queryset(self):
        queryset = Customer.objects.all()

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(company_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
            )

        return queryset.order_by("-created_at")


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrFrontDesk]

    def get_queryset(self):
        
        return Customer.objects.all()