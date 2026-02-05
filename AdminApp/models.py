from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        db_table = "Category"

    def __str__(self):
        return self.category_name

class Electronics(models.Model):
    item_name = models.CharField(max_length=200)
    price = models.FloatField(default=30)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images",default='abc.jpg')
    image1 = models.ImageField(upload_to="images",default='abc.jpg')
    image2 = models.ImageField(upload_to="images",default='abc.jpg')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    details = models.CharField(max_length=500,default='null')

    class Meta:
        db_table = "Electronics"

class Payment(models.Model):
    card_no = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    expiry = models.CharField(max_length=7)
    balance = models.FloatField(default=2000000)

    class Meta:
        db_table = "Payment"
