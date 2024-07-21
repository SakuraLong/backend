# backend

这是一些项目共用的后端，具体项目对应的不同代码可以去不同的应用下查看

#### 项目
- `blog` `-->` blog个人博客
- `blogManage` `-->` blogManage个人博客管理

#### media

运行项目可能需要在根目录下新增`media`文件夹

#### 配置

运行项目需要在根目录下新增`config.py`文件，文件格式如下：
```python
DATABASE_USER = '数据库user'

DATABASE_HOST = '数据库host'

DATABASE_PORT = '数据库port'
```

#### 密码

运行项目需要在根目录下新增`password.py`文件，文件格式如下：
```python
SECRET_KEY = "django SECRET_KEY"

SAKURA_PWD = "数据库密码"

RSA_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----"""

AES_KEY = "需要与前端AES_KEY相同"

TOKEN_KEY = ""
```