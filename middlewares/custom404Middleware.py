from response import Response

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            if "Content-Type" not in response or response["Content-Type"] != "application/json":
                return Response.http404(None, '404')
        
        return response