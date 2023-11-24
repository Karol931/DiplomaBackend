from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name="create" ),
    path('get_parking/', views.get_parking, name="get_parking"),
    path('delete_all/', views.delete_all_parkings, name="delete_all")
]