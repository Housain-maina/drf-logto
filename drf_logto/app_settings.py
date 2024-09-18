from typing import Any, Dict

from django.conf import settings
from rest_framework.settings import APISettings as _APISettings


USER_SETTINGS = getattr(settings, "DRF_LOGTO", None)

DEFAULTS = {
    "LOGTO_WEBHOOK_HEADER_KEY": None,
    "LOGTO_WEBHOOK_HEADER_VALUE": None,
    "LOGTO_SIGNUP_IDENTIFIER": "email",
}


class LogtoAPISettings(_APISettings):  # pragma: no cover
    def __check_user_settings(self, user_settings: Dict[str, Any]) -> Dict[str, Any]:

        if user_settings.LOGTO_SIGNUP_IDENTIFIER not in ["username", "email", "phone"]:
            raise RuntimeError(
                "The LOGTO_SIGNUP_IDENTIFIER setting must be one of username, email, or phone."
            )

        if user_settings.LOGTO_WEBHOOK_HEADER_KEY is None:
            raise RuntimeError("The LOGTO_WEBHOOK_HEADER_KEY setting must be set.")

        if user_settings.LOGTO_WEBHOOK_HEADER_VALUE is None:
            raise RuntimeError("The LOGTO_WEBHOOK_HEADER_VALUE setting must be set.")

        return user_settings


logto_api_settings = LogtoAPISettings(USER_SETTINGS, DEFAULTS)
