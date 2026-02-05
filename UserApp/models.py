from django.db import models
from AdminApp.models import Electronics
from datetime import datetime,timedelta

# Create your models here.
class UserInfo(models.Model):
    user_name = models.CharField(max_length=20,primary_key=True)
    zip_code = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=10)
    address = models.CharField(max_length=300,default="Vivekanand Nagar Bhadgaon Road, Pachora")
    email = models.EmailField(max_length=15)
    
    class Meta:
        db_table = "UserInfo"


class MyCart(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    electronics = models.ForeignKey(Electronics,on_delete=models.CASCADE)
    qty  = models.IntegerField(default=1)

    class Meta:
        db_table = "MyCart"

class OrderMaster(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    amount = models.FloatField(default=1000)
    details = models.CharField(max_length=3000)
    order_id = models.CharField(max_length=6)
    arrival = models.DateField(default= datetime.now().date() + timedelta(days=3))
    qty = models. CharField(max_length=2)
    orderStatus = models.CharField(max_length=25,default="Preparing for dipatch")


    class Meta:
        db_table = "OrderMaster"


    