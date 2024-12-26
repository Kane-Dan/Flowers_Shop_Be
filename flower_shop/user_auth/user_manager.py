from django.contrib.auth.models import  BaseUserManager
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, full_name, phone, password=None, **extra_fields):
        if not full_name:
            raise ValueError("full_name is required")
        if not phone:
            raise ValueError("phone is required")
        if not password:
            raise ValueError("password is required")

        phone_validator = RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Номер должен быть '+79999999999' "
        )
        phone_validator(phone)

        user = self.model(full_name=full_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(full_name=full_name, phone=phone, password=password, **extra_fields) 