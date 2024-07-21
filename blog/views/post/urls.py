from django.urls import path

from .views import get_posts
from .views import get_post
from .views import testset
from .views import testget
from .views import get_categories

urlpatterns = [
    path("blog/posts/get", get_posts),
    path("blog/post/get", get_post),
    path("testset", testset),
    path("testget", testget),
    path("blog/categories/get", get_categories),
]