from django.urls import path

from .views import WebhookView

urlpatterns = [
    path("post-register-webhook/", WebhookView.as_view(), name="post-register-webhook"),
]
