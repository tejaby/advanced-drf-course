from rest_framework import generics

from apps.base.api import GeneralListAPIView

from apps.product.api.serializers.general_serializers import CategorySerializer

from apps.product.models import Category


# class CategoryListAPIView(generics.ListAPIView):
#     serializer_class = CategorySerializer

#     def get_queryset(self):
#         return Category.objects.filter(state=True)
    
class CategoryListAPIView(GeneralListAPIView):
    serializer_class = CategorySerializer
