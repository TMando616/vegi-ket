from django.db import models
from django.utils.crypto import get_random_string

def create_id():
    return get_random_string(22)

class Item(models.Model):
    id = models.CharField(default=create_id, primary_key=True, max_length=22, editable=False) # create_idの後に（）を付けると都度実行される
    name = models.CharField(default='', max_length=50)
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(default='', blank=True)
    sold_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name