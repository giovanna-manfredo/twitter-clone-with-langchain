from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
    BaseUserManager

)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password=None, **extra_fields):
        if date_of_birth and not self.is_adult(date_of_birth):
            raise ValidationError("User must be at least 13 years old.")
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email) 
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)  
        return user

    def create_superuser(self, username, email, date_of_birth, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  

        return self.create_user(username, email, date_of_birth, password, **extra_fields)

    def is_adult(self, date_of_birth):
        today = date.today()
        age = today.year - date_of_birth.year
        if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day):
            age -= 1
        return age >= 13

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=False, blank=False)
    # cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True) # future feature
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True) # future feature
    location = models.CharField(max_length=255, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [ "email", "date_of_birth"]

    class Meta:
        db_table = "users" 
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    