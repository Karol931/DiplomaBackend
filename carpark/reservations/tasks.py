
from .models import Reservations, ArchivedReservations
from datetime import datetime
from usersAPI.models import User
from parking_lot.models import Parking
from background_task import background

@background(schedule=60)
def check_for_old_reservations():
    date = datetime.now()
    old_reservations = Reservations.objects.filter(end_date__lt=date)
    print("Running")
    print(date, old_reservations)
    if old_reservations.exists():
        for old_reservation in old_reservations:
            print(old_reservation.id)
            user = User.objects.get(id=old_reservation.user_id)
            parking = Parking.objects.get(id=old_reservation.parking_id)
            ArchivedReservations.objects.create(start_date = old_reservation.start_date, end_date = old_reservation.end_date, user=user, parking=parking)
            old_reservation.delete()