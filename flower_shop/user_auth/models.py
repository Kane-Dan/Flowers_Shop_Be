from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .user_manager import UserManager
from django.core.validators import RegexValidator


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone in format '+999999999' (9-15 digits)")
        ]
    )
    email = models.EmailField(blank=True, null=True)    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']  

    def __str__(self):
        return self.phone


class Token(models.Model):
    users = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = 'Tokens',
    )
    a_token = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.users}"