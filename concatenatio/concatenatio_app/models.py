from django.db import models
from transliterate import translit

class Item(models.Model):
    item_types = (('Бр', 'Брелоки'),
                ('Откр', 'Открытки'),
                ('Ст', 'Стикеры'),
                ('Блк', 'Блокноты'),
                ('Знч', 'Значки'),
                ('Прч', 'Прочее'))
    
    
    def user_directory_path(instance, filename):
        # Транслитит название из модели и меняет символы " и пробела на нижнее подчеркивание.
        title = str(translit(value = instance.item_title, language_code = 'ru', reversed = True)).replace('"', '_').replace(' ', '_')
        id = str(instance.id)
        return f'item/{id}_{title}/{filename}'

    item_title = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_description = models.TextField()
    item_image = models.ImageField(default='none', upload_to=user_directory_path)
    item_image_2 = models.ImageField(default='none', upload_to=user_directory_path)
    item_quantity = models.IntegerField()
    item_type = models.CharField(max_length = 100, choices=item_types) 
    
    def __str__(self):
        return f'{self.item_title}'
