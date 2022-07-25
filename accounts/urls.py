from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.update_profile, name='profile')
]