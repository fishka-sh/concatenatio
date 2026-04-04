from django.db import models
from transliterate import translit

class Item(models.Model):
    item_types = (('trinket', 'Брелоки'),
                ('postcards', 'Открытки'),
                ('stickers', 'Стикеры'),
                ('notebooks', 'Блокноты'),
                ('icons', 'Значки'),
                ('sets', 'Наборы'),
                ('other', 'Прочее'))
    
    
    def user_directory_path(instance, filename):
        # Транслитит название из модели и меняет символы " и пробела на нижнее подчеркивание.
        title = str(translit(value = instance.item_title, language_code = 'ru', reversed = True)).replace('"', '_').replace(' ', '_')
        id = str(instance.id)
        filename = '1.jpg'
        return f'item/{id}_{title}/{filename}'
    
    def user_directory_path2(instance, filename):
        # Транслитит название из модели и меняет символы " и пробела на нижнее подчеркивание.
        title = str(translit(value = instance.item_title, language_code = 'ru', reversed = True)).replace('"', '_').replace(' ', '_')
        id = str(instance.id)
        filename = '2.jpg'
        return f'item/{id}_{title}/{filename}'

    item_title = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_description = models.TextField()
    item_image = models.ImageField(default='none', upload_to=user_directory_path)
    item_image_2 = models.ImageField(default='none', upload_to=user_directory_path2)
    item_quantity = models.IntegerField()
    item_type = models.CharField(max_length = 100, choices=item_types) 
    
    def __str__(self):
        return f'{self.item_title}'
