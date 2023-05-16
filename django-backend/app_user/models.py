from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import app_user.utils as utils

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CodesManager(models.Model):
    # Activation code
    activation_code = models.CharField(
        max_length=utils.get_activation_code_expiration(), 
        null=True,
        default=None
    )
    activation_code_expiration = models.DateTimeField(
        null=True,
        default=None
    )
    # TODO: user.activation_code_attempts

    # Reset password code
    reset_password_code = models.CharField(
        max_length=utils.get_reset_password_code_expiration(),
        null=True,
        default=None
    )
    reset_password_code_expiration = models.DateTimeField(
        null=True,
        default=None
    )
    # TODO: user.reset_password_code_attempts


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    codemanager = models.ForeignKey(
        to=CodesManager,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
