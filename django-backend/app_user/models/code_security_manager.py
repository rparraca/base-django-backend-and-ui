from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import secrets
import string

from app_user.models import AppUser

def generate_code(length):
    characters = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

class CodeSecurityManager(models.Model):
    """
    Manager for security codes. Current uses ('context') are:
    - Activation / Registration 'activation_code'
    - Password reset 'reset_password'
    """
    app_user = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
        related_name='code_security_manager',
    )
    context = models.CharField(
        max_length=100,
        null=False
    )
    code = models.CharField(
        max_length=100,
        null=True,
        default=None
    )
    minutes_to_expire = models.IntegerField(
        null=True,
        default = -1
    )
    attempts = models.IntegerField(
        null=True,
        default=-1
    )
    def __init__(self, app_user, context):
        self.app_user = app_user
        if context is None or context not in ['activation_code', 'reset_password']:
            raise ValidationError(
                "Security code requires a 'context' string ('activation_code', 'reset_password')"
            )
        self.context = context

        if context == 'activation_code':
            self.code = generate_code(settings.ACTIVATION_CODE_LENGTH)
            self.minutes_to_expire = setting.ACTIVATION_CODE_MINS_TO_EXPIRE
            self.attempts = setting.ACTIVATION_CODE_ATTEMPTS
        elif context == 'reset_password':
            self.code = generate_code(settings.RESET_PASSWORD_CODE_LENGTH)
            self.minutes_to_expire = setting.RESET_PASSWORD_CODE_MINS_TO_EXPIRE
            self.attempts = setting.RESET_PASSWORD_CODE_ATTEMPTS

        # Validate that object has been created properly
        if self.code is None:
            raise ValidationError(f"Code failed to load for context '{context}'")
        if self.minutes_to_expire is None:
            raise ValidationError(f"Minutes to expire to load for context '{context}'")
        if self.attempts is None:
            raise ValidationError(f"Attempts number failed to load for context '{context}'")

    def get_code(self):
        if self.attempts < 1:
            raise ValidationError(
                f"No more attempts allowed for context '{self.context}'"
            )
        self.attempts -= 1
        return self.code

