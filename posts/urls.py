from django.urls import path, include
from .views import (
            Index,
            PostDelete,
            create_post,
            PostDetail,
            update_post,
            PostDelete,
            delete_post_htmx,
            create_post_form,
            update_post_form,
            search,
            create_comment_form
            )

app_name = 'posts'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:slug>/detail/', PostDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', update_post, name='update'),
    path('<slug:slug>/comment/',create_comment_form, name='comment'),
    path('<slug:slug>/htmx_update/', update_post_form, name='htmx-update'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name="delete"),
    path('create/', create_post, name="create"),
    path('search/', search, name="search"),
    path('htmx_delete/<slug:slug>/', delete_post_htmx, name='htmx-delete'),
    path('htmx_create/', create_post_form, name='htmx-create')
    ]