from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Product
from .serializers import ProductSerializer


class product_list(APIView):
    def get(self, request):
        cache_key = "product_list"

        if not cache.get(cache_key):
            print("cache miss")
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            cache.set(cache_key, serializer.data, 180)

        response_data = cache.get(cache_key)
        return Response(response_data)
