from django.contrib import admin
from .models import Category

class SubCategoryInline(admin.TabularInline):  # Или admin.StackedInline для вертикального отображения
    model = Category
    fk_name = 'parent'  # Указываем связь с родителем
    extra = 1  # Количество дополнительных пустых полей для добавления

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'get_subcategories', 'created_at', 'updated_at')  # Добавляем get_subcategories
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('id',)
    inlines = [SubCategoryInline]  

    def get_subcategories(self, obj):
        
        subcategories = obj.subcategories.all()  # Доступ к related_name 'subcategories'
        if subcategories.exists():
            return ", ".join([sub.name for sub in subcategories])
        return "Нет подкатегорий"

    get_subcategories.short_description = "Подкатегории"

admin.site.register(Category, CategoryAdmin)