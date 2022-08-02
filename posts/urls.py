from django.urls import path, include
from .views import (
            Index,
            PostDelete,
            create_post,
            PostDetail,
            delete_comment,
            update_post,
            PostDelete,
            delete_post_htmx,
            create_post_form,
            update_post_form,
            search,
            create_comment_form,
            delete_comment,
            htmx_post_list
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
    path('delete_comment/<int:pk>/', delete_comment, name='delete-comment'),
    path('search/', search, name="search"),
    path('htmx_delete/<slug:slug>/', delete_post_htmx, name='htmx-delete'),
    path('htmx_create/', create_post_form, name='htmx-create'),
    path('htmx_post_list/', htmx_post_list, name='htmx-post-list')
    ]