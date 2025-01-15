from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']

    def get_sub_categories(self, obj):
        """
        Рекурсивно сериализуем подкатегории.
        """
        children = obj.sub_categories.all()  
        if children.exists():
            return CategorySerializer(children, many=True).data  # Рекурсивный вызов
        return []  # Если подкатегорий нет, возвращаем пустой список