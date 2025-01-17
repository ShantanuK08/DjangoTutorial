from django.urls import path

from . import views

urlpatterns = [
    path("sonu", views.index, name="index"),  # Existing URL
    path("posts", views.create_posts, name="create_posts"),  # Existing URL
    path("posts/id/", views.read_lists_posts, name="read_lists_posts"),  # New URL for specific post
    path("posts/2", views.put_posts_id, name="put_posts_id"),
]