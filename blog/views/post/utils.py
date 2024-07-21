from rest_framework import serializers
from blog.models import Post

class TimestampField(serializers.DateTimeField):
    def to_representation(self, value):
        # 将datetime转换为时间戳（单位为秒），然后乘以1000得到毫秒
        return int(value.timestamp() * 1000)

    def to_internal_value(self, data):
        # 这里可以添加将时间戳转换回datetime的逻辑，如果需要的话
        pass

class PostSerializerForAbstract(serializers.ModelSerializer):
    publication_time = TimestampField()
    modification_time = TimestampField()

    class Meta:
        model = Post
        fields = [
            "id",
            "id_en",
            "author",
            "title",
            "title_pinyin",
            "abstract",
            "word_count",
            "publication_time",
            "modification_time",
            "tags",
            "categories",
            "categories_introduction",
        ]

class PostSerializerForFull(serializers.ModelSerializer):
    publication_time = TimestampField()
    modification_time = TimestampField()

    class Meta:
        model = Post
        fields = [
            "id",
            "id_en",
            "author",
            "title",
            "title_pinyin",
            "abstract",
            "body",
            "word_count",
            "publication_time",
            "modification_time",
            "tags",
            "categories",
            "categories_introduction",
        ]