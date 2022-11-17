from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('context_suggest',views.context_suggest,name='context_suggest'),
    path('context_result1',views.context_result1,name='context_result1'),
    path('details/',views.details,name='details'),
]