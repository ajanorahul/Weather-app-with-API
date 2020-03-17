from django.urls import path
from api import views



urlpatterns = [

    path('', views.index, name='index'),
      path('delete/<city_name>/', views.city_delete, name='city_delete'),

]
