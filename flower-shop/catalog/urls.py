# catalog/urls.py
from django.urls import path
from django.http import HttpResponse

app_name = 'catalog'

urlpatterns = [
    path('', lambda request: HttpResponse("Каталог (заглушка)"), name='bouquet_list'),
]