from random import randint
from categories.models import Category  

def create_categories_with_sub_categories():
    """
    Создаёт 25 категорий и подкатегорий с вложенной структурой.
    """
    # Удаляем существующие данные для чистоты эксперимента
    Category.objects.all().delete()

    # Список для хранения всех категорий
    categories = []

    # Создаём 5 главных категорий
    for i in range(5):
        category = Category.objects.create(
            name=f"Категория {i + 1}",
            description=f"Описание категории {i + 1}"
        )
        categories.append(category)

    # Создаём подкатегории для каждой главной категории
    for parent in categories:
        for j in range(3):  # По 3 подкатегории для каждой категории
            subcategory = Category.objects.create(
                name=f"Подкатегория {parent.name}.{j + 1}",
                parent=parent,
                description=f"Описание подкатегории {parent.name}.{j + 1}"
            )

            # Создаём подкатегории второго уровня
            for k in range(2):  # По 2 подкатегории для каждой подкатегории
                Category.objects.create(
                    name=f"Подкатегория {subcategory.name}.{k + 1}",
                    parent=subcategory,
                    description=f"Описание подкатегории {subcategory.name}.{k + 1}"
                )

    print("Категории и подкатегории успешно созданы!")

# Запускаем функцию
create_categories_with_sub_categories()