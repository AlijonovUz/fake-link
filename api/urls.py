from django.urls import path

from .views import GenerateURL, GetURL

urlpatterns = [
    path('generate/', GenerateURL.as_view(), name="generate_api"),
    path('<str:code>/', GetURL.as_view())
]