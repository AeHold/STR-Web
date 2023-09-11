from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class Type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    description = models.TextField(max_length=1000)
    price = models.FloatField()
    genre = models.ManyToManyField(Genre)
    type = models.ForeignKey(Type, related_name="products", on_delete=models.CASCADE)
    cover = models.ImageField()
    amount = models.IntegerField()

    def __str__(self):
        return self.name+"/"+self.author


class Post(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return str(self.user)



class Order(models.Model):
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    appartments = models.CharField(max_length=100, blank=True)
    client = models.ForeignKey(Profile,related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateField()
    deliver_date = models.DateField()
    is_send = models.BooleanField(default=False)
    is_recieved = models.BooleanField(default=False)




