from django.db import models

from datetime import datetime, timedelta

from django.utils import timezone
import django

# Create your models here.

STATUS_CHOICES = [
    (0, "using"),
    (1, "signout"),
    (2, "forbidden"),
]

AUTHORITY_CHOICES = [
    (0, "super"),
    (1, "admin"),
    (2, "visitor"),
]

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=500, blank=False, null=False)
    token = models.CharField(max_length=300)
    token_expiration_time = models.DateTimeField(null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)

class IP(models.Model):
    """
    计算当前时间与上次访问时间的差值
    
    1. 如果超过1min
        - 清空last_10_times_interval
        - 更新last_time
    2. 如果小于1min
        - 检查last_10_times_interval长度
            - 等于10
                - 计算平均值
                    - 小于等于10s
                        - 墙1天
                    - 大于10s
                        - pop(0) and append
            - 小于10
                - append
    """
    ip = models.CharField(primary_key=True, max_length=40, blank=False, null=False)
    
    last_time = models.DateTimeField(default=timezone.make_aware(datetime(2020, 1, 1, 12, 0))) # 上一次访问的时间
    last_10_times_interval = models.JSONField(default=list) # 上10次访问的时间间隔
    block = models.BooleanField(default=False) # 是否被墙
    unblock_time = models.DateTimeField(null=True) # 解封时间

    # get 请求与其他不同 get更加宽松
    get_last_time = models.DateTimeField(default=timezone.make_aware(datetime(2020, 1, 1, 12, 0))) # 上一次访问的时间
    get_last_10_times_interval = models.JSONField(default=list) # 上10次访问的时间间隔
    get_block = models.BooleanField(default=False) # 是否被墙
    get_unblock_time = models.DateTimeField(null=True) # 解封时间

    def block_update(self):
        now = timezone.now()
        if self.block and (now - self.unblock_time).total_seconds() > 0:
            self.block = False
        if self.get_block:
            return
        
        time_diff = (now - self.last_time).total_seconds()

        self.last_time = now
        if time_diff > 60:
            self.last_10_times_interval = []
        else:
            if len(self.last_10_times_interval) >= 10:
                average_interval = sum(self.last_10_times_interval) / len(self.last_10_times_interval)
                if average_interval <= 10:
                    self.block = True
                    self.unblock_time = now + timedelta(hours=5)
                else:
                    self.last_10_times_interval.pop(0)
                    self.last_10_times_interval.append(time_diff)
            else:
                self.last_10_times_interval.append(time_diff)
    
    def get_block_update(self):
        now = timezone.now()
        if self.get_block and (now - self.get_unblock_time).total_seconds() > 0:
            self.get_block = False
        if self.get_block:
            return
        
        time_diff = (now - self.get_last_time).total_seconds()

        self.get_last_time = now
        if time_diff > 20:
            self.get_last_10_times_interval = []
        else:
            if len(self.get_last_10_times_interval) >= 10:
                average_interval = sum(self.get_last_10_times_interval) / len(self.get_last_10_times_interval)
                if average_interval <= 1:
                    self.get_block = True
                    self.get_unblock_time = now + timedelta(minutes=1)
                else:
                    self.get_last_10_times_interval.pop(0)
                    self.get_last_10_times_interval.append(time_diff)
            else:
                self.get_last_10_times_interval.append(time_diff)
