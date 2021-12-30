from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models

from django.utils.translation import gettext_lazy
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(gettext_lazy("Every user should have an Email"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_verified", True)
        other_fields.setdefault("is_approved", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be staff")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be staff")

        return self.create_user(email, username, first_name, last_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    is_active: Whether the account is active or not. An account can be deactivated by the staff from this field
    is_verified: User verified his email (or phone number)
    is_approved: User identification application was approved
    """
    # For a mobile app, the phone number should be used instead of the email
    email = models.EmailField(gettext_lazy("email address"), unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access ": str(refresh.access_token)
        }
