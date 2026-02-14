from django.db import models


item_types = (('Бр', 'Брелоки'), ('Откр', 'Открытки'), ('Ст', 'Стикеры'), ('Блк', 'Блокноты'), ('Знч', 'Значки'), ('Прч', 'Прочее'))

class Item(models.Model):
    item_title = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_description = models.TextField()
    item_image = models.ImageField()
    item_quantity = models.IntegerField()
    item_types = models.CharField(max_length = 100, choices = item_types)
       
    def __str__(self):
        return f'{self.item_title}'
