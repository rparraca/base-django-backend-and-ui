import secrets
import string
from django.conf import settings

def generate_code(length):
    characters = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

def generate_activation_code():
    return generate_code(settings.ACTIVATION_CODE_LENGTH), settings.ACTIVATION_CODE_MINS_TO_EXPIRE

def get_activation_code_expiration():
    return settings.ACTIVATION_CODE_MINS_TO_EXPIRE

def generate_reset_password_code():
    return generate_code(settings.RESET_PASSWORD_CODE_LENGTH), settings.RESET_PASSWORD_CODE_MINS_TO_EXPIRE

def get_reset_password_code_expiration():
    return settings.RESET_PASSWORD_CODE_MINS_TO_EXPIRE
