from django.db import models


class Item(models.Model):
    item_title = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_description = models.TextField()
    item_image = models.ImageField()
    item_quantity = models.IntegerField()
       
    def __str__(self):
        return f'{self.item_title}'