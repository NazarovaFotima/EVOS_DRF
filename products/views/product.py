from django.db import models
from django_filters import rest_framework as django_filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from products.filters import ProductFilter
from products.models import Product
from products.permissions import IsStaffOrReadOnly
from products.serializers import ProductSerializer


class CustomPagination(PageNumberPagination):
    page_size = 3


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]  # default =  AllowAny
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = CustomPagination  # /api/products/?page=2

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'min_price',
                openapi.IN_QUERY,
                description="Minimum price (gte)",
                type=openapi.TYPE_NUMBER,
                required=False
            ),
            openapi.Parameter(
                'max_price',
                openapi.IN_QUERY,
                description="Maximum price (lte)",
                type=openapi.TYPE_NUMBER,
                required=False
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search in title and description",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ]
    )

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'products': serializer.data,
            'related_products': related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):

        # Assuming a related name of "reviews" from Review model to Product model
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({"average_rating": "No reviews yet!"})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating": avg_rating})