from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class Form(models.Model):
    name = models.TextField(max_length=20,db_index=True)

    def __str__(self):
        return self.name

class Hall(models.Model):
    name = models.CharField(max_length=50)
    floor = models.IntegerField()
    square = models.FloatField()

    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Exponate(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    author = models.TextField(max_length=50)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    photo = models.ImageField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='exponates')
    receipt_date = models.DateField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    phone_number = PhoneNumberField()
    exponates = models.ManyToManyField(Exponate, blank=True)

    def __str__(self):
        return str(self.user)

class Exhibition(models.Model):
    hall = models.ManyToManyField(Hall)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    def __str__(self):
        return self.name

class Excursion(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    date = models.DateTimeField()
    guide = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.exhibition) + '/' + str(self.date) + '/' + str(self.guide)









