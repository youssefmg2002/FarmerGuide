from django.db import models

# Create your models here.


class ImageUpload(models.Model):
    image = models.ImageField(upload_to = 'photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SoundFile(models.Model):
    sound = models.FileField(upload_to='sounds/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
    govern = [
        ('Cairo', 'Cairo'),
        ('Giza', 'Giza'),
        ('Alexandria', 'Alexandria'),
        ('Aswan', 'Aswan'),
        ('Asyut', 'Asyut'),
        ('Beheira', 'Beheira'),
        ('Beni Suef', 'Beni Suef'),
        ('Dakahlia', 'Dakahlia'),
        ('Damietta', 'Damietta'),
        ('Faiyum', 'Faiyum'),
        ('Gharbia', 'Gharbia'),
        ('Ismailia', 'Ismailia'),
        ('Kafr El Sheikh', 'Kafr El Sheikh'),
        ('Luxor', 'Luxor'),
        ('Matruh', 'Matruh'),
        ('Minya', 'Minya'),
        ('Monufia', 'Monufia'),
        ('New Valley', 'New Valley'),
        ('North Sinai', 'North Sinai'),
        ('Port Said', 'Port Said'),
        ('Qalyubia', 'Qalyubia'),
        ('Qena', 'Qena'),
        ('Red Sea', 'Red Sea'),
        ('Sharqia', 'Sharqia'),
        ('Sohag', 'Sohag'),
        ('South Sinai', 'South Sinai'),
        ('Suez', 'Suez')
    ]
    inventoryID = models.CharField(max_length=50, primary_key=True)
    governorate = models.CharField(max_length=50, choices=govern , null=True)
    def __str__(self):
        return self.inventoryID

class User(models.Model):
    govern = [
        ('Cairo', 'Cairo'),
        ('Giza', 'Giza'),
        ('Alexandria', 'Alexandria'),
        ('Aswan', 'Aswan'),
        ('Asyut', 'Asyut'),
        ('Beheira', 'Beheira'),
        ('Beni Suef', 'Beni Suef'),
        ('Dakahlia', 'Dakahlia'),
        ('Damietta', 'Damietta'),
        ('Faiyum', 'Faiyum'),
        ('Gharbia', 'Gharbia'),
        ('Ismailia', 'Ismailia'),
        ('Kafr El Sheikh', 'Kafr El Sheikh'),
        ('Luxor', 'Luxor'),
        ('Matruh', 'Matruh'),
        ('Minya', 'Minya'),
        ('Monufia', 'Monufia'),
        ('New Valley', 'New Valley'),
        ('North Sinai', 'North Sinai'),
        ('Port Said', 'Port Said'),
        ('Qalyubia', 'Qalyubia'),
        ('Qena', 'Qena'),
        ('Red Sea', 'Red Sea'),
        ('Sharqia', 'Sharqia'),
        ('Sohag', 'Sohag'),
        ('South Sinai', 'South Sinai'),
        ('Suez', 'Suez')
    ]
    name = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    govername = models.CharField(max_length=50 , choices=govern , null=True)
    admin = models.BooleanField(default=False)
    inventoryID = models.ForeignKey(Inventory , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    productid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200 , null=True)
    price = models.DecimalField(max_digits=6 , decimal_places=2, null=True , default=0.00)
    def __str__(self):
        return self.name
    

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100, null=True)
    userGovernorate = models.CharField(max_length=50, null=True)

    productid = models.IntegerField(default=0,null=True)
    productName = models.CharField(max_length=200, null=True)
    productprice = models.DecimalField(max_digits=6 , decimal_places=2, null=True)
    productNum = models.IntegerField(default=0, null=True)
    totalPrice = models.DecimalField(max_digits=6 , decimal_places=2, null=True)
    accepted = models.BooleanField(default=False, null=True)

    adminName = models.CharField(max_length=100, null=True , default="Admin Name")
    adminAddress = models.CharField(max_length=200, null=True , default="Admin Address") 
    def __str__(self):
        ID = str(self.id)
        return ID


class Products_Inventory(models.Model):
    inventoryID = models.ForeignKey(Inventory , on_delete=models.CASCADE , null=True)
    productid = models.IntegerField(default=0,null=True)
    productName = models.CharField(max_length=200, null=True)
    productPrice = models.DecimalField(max_digits=6 , decimal_places=2, null=True)
    productnum = models.IntegerField(default=0, null=True)
    
    def __str__(self):
        invID = str(self.inventoryID) + " - " + self.productName
        return invID


class Disease_Treatment(models.Model):
    diseaseName = models.CharField(max_length=50, primary_key=True)
    organic = models.TextField(max_length=1000)
    chemical = models.TextField(max_length=1000)
    productid = models.IntegerField(default=0,null=True)
    productName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.diseaseName

