from django.db import models
class SaleType(models.IntegerChoices):
    retail = 1, 'Розница'
    wholesale = 2, 'Оптом'
    both = 3, 'Оптом и розница'