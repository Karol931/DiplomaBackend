from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name="create" ),
    path('get_parking/', views.get_parking, name="get_parking"),
    path('delete_all/', views.delete_all_parkings, name="delete_all"),
    path('get_names/', views.get_names, name="get_names"),
    path('find_spot/', views.find_spot, name="find_spot"),
    path('delete_spot/', views.delete_spot, name="delete_spot"),
    path('create_shops/', views.crete_shops, name="create_shops"),
    path('get_parking_options/', views.get_parking_options, name="get_parking_options"),
]