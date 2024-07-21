from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    id_en = models.CharField(max_length=200, blank=False, null=False, unique=True)
    author = models.CharField(max_length=200, blank=False, null=False, default='SakuraLong')
    title = models.CharField(max_length=200, blank=False, null=False)
    title_pinyin = models.CharField(max_length=200, blank=False, null=False, default='biao ti')
    abstract = models.TextField(blank=True)
    body = models.TextField(blank=True)
    draft = models.BooleanField(default=True)
    word_count = models.IntegerField(default=0)
    publication_time = models.DateTimeField()  # 发布时间
    modification_time = models.DateTimeField()  # 修改时间
    tags = models.JSONField(default=list)
    categories = models.JSONField(default=list)
    categories_introduction = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)