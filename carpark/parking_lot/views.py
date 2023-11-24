from django.http import JsonResponse, HttpResponse
from .utils.rand_free_or_taken import rand_free_or_taken
import random
from .models import Spot, Zone, Level, Parking
# Create your views here.


def create(request):
    # zmienne do requesta
    levels = 3
    zones = ['A', 'B', 'C', 'D']
    # occupancy = 0.5
    number_of_spots_in_zone = 14
    name = 'test'
    
    parking = Parking.objects.create(name=name, is_paid=True)
    for l in range(levels):
        level = Level.objects.create(level_number=l + 1, parking=parking)
        for z in zones:
            zone = Zone.objects.create(name=z, level=level)
            
            spots = [{'spot_number' : spot + 1 , 'user_id': None, 'is_taken' : True if random.random() > 0.5 else False } for spot in range(number_of_spots_in_zone)]
            for s in spots:
                spot = Spot.objects.create(spot_number=s['spot_number'], user_id=s['user_id'], is_taken=s['is_taken'], zone=zone)
    
    return HttpResponse()

def get_parking(request):

    # geting data from database
    if request.method == "GET":
        parking2 = Parking.objects.get(id=4)

        levels = Level.objects.filter(parking_id=parking2.id)
        levels_ids = [l.id for l in levels]

        zones = Zone.objects.filter(level_id__in=levels_ids)
        zones_ids = [z.id for z in zones]

        spots = Spot.objects.filter(zone_id__in=zones_ids)

        # seting data to JSON
        data = { 'name': parking2.name, 'is_paid': parking2.is_paid, 'levels': [{'level': level.level_number, 'zones' : [{'zone' : zone.name, 'spots' : [{'number' : spot.spot_number , 'user_id': spot.user_id, 'is_taken' : spot.is_taken} for spot in spots if zone.id == spot.zone_id]} for zone in zones if level.id == zone.level_id]} for level in levels]}

        print(data)
        
        return JsonResponse(data)


def delete_all_parkings(request):
    # Parking.objects.all().delete()

    return HttpResponse()