import json
from datetime import timedelta

from rest_framework_simplejwt.backends import TokenBackend as _TokenBackend
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenBackendError
from drf_logto.jwt_auth import Token
from typing import Optional, Any, Union, Iterable, Type, Dict
from django.utils.translation import gettext_lazy as _


try:
    from jwt import PyJWKClient, PyJWKClientError

    JWK_CLIENT_AVAILABLE = True
except ImportError:
    JWK_CLIENT_AVAILABLE = False


class TokenBackend(_TokenBackend):
    def __init__(
        self,
        algorithm: str,
        signing_key: Optional[str] = None,
        verifying_key: str = "",
        audience: Union[str, Iterable, None] = None,
        issuer: Optional[str] = None,
        jwk_url: Optional[str] = None,
        leeway: Union[float, int, timedelta, None] = None,
        json_encoder: Optional[Type[json.JSONEncoder]] = None,
    ):
        super().__init__(
            algorithm,
            signing_key,
            verifying_key,
            audience,
            issuer,
            jwk_url,
            leeway,
            json_encoder,
        )

        if JWK_CLIENT_AVAILABLE:
            self.jwks_client = PyJWKClient(jwk_url, headers={"User-Agent": "DjangoRestFramework"}) if jwk_url else None
        else:
            self.jwks_client = None

    def get_verifying_key(self, token: Token) -> Optional[str]:
        if self.algorithm.startswith("HS"):
            return self.signing_key

        if self.jwks_client:
            try:
                return self.jwks_client.get_signing_key_from_jwt(token).key
            except PyJWKClientError as ex:
                raise TokenBackendError(_("Token is invalid or expired")) from ex

        return self.verifying_key


token_backend = TokenBackend(
    api_settings.ALGORITHM,
    api_settings.SIGNING_KEY,
    api_settings.VERIFYING_KEY,
    api_settings.AUDIENCE,
    api_settings.ISSUER,
    api_settings.JWK_URL,
    api_settings.LEEWAY,
    api_settings.JSON_ENCODER,
)
