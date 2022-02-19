
from django.contrib import admin
from django.urls import path

from calculate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('calculate/<int:number1>/<int:number2>', views.enter_numbers, name='enter_numbers'),
    path('get_answer/<str:identifier>/', views.get_answer, name='get_answer')
]
