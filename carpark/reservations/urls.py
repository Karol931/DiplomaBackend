from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name="create" ),
    path('delete_all/', views.delete_all, name="delete_all" ),
    path('cancel_reservation/', views.cancel_reservation, name="cancel_reservation"),
    path('get_reservation/', views.get_reservation, name="get_reservation"),
]