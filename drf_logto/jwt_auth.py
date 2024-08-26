from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token as _Token

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils.translation import gettext_lazy as _
from typing import TYPE_CHECKING
from django.utils.module_loading import import_string
from rest_framework_simplejwt.settings import api_settings

if TYPE_CHECKING:
    from drf_logto.backends import TokenBackend


class Token(_Token):
    @property
    def token_backend(self) -> "TokenBackend":
        if self._token_backend is None:
            self._token_backend = import_string("drf_logto.backends.token_backend")
        return self._token_backend


class AccessToken(Token):
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME


class JWTCookieAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []

        try:
            return AccessToken(raw_token)
        except TokenError as e:
            messages.append(
                {
                    "token_class": AccessToken.__name__,
                    "token_type": AccessToken.token_type,
                    "message": e.args[0],
                }
            )

        raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            return None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
