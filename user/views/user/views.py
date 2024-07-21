"""
用户管理相关接口
"""

from user.models import User
from response import Response
from utils.en_and_decryption import sha256_encrypt, rsa_decrypt, base64_aes_decrypt
from .utils import create_token

import json

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods

@csrf_exempt
@require_POST
def login(request):
    """
    用户登录

    need:
    ```json
    {
        username: '',
        password: ''
    }
    ```
    """
    body = request.body
    try:
        body = json.loads(body)
    except:
        return Response.bad_request(message="数据结构异常")
    username = body.get("username", None)
    password = body.get("password", None)
    params = Response.create_missing_required_params(
        [username, password],
        ["username", "password"]
    )
    if params != True:
        return Response.missing_required_params(None, params)

    try:
        username = base64_aes_decrypt(username)
        password = rsa_decrypt(password)
        password = sha256_encrypt(password)
    except:
        return Response.error(message="用户名或密码有误")
    
    try:
        user = User.objects.filter(status=0).get(username=username)
    except:
        return Response.error(message="用户名或密码有误")
    
    if user.password != password:
        return Response.error(message="用户名或密码有误")
    
    # 验证通过 配置token
    token = create_token(username) # encrypted

    return Response.success({
        "token": token
    }, "登录成功")