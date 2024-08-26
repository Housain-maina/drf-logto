from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from drf_logto.settings import logto_api_settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, sub, username, email, phone, password, **extra_fields):
        """
        Create and save a user with the given sub, username, email, and password.
        """

        if not sub:
            raise ValueError("The given sub must be set")

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(
            sub=sub, username=username, email=email, phone=phone, **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, sub, username=None, email=None, phone=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(sub, username, email, phone, password, **extra_fields)

    def create_superuser(
        self, sub, username=None, email=None, phone=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(sub, username, email, phone, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class LogtoUser(AbstractUser):
    logto_identifier = logto_api_settings.LOGTO_SIGNUP_IDENTIFIER

    sub = models.CharField(max_length=150, blank=False, null=False, unique=True)

    username = models.CharField(
        max_length=150,
        unique=logto_identifier == "username",
        blank=logto_identifier != "username",
        null=logto_identifier != "username",
    )
    phone = models.CharField(
        max_length=150,
        blank=logto_identifier != "phone",
        unique=logto_identifier == "phone",
        null=logto_identifier != "phone",
    )
    email = models.EmailField(
        unique=logto_identifier == "email",
        blank=logto_identifier != "email",
        null=logto_identifier != "email",
    )

    USERNAME_FIELD = logto_api_settings.LOGTO_SIGNUP_IDENTIFIER
    REQUIRED_FIELDS = ["sub"]

    objects = UserManager()

    def __str__(self):
        return self.email
