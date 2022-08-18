from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.update_profile, name='profile'),
    path("u/<str:username>/", views.public_profile, name='public-profile')
]