from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name="reservation_create" ),
    path('delete_all/', views.delete_all, name="reservation_delete_all" ),
    path('cancel_reservation/', views.cancel_reservation, name="reservation_cancel"),
    path('get_reservation/', views.get_reservation, name="reservation_get"),
]