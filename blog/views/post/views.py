"""
帖子相关的接口
"""

from blog.models import Post
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from response import Response

from .utils import *


@csrf_exempt
def testset(request):
    post_data = {
        "id_en": "bbest-test7",
        'title': 'Sample Title 444444',
        'abstract': 'This is an abstract for the post.',
        'body': '# This is the body of the post.',
        'word_count': 1000,
        'publication_time': timezone.now(),  # 使用当前时间作为发布时间
        'modification_time': timezone.now(),  # 使用当前时间作为修改时间
        'tags': ['sample', 'example', 'test'],
        'categories': ['News', 'Local'],
        'categories_introduction': False,
        "visible": True,
    }

    # 创建Post实例
    post = Post(**post_data)

    # 保存到数据库（这里不会真正设置id为0，但可以逻辑上认为这是id=0的记录）
    post.save()

    return Response.success()

@csrf_exempt
def testget(request):
    post = Post.objects.get(id=4)
    return Response.success({
        "post": PostSerializerForFull(post).data
    })

@csrf_exempt
@require_GET
def get_posts(request):
    """
    返回全部可见帖子的信息

    get(data):
    ```json
    {
        "posts": [
            {
                "title": "标题",
                "author": "作者",
                "title_pinyin": "biao ti",
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
    ```
    """
    posts = Post.objects.filter(visible=True, draft=False)
    res = []
    for post in posts:
        res.append(PostSerializerForAbstract(post).data)
    return Response.success(res)

@csrf_exempt
@require_GET
def get_post(request):
    """
    根据id返回可见帖子的具体信息

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
            "author": "作者",
            "title_pinyin": "biao ti",
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
        }
    }
    ```
    """
    id = request.GET.get("id", None)
    if id == None:
        return Response.missing_required_params(None, ["id"])
    try:
        post = Post.objects.filter(visible=True, draft=False).get(id=id)
    except Post.DoesNotExist:
        return Response.http404(None, "帖子不存在")
    
    return Response.success({
        "post": PostSerializerForFull(post).data
    })

@csrf_exempt
@require_GET
def get_categories(request):
    """
    获取分类目录

    get(data):
    ```json
    {
        "categories": []
    }
    ```
    """
    post = Post.objects.get(id=1)
    c = post.categories
    return Response.success({
        "categories": c
    })