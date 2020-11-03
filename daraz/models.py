from django.db import models
class people(models.Model):
    Id = models.IntegerField(primary_key= True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=1000)
    email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    Address = models.CharField(max_length=1000)
    zone = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000)
    method = models.CharField(max_length=100)

    class Meta:
        db_table = "PEOPLE"

# Create your models here.
