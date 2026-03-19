from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name = 'index'),
    path('login' , views.login , name = 'login'),
    path('edit' , views.edit , name = 'edit'),
    path('soil' , views.soil , name = 'soil'),
    path('sound' , views.sound , name = 'sound'),
    path('inventory' , views.inventory , name = 'inventory'),
    path('my_orders' , views.my_orders , name = 'my_orders'),
    path('orders' , views.orders, name = 'orders'),
    path('accept/<int:id>' , views.accept_order, name = 'accept'),
    path('orders_accepted' , views.orders_accepted, name = 'orders_accepted'),
    path('image' , views.image , name = 'image'),
    path('order' , views.order , name = 'order'),
    path('segment' , views.segment , name = 'segment'),
    path('register' , views.register , name = 'register'),
    path('logout' , views.logout , name = 'logout'),
    path('index_type_admin', views.index_type_admin, name='index_type_admin'),
    path('index_type_user', views.index_type_user, name='index_type_user'),
    path('makeOrder/<int:proID>', views.makeOrder, name='makeOrder'),
    path('cancelOrder/<int:orderID>', views.cancelOrder, name='cancelOrder'),
]

