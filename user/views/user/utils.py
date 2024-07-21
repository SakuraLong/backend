from user.models import User
from utils.en_and_decryption import base64_aes_encrypt
from password import TOKEN_KEY
from utils.en_and_decryption import rsa_decrypt

import random
import jwt
from datetime import datetime, timedelta

from django.utils import timezone

def create_token(username):
    char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    length = 50

    # 生成随机字符串
    random_string = ''.join(random.choice(char_set) for _ in range(length))
    token = jwt.encode(
                {
                    "token": random_string,
                    "username": username
                },
                TOKEN_KEY,
                algorithm="HS256",
            )
    encrypted = base64_aes_encrypt(token)

    user = User.objects.get(username=username)
    user.token = random_string
    user.token_expiration_time = timezone.now() + timedelta(days=2)
    user.save()

    return encrypted

def get_token_data(token):
    try:
        auth_dict = jwt.decode(rsa_decrypt(token), TOKEN_KEY, algorithms=["HS256"])
    except:
        return {
            "token": "",
            "username": "",
        }
    return {
        "token": auth_dict.get("token", ""),
        "username": auth_dict.get("username", ""),
    }