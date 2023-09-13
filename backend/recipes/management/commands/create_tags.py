from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    """Загрузка данных в БД"""
    def handle(self, *args, **options):
        try:
            create_tags()
            print('теги созданы')
        except Exception as er:
            print(er)


def create_tags():
    Tag.objects.bulk_create([
        Tag(name='Завтрак', color='#E26C2D', slug='breakfast'),
        Tag(name='Обед', color='#88e990', slug='lunch'),
        Tag(name='Ужин', color='#494ce8', slug='dinner')]
    )
