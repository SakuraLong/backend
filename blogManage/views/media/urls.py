from django.urls import path

from .views import upload_images
from .views import delete_image
from .views import rename_image
from .views import get_image_urls

urlpatterns = [
    path("blogmanage/images/upload", upload_images),
    path("blogmanage/images/delete", delete_image),
    path("blogmanage/images/rename", rename_image),
    path("blogmanage/images/get", get_image_urls),
]