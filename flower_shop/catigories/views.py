from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category
from .serializers import CategorySerializer
class CategotyViewSet(ViewSet):
    
    def list(self, request):
        root_categories = Category.objects.filter(parent=None)  
        serializer = CategorySerializer(root_categories, many=True)
        return Response({"categories": serializer.data})
         


