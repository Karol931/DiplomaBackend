from django.apps import AppConfig

class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    def ready(self):
        from .tasks import check_for_old_reservations
        check_for_old_reservations(repeat=60)
