from rest_framework import generics

from apps.product.api.serializers.general_serializers import CategorySerializer

from apps.product.models import Category


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(state=True)
