from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import Reservations
from usersAPI.models import User
from parking_lot.models import Parking
import json

# Create your views here.

@csrf_exempt
def create(request):
    if request.method == "POST":   
        start_date = datetime.now()
        
        hours = int(json.loads(request.body.decode('utf-8'))['hours'])
        minutes = int(json.loads(request.body.decode('utf-8'))['minutes'])
        parking_name = json.loads(request.body.decode('utf-8'))['parkingName']
        user_id = json.loads(request.body.decode('utf-8'))['userId']
        # print(hours, minutes)

        end_date = start_date + timedelta(hours=hours, minutes=minutes)

        parking = Parking.objects.get(name=parking_name)
        user = User.objects.get(id=user_id)

        reservation = Reservations.objects.filter(user_id=user.id, parking_id=parking.id)
        if reservation.exists():
            reservation = reservation.first()
            reservation.end_date += timedelta(hours=hours, minutes=minutes)
            reservation.save()
        else:
            reservation = Reservations.objects.create(start_date=start_date, end_date=end_date, user=user, parking=parking)


        return JsonResponse({'end_date': reservation.end_date})

@csrf_exempt
def cancel_reservation(request):
    if request.method == "POST":
        parking_name = json.loads(request.body.decode('utf-8'))['parkingName']
        user_id = json.loads(request.body.decode('utf-8'))['userId']

        parking_id = Parking.objects.get(name=parking_name).id
        
        reservation = Reservations.objects.filter(parking_id=parking_id, user_id=user_id)
        if reservation.exists():
            reservation.delete()
        return JsonResponse({})

@csrf_exempt
def get_reservation(request):
    if request.method == "POST":
        parking_name = json.loads(request.body.decode('utf-8'))['parkingName']
        user_id = json.loads(request.body.decode('utf-8'))['userId']

        parking_id = Parking.objects.get(name=parking_name).id
        
        reservation = Reservations.objects.filter(parking_id=parking_id, user_id=user_id)
        if(reservation.exists()):
            reservation = reservation.first()
            return JsonResponse({'end_date': reservation.end_date})
        else:
            return JsonResponse({'end_date': "doesn\'t exist"}, status=400)

def delete_all(request):
    # Reservations.objects.all().delete()
    
    return JsonResponse({})