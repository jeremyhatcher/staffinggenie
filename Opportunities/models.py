# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    is_unloader = models.BooleanField(default=False)
    is_loader = models.BooleanField(default=False)
    is_pallet_picker = models.BooleanField(default=False)
    is_reserve_picker = models.BooleanField(default=False)
    is_slotter = models.BooleanField(default=False)
    is_yard_driver = models.BooleanField(default=False)
    is_desk_clerk = models.BooleanField(default=False)
    is_QA = models.BooleanField(default=False)
    is_office_admin = models.BooleanField(default=False)
    is_AP = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
