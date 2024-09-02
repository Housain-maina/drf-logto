# Drf-Logto

Logto authentication integration for Django Rest Framework.

## Installation & Usage

    pip install drf-logto

Add "drf_logto" to INSTALLED_APPS list:

```py
INSTALLED_APPS = [

    "drf_logto",
]
```

Include "drf_logto.urls" in your project's urls.py:

```py
from django.urls import path, include

urlpatterns = [

    path("auth/", include("drf_logto.urls")),
]
```

Set AUTH_USER_MODEL in settings.py to "drf_logto.LogtoUser"

```py
AUTH_USER_MODEL = "drf_logto.LogtoUser"
```

### Settings

```py
DRF_LOGTO = {
    "WEBHOOK_HEADER_KEY": "Example-Webhook-Token",
    "WEBHOOK_HEADER_VALUE": "sdfksdjfksjdfsdkfjsdkfjksdjf",
    "SIGNUP_IDENTIFIER": "email",
}
```
