"""
帖子管理相关接口
"""

from blog.models import Post
from response import Response
from .utils import PostSerializerForManageAbstract, PostSerializerForManageFull
from .utils import (
    create_update_dict,
    create_publish_dict,
    create_draft_dict,
    create_save_dict
)

import json

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods

@csrf_exempt
@require_POST
def get_posts(request):
    """
    返回全部帖子的信息

    get(data):
    ```json
    {
        "posts": [
            {
                "title": "标题",
                "abstract": "摘要",
                "publication_time": 12121212, // 发布时间s
                "modification_time": 12121212, // 修改时间s
                "word_count": 123, // 字数
                "id": 1,
                "id_en": "aaabbb",
                "tags": ["标签1", "标签2"],
                "categories": ["分类1", "分类2"],
                "categories_introduction": false, // 帖子是否是分类的介绍
            }
        ]
    }
    """
    posts = Post.objects.exclude(id=1)
    res = []
    for post in posts:
        res.append(PostSerializerForManageAbstract(post).data)
    return Response.success(res)

@csrf_exempt
@require_POST
def get_post(request):
    """
    根据id返回帖子的具体信息

    need:
    ```json
    {
        "id": 1
    }
    ```
    get(data):
    ```json
    {
        "post": {
            "title": "标题",
            "abstract": "摘要",
            "body": "帖子主体",
            "publication_time": 12121212, // 发布时间s
            "modification_time": 12121212, // 修改时间s
            "word_count": 123, // 字数
            "id": 1,
            "id_en": "aaabbb",
            "tags": ["标签1", "标签2"],
            "categories": ["分类1", "分类2"],
            "categories_introduction": false, // 帖子是否是分类的介绍
            "visible": true,
        }
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    id = body.get("id", None)
    if id == None:
        return Response.missing_required_params(None, ["id"])
    try:
        post = Post.objects.exclude(id=1).get(id=id)
    except Post.DoesNotExist:
        return Response.http404(None, "帖子不存在")
    
    return Response.success({
        "post": PostSerializerForManageFull(post).data
    })

@csrf_exempt
@require_POST
def create_draft(request):
    """
    新建草稿

    need:
    ```json
    {
        "post": {
            "id_en": "aaabbb",
            "title": "标题",
            "title_pinyin": "saac",
            "author": "acsa",
        }
    }
    ```
    get(data):
    ```json
    {
        "id": 1
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except Exception as e:
        return Response.bad_request(message=f"数据结构异常:{str(e)}")
    post = body.get("post", {})
    res = create_draft_dict(post)
    if type(res) is list:
        return Response.missing_required_params(None, res, pre="缺少草稿信息参数:")
    res["publication_time"] = timezone.now()
    res["modification_time"] = timezone.now()

    post = Post(**res)
    try:
        post.save()
    except Exception as e:
        return Response.error(message=f"{str(e)}")
    
    return Response.success({
        "id": post.id
    }, "新建草稿成功")

@csrf_exempt
@require_POST
def save(request):
    """
    保存

    need:
    ```json
    {
        "id": 0,
        "post": {
            "title": "",
            "title_pinyin": "",
            "author": "",
            "abstract": "",
            "body": "",
            "word_count": 0,
            "tags": [],
            "categories": [],
            "categories_introduction": False,
        }
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except Exception as e:
        return Response.bad_request(message=f"数据结构异常:{str(e)}")
    id = body.get("id", None)
    post = body.get("post", None)
    params = Response.create_missing_required_params(
        [id, post],
        ["id", "post"]
    )
    if params != True:
        return Response.missing_required_params(None, params)
    res = create_save_dict(post)
    res["modification_time"] = timezone.now()
    try:
        p = Post.objects.filter(id=id)
        p.update(**res)
    except Post.DoesNotExist:
        return Response.http404(None, "帖子不存在")
    except Exception as e:
        return Response.error(message=e)
    
    return Response.success({
        "id": id
    }, "更新成功")


@csrf_exempt
@require_POST
def publish_post(request):
    """
    发布新帖子

    need:
    ```json
    {
        "id": 1
    }
    ```
    get(data):
    ```json
    {
        "id": 1
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except Exception as e:
        return Response.bad_request(message=f"数据结构异常:{str(e)}")
    id = body.get("id", None)
    if id == None:
        return Response.missing_required_params(None, ["id"])
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response.http404(None, "帖子不存在")
    except Exception as e:
        return Response.error(message=e)
    
    post.publication_time = timezone.now()
    post.modification_time = timezone.now()
    post.draft = False

    try:
        post.save()
    except Exception as e:
        return Response.error(message=f"{str(e)}")

    return Response.success({
        "id": post.id
    }, "发布成功")

@csrf_exempt
@require_http_methods(["PUT"])
def update_post(request):
    """
    更新帖子

    need:
    ```json
    {
        "id": 1, // required
        "post": {  // all is optional
            "id_en": "aaabbb",
            "title": "标题",
            "abstract": "摘要",
            "body": "帖子主体",
            "word_count": 123, // 字数
            "tags": ["标签1", "标签2"],
            "categories": ["分类1", "分类2"],
            "categories_introduction": false, // 帖子是否是分类的介绍
        }
    }
    ```
    get(data):
    ```json
    {
        "id": 1
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    id = body.get("id", None)
    post = body.get("post", None)
    params = Response.create_missing_required_params(
        [id, post],
        ["id", "post"]
    )
    if params != True:
        return Response.missing_required_params(None, params)
    d = create_update_dict(post)
    d["modification_time"] = timezone.now()
    Post.objects.filter(id=id).update(**d)

    return Response.success({
        "id": id
    }, "更新成功")

@csrf_exempt
@require_POST
def change_visibility(request):
    """
    修改帖子可见性

    need:
    ```json
    {
        "id": 1,
        "visible": true, // 当前是否可见
    }
    ```
    get(data):
    ```json
    {
        "id": 1
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    id = body.get("id", None)
    visible = body.get("visible", None)
    params = Response.create_missing_required_params(
        [id, visible],
        ["id", "visible"]
    )
    if params != True:
        return Response.missing_required_params(None, params)
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response.http404(None, "帖子不存在")
    if post.visible != visible:
        return Response.bad_request({
            "id": id
        }, "是否可见与服务器数据不符")
    post.visible = not visible
    post.save()

    return Response.success({
        "id": id
    }, "修改可见性成功")

@csrf_exempt
@require_http_methods(["PUT"])
def update_categories(request):
    """
    更新分类目录

    need:
    ```json
    {
        "categories": []
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    categories = body.get("categories", None)
    if categories == None:
        return Response.missing_required_params(None, ["categories"])
    d = {
        "categories": categories
    }
    Post.objects.filter(id=1).update(**d)

    return Response.success(None, "更新分类目录成功")