from django.db import models
from django.contrib.auth.models import User
import string
import random

def generate_unique_code():
    length = 8
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k =length))
        if League_Mod.objects.filter(code=code).count() == 0:
            break

    return code

# Create your models here.
class League_Mod(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique = True)
    host = models.CharField(max_length=50)
    Espn_League_Id = models.IntegerField(null=False, unique = True)
    Espn_S2 = models.CharField(max_length=3000)
    Espn_Swid = models.CharField(max_length=300) 
