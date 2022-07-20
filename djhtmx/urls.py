from turtle import update
from django.contrib import admin
from django.urls import path
from posts.views import (
            Index,
            PostDelete,
            create_post,
            PostDetail,
            update_post,
            PostDelete,
            delete_post_htmx
            )
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:slug>/detail/', PostDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', update_post, name='update'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name="delete"),
    path('create/', create_post, name="create"),
    path('htmx_delete/<slug:slug>/', delete_post_htmx, name='htmx-delete'),
    # admin
    path('admin/', admin.site.urls),
]
