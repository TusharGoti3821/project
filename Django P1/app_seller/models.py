from django.db import models

# Create your models here.
class seller_user(models.Model):
    fullname=models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)


    def __str__(self):
        return self.fullname
    



# class Product(models.Model):
#     pname=models.CharField(max_length=50)
#     price = models.CharField(max_length=5)
#     description= models.CharField(max_length=250)
#     image = models.FileField(upload_to='pimage/',default="ghughu")
#     seller = models.ForeignKey(seller_user,on_delete=models.CASCADE)


#     def __str__(self):
#         return self.pname
    


class Add_Product(models.Model):
    pname=models.CharField(max_length=50)
    price = models.CharField(max_length=5)
    description= models.CharField(max_length=250)
    image = models.FileField(upload_to='pimage/',default="ghughu")
    seller = models.ForeignKey(seller_user,on_delete=models.CASCADE)


    def __str__(self):
        return self.pname