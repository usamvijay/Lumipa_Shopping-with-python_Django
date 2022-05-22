from django.db import models

# Create your models here.

class User_data(models.Model):  
   firstname  =      models.CharField(max_length=30)
   lastname   =      models.CharField(max_length=100, null=True)  
   mobile     =      models.IntegerField() 
   email      =      models.EmailField( null=True)  
   password   =      models.CharField(max_length=200)  
   JoinedAt   =      models.DateField(auto_now=True)


   def __str__(self):
       return self. firstname


class Catagories(models.Model):
    Catagory_name   =   models.CharField(max_length=50)
    createdAt       =   models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return self.Catagory_name

class Sub_Catagory(models.Model):
    CatId            =       models.ForeignKey(Catagories, on_delete=models.CASCADE, default=1)
    Sub_catagory   =   models.CharField(max_length=50)
    createdAt       =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.Sub_catagory


class Products(models.Model):
    cat                   =       models.ForeignKey(Catagories, on_delete=models.CASCADE, default=1)
    Product_name          =       models.CharField(max_length=60)
    Item_image                 =       models.FileField(upload_to = 'media/products/')
    Total_price           =       models.IntegerField()
    descount_price           =       models.IntegerField()
    Qty                   =       models.IntegerField()
    Color                   =       models.CharField( max_length=10, default='Red')
    Description           =       models.CharField(max_length=200)
    Created_At             =      models.DateField(auto_now  = True)


class Add_to_Cart(models.Model):  
   user      =      models.ForeignKey(User_data, on_delete=models.CASCADE)
   Product   =      models.ForeignKey(Products, on_delete=models.CASCADE)
   total_price     = models.CharField( max_length=15, default=1)    
   Qty       =      models.IntegerField()    
   AddedAt   =      models.DateField(auto_now=True)

   def __str__(self):
       return self.total_price

class Order(models.Model):
   user      =      models.ForeignKey(User_data, on_delete=models.CASCADE)
   firstname  =      models.CharField(max_length=30)
   lastname   =      models.CharField(max_length=100, null=True)  
   cumpany_name   =      models.CharField(max_length=100, null=True)  
   address   =      models.CharField(max_length=500)  
   appartment   =      models.CharField(max_length=100, null=True)  
   city   =      models.CharField(max_length=100)  
   state   =      models.CharField(max_length=10)  
   payment   =      models.CharField(max_length=10, null=False , default=1)  
   Zip_code   =      models.IntegerField( )  
   mobile     =      models.IntegerField()
   email      =      models.EmailField( null=True)  
   created_At   =      models.DateField(auto_now=True)
   tracing_number   =      models.CharField(max_length=150, null=True)


   def __str__(self):
       return self.firstname


class Orders_items(models.Model):
   user         =      models.ForeignKey(User_data, on_delete=models.CASCADE)
   product      =      models.ForeignKey(Products, on_delete=models.CASCADE)
   price = models.IntegerField(null=False)
   Quantity = models.IntegerField(null=False)
   tracing_number   =      models.CharField(max_length=150, null=True)
