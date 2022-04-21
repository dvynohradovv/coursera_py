from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseBadRequest


# Create your views here.


def simple_route(request):
    if request.method == 'GET':
        return HttpResponse("GET request, status: 200")
    else:
        return HttpResponseNotAllowed("Not GET request, status: 405")


def slug_route(request, slug: str):
    if len(slug) > 16:
        raise Http404
    return HttpResponse(slug)


def sum_route(request, left_operand, right_operand):
    try:
        return HttpResponse(int(left_operand) + int(right_operand))
    except (ValueError, TypeError):
        raise Http404


def sum_get_method(request):
    if request.method == 'GET':
        try:
            a, b = request.GET.get("a"), request.GET.get("b")
            a, b = int(a), int(b)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Bad request, status: 400")
        return HttpResponse(a + b)
    else:
        return HttpResponseNotAllowed("POST request, status: 405")


def sum_post_method(request):
    if request.method == 'POST':
        try:
            a, b = request.POST.get("a"), request.GET.get("b")
            a, b = int(a), int(b)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Bad request, status: 400")
        return HttpResponse(a + b)
    else:
        return HttpResponseNotAllowed("POST request, status: 405")
