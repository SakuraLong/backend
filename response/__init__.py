from django.http import JsonResponse
from rest_framework import status

# code
SUCCESS = 0
ERROR = 1


class Response:
    @staticmethod
    def success(data=None, message="success"):
        return JsonResponse(
            {
                "data": data, 
                "code": SUCCESS, 
                "message": message
            }, 
            status=status.HTTP_200_OK
        )

    @staticmethod
    def error(data=None, message=""):
        return JsonResponse(
            {
                "data": data, 
                "code": ERROR, 
                "message": message
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @staticmethod
    def custom(data=None, message="", code=SUCCESS, status=status.HTTP_200_OK):
        return JsonResponse(
            {
                "data": data, 
                "code": code, 
                "message": message
            }, 
            status=status
        )

    @staticmethod
    def http404(data=None, message="未查询到匹配结果"):
        return JsonResponse(
            {
                "data": None,
                "code": ERROR,
                "message": message,
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def bad_request(data=None, message=""):
        return JsonResponse(
            {
                "data": data,
                "code": ERROR,
                "message": message,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def create_missing_required_params(params=[], names=[]):
        res = []
        for i in range(0, min(len(params), len(names))):
            if params[i] is None:
                res.append(names[i])
        return res if len(res) > 0 else True

    @staticmethod
    def missing_required_params(data=None, params=[], pre="缺少查询参数:"):
        return JsonResponse(
            {
                "data": data,
                "code": ERROR,
                "message": pre + ",".join(params),
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def forbidden():
        return JsonResponse(
            {
                "data": None,
                "code": ERROR,
                "message": "Your IP is not allowed to access this service.",
            },
            status=status.HTTP_403_FORBIDDEN
        )

    @staticmethod
    def token_error(message="UNAUTHORIZED"):
        return JsonResponse(
            {
                "data": None,
                "code": ERROR,
                "message": message,
            },
            status=status.HTTP_401_UNAUTHORIZED
        )