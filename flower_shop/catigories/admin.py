from django.contrib import admin
from .models import Category

class SubCategoryInline(admin.TabularInline):  # Или admin.StackedInline для вертикального отображения
    model = Category
    fk_name = 'parent'  # Указываем связь с родителем
    extra = 1  # Количество дополнительных пустых полей для добавления

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'get_sub_categories', 'created_at', 'updated_at')  
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('id',)
    inlines = [SubCategoryInline]  

    def get_sub_categories(self, obj):
        
        sub_categories = obj.sub_categories.all()  
        if sub_categories.exists():
            return ", ".join([sub.name for sub in sub_categories])
        return "Нет подкатегорий"

    get_sub_categories.short_description = "Подкатегории"

admin.site.register(Category, CategoryAdmin)