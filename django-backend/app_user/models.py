from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
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
        return self.create_user(email, password, **extra_fields)
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self.create_user(email, password, **extra_fields)

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'

    #### SECURITY: Codes ####
    #
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
    activation_code_attempts = models.IntegerField(
        default = 3
    )
    def get_activaction_code(self):
        if self.activation_code_attempts < 1:
            raise ValidationError(
                f"No more activation attempts allowed"
            )
        self.activation_code_attempts -= 1
        return self.activation_code
    #
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
    reset_password_code_attempts = models.IntegerField(
        default = 3
    )
    def get_reset_password_code(self):
        if self.reset_password_code_attempts < 1:
            raise ValidationError(
                f"No more reset password attempts allowed"
            )
        self.reset_password_code_attempts -= 1
        return self.reset_password_code
