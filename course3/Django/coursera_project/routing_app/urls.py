from django.urls import path
from . import views

urlpatterns = [
    path('simple_route/', views.simple_route),
    path('slug_route/<slug:slug>', views.slug_route),
    path('sum_route/<str:left_operand>/<str:right_operand>', views.sum_route),
    path('sum_get_method/', views.sum_get_method),
    path('sumg_post_method/', views.sum_post_method),
]
