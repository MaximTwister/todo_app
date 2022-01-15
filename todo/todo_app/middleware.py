from django.http import HttpResponseRedirect


class AjaxRedirect:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        content_type = request.META.get("CONTENT_TYPE")
        is_ajax = content_type == "application/json"
        if is_ajax and type(response) == HttpResponseRedirect:
            response.status_code = 278
        print(f"Middleware response.status_code : {response.status_code}")

        return response
