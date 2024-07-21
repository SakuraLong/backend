from django.urls import path

from .views import get_posts
from .views import get_post
from .views import save
from .views import publish_post
from .views import create_draft
from .views import update_post
from .views import change_visibility
from .views import update_categories

urlpatterns = [
    path("blogmanage/posts/get", get_posts),
    path("blogmanage/post/get", get_post),
    path("blogmanage/post/save", save),
    path("blogmanage/post/publish", publish_post),
    path("blogmanage/post/create", create_draft),
    path("blogmanage/post/update", update_post),
    path("blogmanage/post/visibility", change_visibility),
    path("blogmanage/categories/update", update_categories),
]