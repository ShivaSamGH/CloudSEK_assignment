import uuid

from django.db import models


# Create your models here.

class Calculation(models.Model):
    unique_identifier = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    number1 = models.IntegerField()
    number2 = models.IntegerField()
    answer = models.IntegerField(null=True)

    def get_unique_identifier(self):
        return self.unique_identifier
