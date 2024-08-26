from secrets import compare_digest

from django.db.transaction import atomic
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model
from drf_logto.settings import logto_api_settings
from rest_framework.views import APIView


User = get_user_model()


class WebhookView(APIView):
    def post(self, request):
        # Extract webhook data from the request
        data = request.data
        given_token = request.headers.get(logto_api_settings.LOGTO_WEBHOOK_HEADER_KEY)
        if not compare_digest(
            given_token, logto_api_settings.LOGTO_WEBHOOK_HEADER_VALUE
        ):
            return HttpResponseForbidden(
                f"Incorrect token in {logto_api_settings.LOGTO_WEBHOOK_HEADER_KEY} header.",
                content_type="text/plain",
            )
        process_webhook_payload(data)
        return HttpResponse("Message received okay.", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    if payload["event"] == "PostRegister":
        if logto_api_settings.LOGTO_SIGNUP_IDENTIFIER == "email":
            user = User.objects.create(
                sub=payload["user"]["userId"], email=payload["user"]["primaryEmail"]
            )
            user.save()
        elif logto_api_settings.LOGTO_SIGNUP_IDENTIFIER == "username":
            user = User.objects.create(
                sub=payload["user"]["userId"], username=payload["user"]["username"]
            )
            user.save()
        elif logto_api_settings.LOGTO_SIGNUP_IDENTIFIER == "phone":
            user = User.objects.create(
                sub=payload["user"]["userId"], phone=payload["user"]["primaryPhone"]
            )
            user.save()

    elif payload["event"] == "User.Created":
        if logto_api_settings.LOGTO_SIGNUP_IDENTIFIER == "email":
            user = User.objects.create(
                sub=payload["data"]["id"], email=payload["data"]["primaryEmail"]
            )
            user.save()
        elif logto_api_settings.LOGTO_SIGNUP_IDENTIFIER == "username":
            user = User.objects.create(
                sub=payload["data"]["id"], username=payload["data"]["username"]
            )
            user.save()
        elif logto_api_settings.LOGTO_SIGNUP_IDENTIFIER == "phone":
            user = User.objects.create(
                sub=payload["data"]["id"], phone=payload["data"]["primaryPhone"]
            )
            user.save()

    elif payload["event"] == "User.SuspensionStatus.Updated":
        user = User.objects.get(sub=payload["data"]["id"])
        user.is_active = not payload["data"]["isSuspended"]
        user.save()
