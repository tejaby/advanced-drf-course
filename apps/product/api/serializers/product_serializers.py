from rest_framework import serializers

from apps.product.models import Product

from apps.product.api.serializers.general_serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    ''' Formas de Serializar Relaciones en Modelos '''
    # Nested Serializers:  definir otro serializador para el modelo relacionado
    # category = CategorySerializer()

    # StringRelatedField: definir como cadena en lugar de un objeto
    # category = serializers.StringRelatedField()

    # to_representation

    class Meta:
        model = Product
        exclude = ['state', 'created_at', 'deleted_at']

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'producto': instance.product,
            'descripcion': instance.description,
            'categoria': instance.category.category,
            'precio': instance.price,
            'imagen': instance.image.url if instance.image else None,

        }

        # if instance.image:
        #     data['imagen'] = instance.image.url
        # else:
        #     data['imagen'] = None

        return data
