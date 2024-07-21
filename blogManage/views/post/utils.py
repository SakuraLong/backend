from rest_framework import serializers
from blog.models import Post

class TimestampField(serializers.DateTimeField):
    def to_representation(self, value):
        # 将datetime转换为时间戳（单位为秒），然后乘以1000得到毫秒
        return int(value.timestamp() * 1000)

    def to_internal_value(self, data):
        # 这里可以添加将时间戳转换回datetime的逻辑，如果需要的话
        pass

class PostSerializerForManageAbstract(serializers.ModelSerializer):
    publication_time = TimestampField()
    modification_time = TimestampField()

    class Meta:
        model = Post
        fields = [
            "id", 
            "id_en",
            "title", 
            "author",
            "title_pinyin",
            "visible",
            "draft",
            "abstract", 
            "word_count", 
            "publication_time", 
            "modification_time", 
            "tags", 
            "categories", 
            "categories_introduction",
        ]

class PostSerializerForManageFull(serializers.ModelSerializer):
    publication_time = TimestampField()
    modification_time = TimestampField()

    class Meta:
        model = Post
        fields = [
            "id", 
            "id_en",
            "title", 
            "author",
            "title_pinyin",
            "visible",
            "draft",
            "abstract", 
            "body",
            "word_count", 
            "publication_time", 
            "modification_time", 
            "tags", 
            "categories", 
            "categories_introduction",
        ]

CAN_UPDATE_ATTR = [
    "id_en",
    "title", 
    "abstract", 
    "body",
    "word_count", 
    "tags", 
    "categories", 
    "categories_introduction",
]

CAN_PUBLISH_ATTR = [
    "id_en",
    "title", 
    "abstract", 
    "body",
    "word_count", 
    "tags", 
    "categories", 
    "categories_introduction",
    "visible",
]

CAN_CREATE_DRAFT_ATTR = [
    "id_en",
    "title",
    "title_pinyin",
    "author",
]

CAN_SAVE_ATTR = [
    "title",
    "title_pinyin",
    "author",
    "abstract",
    "body",
    "word_count",
    "tags",
    "categories",
    "categories_introduction",
]

def create_save_dict(post):
    d = {}
    for attr in CAN_SAVE_ATTR:
        v = post.get(attr, None)
        if v != None:
            d[attr] = v
    return d

def create_publish_dict(post):
    d = {}
    miss = []
    for attr in CAN_PUBLISH_ATTR:
        v = post.get(attr, None)
        if v == None:
            miss.append(attr)
        d[attr] = v
    if len(miss) > 0:
        return miss
    return d

def create_update_dict(post):
    d = {}
    for attr in CAN_UPDATE_ATTR:
        v = post.get(attr, None)
        if v != None:
            d[attr] = v
    return d

def create_draft_dict(post):
    d = {}
    miss = []
    for attr in CAN_CREATE_DRAFT_ATTR:
        v = post.get(attr, None)
        if v == None:
            miss.append(attr)
        d[attr] = v
    if len(miss) > 0:
        return miss
    return d