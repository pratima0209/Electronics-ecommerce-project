from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('Products/<id>/',views.Products),
    path('search',views.search),
    path('getGadjets/<id>',views.getGadjets),
    path('masterLogin',views.masterLogin),
    path('masterSignUp',views.masterSignUp),
    path('SignOut',views.SignOut),
    path('addToCart',views.addToCart),
    path('showCart_Item',views.showCart_Item),
    path('deleteCart_item/<id>',views.deleteCart_item),
    path('makePayment',views.makePayment),
    path('orderDetails',views.orderDetails),
    path('yourAccount',views.yourAccount),
    path('address',views.address),
    path('cancleOrder/<id>',views.cancleOrder),
    path('requestCancelation/<id>',views.requestCancelation),
    path('contactUs',views.contactUs),
    path('login_And_Security',views.login_And_Security),
    path('login',views.login),
    path('Otp',views.Otp),
    path('Resend',views.Resend),
]
