from django.contrib import admin
from .models import ImageUpload
from .models import SoundFile
from .models import User
from .models import Inventory
from .models import Order
from .models import Product
from .models import Products_Inventory
from .models import Disease_Treatment
# Register your models here.


admin.site.register(ImageUpload)
admin.site.register(SoundFile)
admin.site.register(User)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Products_Inventory)
admin.site.register(Disease_Treatment)

