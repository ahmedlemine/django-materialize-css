from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts import urls

urlpatterns = [
    path('', include("posts.urls", namespace="posts")),
    # admin
    path('admin/', admin.site.urls),
    # allauth & accounts
    path('accounts/', include('allauth.urls')),
    path('accounts/', include("accounts.urls", namespace="accounts"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)