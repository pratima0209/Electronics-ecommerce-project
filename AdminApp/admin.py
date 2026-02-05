from django.contrib import admin
from .models import Electronics,Category,Payment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name')

class ElectronicsAdmin(admin.ModelAdmin):
    list_display = ('id','item_name','price','description','details','image','image1','image2','category')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','card_no','cvv','expiry','balance')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Electronics,ElectronicsAdmin)
admin.site.register(Payment,PaymentAdmin)
