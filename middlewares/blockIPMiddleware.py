from user.models import IP
from response import Response

from datetime import datetime, timedelta

from django.utils import timezone
from mybackend.settings import MEDIA_URL

class BlockIPMiddleware:
    BLOCKED_IPS = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        get = request.method == "GET"
        # 获取请求的 IP 地址
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        origin_ip = ip
        ip = "get-" + ip if get else ip

        # 检查 IP 是否在禁止列表中
        if ip in self.BLOCKED_IPS:
            if (timezone.now() - self.BLOCKED_IPS[ip]).total_seconds() > 0:
                del self.BLOCKED_IPS[ip]
            else:
                return Response.forbidden()
            
        # 检查是否是请求media资源
        if request.path.startswith(MEDIA_URL):
            # 调用视图
            response = self.get_response(request)
            return response

        obj, created = IP.objects.get_or_create(ip=origin_ip)
        if get:
            obj.get_block_update()
            if obj.get_block:
                self.BLOCKED_IPS[ip] = obj.get_unblock_time
                obj.save()
                return Response.forbidden()
        else:
            obj.block_update()
            if obj.block:
                self.BLOCKED_IPS[ip] = obj.unblock_time
                obj.save()
                return Response.forbidden()
        obj.save()

        # 调用视图
        response = self.get_response(request)
        return response