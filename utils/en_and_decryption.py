import hashlib
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES

from password import RSA_PRIVATE_KEY, AES_KEY

# 关于AES加密配置
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
# 关于AES加密配置

def sha256_encrypt(str):
    original_string = str
    sha256_hash = hashlib.sha256()
    encoded_string = original_string.encode()
    sha256_hash.update(encoded_string)
    return sha256_hash.hexdigest()

def rsa_decrypt(str):
    private_key = serialization.load_pem_private_key(
        RSA_PRIVATE_KEY.encode(),
        password=None,
        backend=default_backend()
    )
    encrypted = base64.b64decode(str)
    decrypted = private_key.decrypt(
        encrypted,
        padding = padding.PKCS1v15()
    )
    return decrypted.decode()

def aes_encrypt(str):
    try:
        key = AES_KEY.encode('utf8')
        # 字符串补位
        data = pad(str)
        cipher = AES.new(key, AES.MODE_ECB)
        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        result = cipher.encrypt(data.encode())
        encodestrs = base64.b64encode(result)
        enctext = encodestrs.decode('utf8')
    except:
        enctext = False
    return enctext

def aes_decrypt(str):
    key = AES_KEY.encode('utf8')
    data = base64.b64decode(str)
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        # 去补位
        text_decrypted = unpad(cipher.decrypt(data))
        text_decrypted = text_decrypted.decode('utf8')
    except:
        text_decrypted = False
    return text_decrypted

def base64_encode(str):
    return base64.b64encode(str.encode()).decode()


def base64_decode(str):
    return base64.b64decode(str.encode()).decode()

def base64_aes_encrypt(str):
    return base64_encode(aes_encrypt(str))

def base64_aes_decrypt(str):
    return aes_decrypt(base64_decode(str))