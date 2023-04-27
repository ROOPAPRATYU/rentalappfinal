from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
# Create your models here.

class CustomUser(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            **extra_fields
        )
        if password is not None:
           user.set_password(password)
        user.save()
        return user
    def create_owner(self,email, password, **extra_fields):
        extra_fields.setdefault('is_owner', True)
        extra_fields.setdefault('is_active', True)

        
        if extra_fields.get('is_owner')is not True:
            raise ValueError("is_owner need to be True for Owner.")
        user = self.create_user(email=email, password=password, **extra_fields)
        return user
    
    def create_tenet(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_tenet', True)
        if extra_fields.get('is_tenet')is not True:
            raise ValueError("is_owner need to be True for Owner.")
        user = self.create_user(email=email, password=password, **extra_fields)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff')is not True:
            raise ValueError("is_staff need to be True for Superuser.")
        if extra_fields.get('is_superuser')is not True:
            raise ValueError("is_superuser need to be True for Superuser.")

        user = self.create_user(email=email, password=password, **extra_fields)
        return user
 

class User(AbstractBaseUser, PermissionsMixin):
    username=None
    is_owner = models.BooleanField(default=True)
    is_tenet = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, unique=True)
    # username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUser()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email





