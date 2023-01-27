from django.db import models

class SaleType(models.IntegerChoices):
    retail = 1, 'Розница'
    wholesale = 2, 'Оптом'
    both = 3, 'Оптом и розница'


class AgentType(models.IntegerChoices):
    wholesale = 1, 'Оптом'
    score = 2, 'Балл'
