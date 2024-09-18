from drf_logto.backends import TokenBackend
from rest_framework_simplejwt.settings import api_settings


def test_token_backend():
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
    assert token_backend.jwks_client
