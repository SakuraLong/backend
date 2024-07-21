"""
图片处理相关接口
"""

from response import Response

import os
import json
import shutil

from mybackend.settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "jfif", "webp"]

@csrf_exempt
@require_POST
def upload_images(request):
    """
    上传图片
    
    need:
    ```json
    {
        "images": [],
        "id_en": ""
    }
    ```
    get(data):
    ```json
    {
        "urls": []
    }
    ```
    """
    files = request.FILES.getlist("images")
    id_en = request.POST.get("id_en", None)
    print(request.FILES, files)
    if id_en == None:
        return Response.missing_required_params(params=["id_en"])
    if len(files) == 0:
        return Response.bad_request(message="未提供图片")
    urls = []
    for file in files:
        fs = FileSystemStorage()
        file_extension = file.name.split(".")[-1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            continue
        file_path = os.path.join("blog", id_en, file.name)
        filename = fs.save(file_path, file)
        file_url = fs.url(filename)
        urls.append(file_url)
    return Response.success({
        "urls": urls
    })

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_image(request):
    """
    删除图片

    need:
    ```json
    {
        "name": "",
        "id_en": ""
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    name = body.get("name", None)
    id_en = body.get("id_en", None)
    params = Response.create_missing_required_params(
        [name, id_en],
        ["name", "id_en"]
    )
    if params != True:
        return Response.missing_required_params(None, params)
    fs = FileSystemStorage()
    file_path = os.path.join("blog", id_en, name)
    if fs.exists(file_path):
        fs.delete(file_path)
        return Response.success(message="删除成功")
    else:
        # 文件不存在
        return Response.http404(message="图片不存在")

@csrf_exempt
@require_http_methods(["PUT"])
def rename_image(request):
    """
    重命名图片

    need:
    ```json
    {
        "old": "",
        "new": "",
        "id_en": ""
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    old = body.get("old", None)
    new = body.get("new", None)
    id_en = body.get("id_en", None)
    params = Response.create_missing_required_params(
        [old, new, id_en],
        ["old", "new", "id_en"]
    )
    if params != True:
        return Response.missing_required_params(None, params)
    fs = FileSystemStorage()
    old_path = os.path.join(MEDIA_ROOT, "blog", id_en, old)
    new_path = os.path.join(MEDIA_ROOT, "blog", id_en, new)
    if fs.exists(old_path):
        try:
            shutil.move(old_path, new_path)
            return Response.success(message="重命名成功")
        except Exception as e:
            return Response.error(message=str(e))
    else:
        # 文件不存在
        return Response.http404(message="图片不存在")

@csrf_exempt
@require_GET
def get_image_urls(request):
    """
    根据id_en获取其所有的图片的url

    need:
    ```json
    {
        "id_en": ""
    }
    ```
    get(data):
    ```json
    {
        urls: []
    }
    ```
    """
    id_en = request.GET.get("id_en", None)
    if id_en == None:
        return Response.missing_required_params(params=["id_en"])
    media_dir = os.path.join(MEDIA_ROOT, "blog", id_en)
    use_dir = os.path.join("blog", id_en)
    fs = FileSystemStorage()
    urls = []
    if os.path.exists(media_dir):
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
                    path = os.path.join(use_dir, file)
                    file_url = fs.url(path)
                    image_info = [file_url, os.path.basename(file), ext[1:].lower()]  # 去掉点的扩展名
                    urls.append(image_info)
    return Response.success({
        "urls": urls
    })