from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def echo(request):
    params = {
        "method": request.method.lower(),
        "param_name": "",
        "param_value": "",
        "statement": request.META.get("HTTP_X_PRINT_STATEMENT", "empty"),
    }
    query_string = request.META['QUERY_STRING']
    if len(query_string) > 0:
        params["param_name"] = query_string[0]
        params["param_value"] = request.GET.get(params["param_name"])
    return render(request, "template_app/echo.html", params)


def filters(request):
    params = {k: v for k, v in request.GET.items()}
    return render(request, "template_app/filters.html", params)
