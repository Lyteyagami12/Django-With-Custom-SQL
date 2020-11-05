from django.db import models


class people(models.Model):
    Id = models.IntegerField(primary_key=True)
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
#
#     class Meta:
#         db_table = "PEOPLE"
# class order(models.Model):
#     ordeid = models.IntegerField(primary_key=True, unique=True)
#     customerid = models.IntegerField()
#     orderdate = models.DateField()
#     amount = models.IntegerField()
#     quantity = models.IntegerField()
#     status = models.CharField(max_length=200)
#     items = models.CharField(max_length=2000)
#
#     class Meta:
#         db_table = "ORDERS"
#
#
# class Catagories(models.Model):
#     cat_id = models.IntegerField()
#     cat_name = models.CharField(max_length=200)
#     quantity = models.IntegerField()
#     class Meta:
#         db_table = "CATAGORIES"
# class Products(models.Model):
#     id = models.IntegerField()
#     shopid = models.IntegerField()
#     description = models.CharField(max_length=1000)
#     catid = models.IntegerField(primary_key=True, unique=True)
#     customerid = models.IntegerField()
#     price = models.IntegerField()
#     quantity = models.IntegerField()
#     status = models.CharField(max_length=200)
#     name = models.CharField(max_length=200)
#     product_photo = models.CharField(max_length=2000)
#     class Meta:
#         db_table = "PRODUCTS"
#

# Create your models here.
