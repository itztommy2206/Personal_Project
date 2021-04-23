from django.db import models
from time import gmtime, strftime
import re
from datetime import datetime
# Create your models here.
class UserManager (models.Manager):
    def register_validator(self, reqData):
        errors = {}
        if len(reqData['first_name']) < 3:
            errors['first_name'] = "Name must be atleast 3 characters"
        if len(reqData['last_name']) < 2:
            errors['last_name'] = "last name must be atlease 2 characters"
        if len(reqData['password']) < 8:
            errors['password'] = "Password needs to be atleast 8 characters long"
        if reqData['password'] != reqData['passwordcf']:
            errors['match'] = 'password does not match'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqData['email']):
            errors['email'] = "invalid email address!"
        email_check = User.objects.filter(email = reqData['email'])
        if len(email_check) >= 1:
            errors['dups'] = "This Email is already taken"
        user_birthdate = datetime.strptime(reqData['birthday'], "%Y-%m-%d")
        if datetime.now() < user_birthdate:
            errors['date'] = "Birthday must be before today"
        age = (datetime.now() - user_birthdate).days/365
        if age < 13:
            errors['tooYoung'] = "Must be 13 years of age"
        return errors
    
    

class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    birthday = models.DateField()
    email = models.CharField(max_length = 255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Item(models.Model):
    item_name = models.TextField()
    price = models.DecimalField(decimal_places = 2, max_digits = 5)
    users_who_bought_item = models.ManyToManyField(User, related_name = "items")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Champion(models.Model):
    name = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "champions"