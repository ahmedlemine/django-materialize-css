from django.conf import settings
from django.conf.urls.static import static
# from turtle import update
from django.contrib import admin
from django.urls import path
from posts.views import (
            Index,
            PostDelete,
            create_post,
            PostDetail,
            update_post,
            PostDelete,
            delete_post_htmx,
            create_post_form,
            update_post_form,
            search
            )
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:slug>/detail/', PostDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', update_post, name='update'),
    path('<slug:slug>/htmx_update/', update_post_form, name='htmx-update'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name="delete"),
    path('create/', create_post, name="create"),
    path('search/', search, name="search"),
    path('htmx_delete/<slug:slug>/', delete_post_htmx, name='htmx-delete'),
    path('htmx_create/', create_post_form, name='htmx-create'),
    # admin
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)