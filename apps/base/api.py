from rest_framework import generics


class GeneralListAPIView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        # obtenemos el modelo con el metodo get_serializer

        # model = self.get_serializer().Meta.model
        # return model.objects.filter(state=True)

        return self.get_serializer().Meta.model.objects.filter(state=True)
