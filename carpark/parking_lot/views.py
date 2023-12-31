from django.http import JsonResponse, HttpResponse
import random
from .models import Spot, Zone, Level, Parking
from shops.models import Shops
from django.views.decorators.csrf import csrf_exempt
import json
import re
import networkx as nx
import math
# Create your views here.

@csrf_exempt
def create(request):
    if request.method == "POST":
        levels = json.loads(request.body.decode('utf-8'))['levels']
        name = json.loads(request.body.decode('utf-8'))['name']
        occupacy = float(re.sub(r'%','',json.loads(request.body.decode('utf-8'))['occupacy']))/100
        is_paid = json.loads(request.body.decode('utf-8'))['isPaid']
        # print(name, levels, occupacy, is_paid)

        #stałe
        zones = ['A', 'B', 'C', 'D']
        levels = [l + 1 for l in range(levels)]
        number_of_spots_in_zone = 14

        distance = dijkstra(zones, levels)
        # print(distance)
        try:
            parking = Parking.objects.create(name=name, is_paid=is_paid)
        except:
            return JsonResponse({"err": "Parking with this name alerady exists"}, status=400)
        for l in levels:
            level = Level.objects.create(level_number=l, parking=parking)
            for z in zones:
                zone = Zone.objects.create(name=z, level=level)
                
                spots = [{'spot_number' : spot + 1 , 'user_id': None, 'is_taken' : True if random.random() <= occupacy else False } for spot in range(number_of_spots_in_zone)]
                for s in spots:
                    # print(f'{l}{z}{s["spot_number"]}')
                    dist = distance[f'{l}{z}{s["spot_number"]}']
                    spot = Spot.objects.create(spot_number=s['spot_number'], user_id=s['user_id'], is_taken=s['is_taken'], distance=dist, zone=zone)
        
        return JsonResponse({})


def get_names(request):

    querry = Parking.objects.values_list('name')
    names = {'names': [name[0] for name in querry]}

    # print(names)

    return JsonResponse(names)

@csrf_exempt
def get_parking(request):
    # geting parking from database
    if request.method == 'POST':
        # token = request.headers['Authorization']
        # print(token)
        # token = jwt.decode(request.headers['Authorization'].split(" ")[1], base64.b64decode(SECRET_KEY), ["HS256"])
        # print(token)

        name = json.loads(request.body.decode('utf-8'))['name']
        parking = Parking.objects.get(name=name)

        levels = Level.objects.filter(parking_id=parking.id)
        levels_ids = [l.id for l in levels]

        zones = Zone.objects.filter(level_id__in=levels_ids)
        zones_ids = [z.id for z in zones]

        spots = Spot.objects.filter(zone_id__in=zones_ids)
    
        # seting data to JSON
        data = { 'name': parking.name, 'is_paid': parking.is_paid, 'levels': [{'level': level.level_number, 'zones' : [{'zone' : zone.name, 'spots' : [{'number' : spot.spot_number , 'user_id': spot.user_id, 'is_taken' : spot.is_taken} for spot in spots if zone.id == spot.zone_id]} for zone in zones if level.id == zone.level_id]} for level in levels]}
        
        return JsonResponse(data)

@csrf_exempt
def find_spot(request):
    if request.method == "POST":

        data = json.loads(request.body.decode('utf-8'))
        user_id = data['userId']
        level = data['level']
        parking_name = data['parkingName']
        parking = Parking.objects.get(name=parking_name)
        try:
            if data.__contains__('shop'):
                shop_name = data['shop']
                if shop_name == '' and level == '':
                    spot, zone, level = find_spot_no_params(parking)

                elif level == '':

                    levels = Level.objects.filter(parking_id=parking.id)
                    levels_ids = [l.id for l in levels]

                    shop_zone = Shops.objects.get(name=shop_name).zone
                    
                    zones = Zone.objects.filter(level_id__in=levels_ids, name=shop_zone)
                    zones_ids = [z.id for z in zones]

                    spot = Spot.objects.filter(zone_id__in=zones_ids, is_taken=False).order_by('distance').first()
                    
                    set_spot(spot, user_id)

                    zone = Zone.objects.get(id=spot.zone_id)
                    level = Level.objects.get(id=zone.level_id)
                    print(spot.spot_number, zone.name, level.level_number)

                elif shop_name == '':
                    spot, zone, level = find_spot_with_level(parking, level)
                    set_spot(spot, user_id)

                else:
                    shop_zone = Shops.objects.get(name=shop_name).zone

                    level_id = Level.objects.get(parking_id=parking.id, level_number=level).id

                    zone = Zone.objects.get(level_id = level_id, name=shop_zone)

                    spot = Spot.objects.filter(zone_id=zone.id, is_taken=False).order_by('distance').first()
                    set_spot(spot, user_id)

                    print(spot.spot_number, shop_zone, level)

            elif data.__contains__('zone'):
                zone = data['zone']
                if zone == '' and level == '':
                    spot, zone, level = find_spot_no_params(parking)
                    set_spot(spot, user_id)

                elif level == '':
                    levels = Level.objects.filter(parking_id=parking.id)
                    levels_ids = [l.id for l in levels]
                    
                    zones = Zone.objects.filter(level_id__in=levels_ids, name=zone)
                    zones_ids = [z.id for z in zones]

                    spot = Spot.objects.filter(zone_id__in=zones_ids, is_taken=False).order_by('distance').first()

                    zone = Zone.objects.get(id=spot.zone_id)
                    level = Level.objects.get(id=zone.level_id)
                    set_spot(spot, user_id)

                    print(spot.spot_number, zone.name, level.level_number)
                elif zone == '':

                    spot, zone, level = find_spot_with_level(parking, level)

                    set_spot(spot, user_id)
                else:
                    level_id = Level.objects.get(parking_id=parking.id, level_number=level).id

                    zone = Zone.objects.get(level_id = level_id, name=zone)

                    spot = Spot.objects.filter(zone_id=zone.id, is_taken=False).order_by('distance').first()

                    set_spot(spot, user_id)

                    print(spot.spot_number, zone.name, level)
            return JsonResponse({'spot': spot.id})
        except:
            return JsonResponse({'err': "No free spots in desired zone"}, status=400)

def set_spot(spot, user_id):
    old_spot = Spot.objects.filter(user_id=user_id)
    if old_spot.exists():
        old_spot = old_spot.first()
        old_spot.user_id = None  
        old_spot.is_taken = False           
        print(old_spot)
        old_spot.save()
    
    spot.user_id = user_id
    spot.is_taken = True
    spot.save()

def find_spot_no_params(parking):

    levels = Level.objects.filter(parking_id=parking.id)
    levels_ids = [l.id for l in levels]

    zones = Zone.objects.filter(level_id__in=levels_ids)
    zones_ids = [z.id for z in zones]

    spot = Spot.objects.filter(zone_id__in=zones_ids, is_taken=False).order_by('distance').first()

    zone = Zone.objects.get(id=spot.zone_id)
    level = Level.objects.get(id=zone.level_id)
    return spot, zone, level

def find_spot_with_level(parking, level):

    level = Level.objects.get(parking_id=parking.id, level_number=level)
    level_id = level.id

    zones = Zone.objects.filter(level_id=level_id)
    zones_ids = [z.id for z in zones]

    spot = Spot.objects.filter(zone_id__in=zones_ids, is_taken=False).order_by('distance').first()

    zone = Zone.objects.get(id=spot.zone_id)
    
    return spot, zone, level

@csrf_exempt
def get_parking_options(request):
    if request.method == "POST":
        shops = Shops.objects.all()
        data = { 'shops': [{'name': shop.name }for shop in shops]}

        parking_name = json.loads(request.body.decode('utf-8'))['parkingName']
        parking = Parking.objects.get(name=parking_name)

        levels = Level.objects.filter(parking_id=parking.id)

        data['levels'] = [{'number': level.level_number} for level in levels]
        zones = Zone.objects.filter(level_id=levels[0].id)
        data['zones'] = [{'name': zone.name} for zone in zones]

        return JsonResponse(data)

@csrf_exempt
def delete_spot(request):
    if request.method == "POST":
        user_id = json.loads(request.body.decode('utf-8'))['id']
        old_spot = Spot.objects.filter(user_id=user_id)
        if old_spot.exists():
            old_spot = old_spot.first()
            old_spot.user_id = None
            old_spot.is_taken = False     
            old_spot.save()
            return JsonResponse({})
        else:
            return JsonResponse({'err': 'user had no spot assigned'}, status=400)

def dijkstra(zones, levels):

    G = nx.Graph()
    # szerokosc 5, dlugosc 10
    pos_adj_per_level = 0
    for level in levels:
        G.add_node(f'Entr{level}', pos = (5 + pos_adj_per_level, 22.5))
        G.add_node(f'Lvl{level}', pos=(25 + pos_adj_per_level, 22.5))
        if level % 2 != 0:
            #D
            G.add_node(f'{level}D1', pos=(5 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}D2', pos=(5 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D3', pos=(5 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D4', pos=(5 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D5', pos=(5 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}D6', pos=(5 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}D7', pos=(6.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D8', pos=(8.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D9', pos=(11.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D10', pos=(13.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D11', pos=(10 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D12', pos=(10 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D13', pos=(10 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D14', pos=(10 + pos_adj_per_level, 26.25))
            #C
            G.add_node(f'{level}C1', pos=(5 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}C2', pos=(5 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C3', pos=(5 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C4', pos=(5 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C5', pos=(5 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}C6', pos=(5 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}C7', pos=(6.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C8', pos=(8.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C9', pos=(11.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C10', pos=(13.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C11', pos=(10 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C12', pos=(10 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C13', pos=(10 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C14', pos=(10 + pos_adj_per_level, 18.75))
            #A
            G.add_node(f'{level}A1', pos=(25 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}A2', pos=(25 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A3', pos=(25 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A4', pos=(25 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A5', pos=(25 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}A6', pos=(25 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}A7', pos=(23.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A8', pos=(21.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A9', pos=(18.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A10', pos=(16.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A11', pos=(20 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A12', pos=(20 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A13', pos=(20 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A14', pos=(20 + pos_adj_per_level, 26.25))
            #B
            G.add_node(f'{level}B1', pos=(25 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}B2', pos=(25 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B3', pos=(25 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B4', pos=(25 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B5', pos=(25 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}B6', pos=(25 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}B7', pos=(23.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B8', pos=(21.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B9', pos=(18.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B10', pos=(16.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B11', pos=(20 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B12', pos=(20 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B13', pos=(20 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B14', pos=(20 + pos_adj_per_level, 18.75))
        else:
            #A
            G.add_node(f'{level}A1', pos=(5 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}A2', pos=(5 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A3', pos=(5 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A4', pos=(5 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A5', pos=(5 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}A6', pos=(5 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}A7', pos=(6.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A8', pos=(8.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A9', pos=(11.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A10', pos=(13.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A11', pos=(10 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A12', pos=(10 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A13', pos=(10 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A14', pos=(10 + pos_adj_per_level, 26.25))
            #B
            G.add_node(f'{level}B1', pos=(5 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}B2', pos=(5 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B3', pos=(5 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B4', pos=(5 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B5', pos=(5 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}B6', pos=(5 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}B7', pos=(6.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B8', pos=(8.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B9', pos=(11.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B10', pos=(13.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B11', pos=(10 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B12', pos=(10 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B13', pos=(10 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B14', pos=(10 + pos_adj_per_level, 18.75))
            #D
            G.add_node(f'{level}D1', pos=(25 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}D2', pos=(25 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D3', pos=(25 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D4', pos=(25 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D5', pos=(25 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}D6', pos=(25 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}D7', pos=(23.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D8', pos=(21.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D9', pos=(18.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D10', pos=(16.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D11', pos=(20 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D12', pos=(20 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D13', pos=(20 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D14', pos=(20 + pos_adj_per_level, 26.25))
            #C
            G.add_node(f'{level}C1', pos=(25 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}C2', pos=(25 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C3', pos=(25 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C4', pos=(25 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C5', pos=(25 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}C6', pos=(25 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}C7', pos=(23.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C8', pos=(21.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C9', pos=(18.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C10', pos=(16.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C11', pos=(20 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C12', pos=(20 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C13', pos=(20 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C14', pos=(20 + pos_adj_per_level, 18.75))
        
        #edges
        #entrance to next level
        dist = distance(G, f'Entr{level}', f'Lvl{level}')
        G.add_edge(f'Entr{level}', f'Lvl{level}', weight=dist)

        for zone in zones:
            #entrance to 1
            dist = distance(G, f'Entr{level}', f'{level}{zone}1')
            G.add_edge(f'Entr{level}', f'{level}{zone}1', weight=dist)

            #entrance to 14
            dist = distance(G, f'Entr{level}', f'{level}{zone}14')
            G.add_edge(f'Entr{level}', f'{level}{zone}14', weight=dist)

            # side spots
            for spot in [1,2,3,4,5,6,7,8,9]:
                dist = distance(G, f'{level}A{spot}', f'{level}A{spot + 1}')
                G.add_edge(f'{level}{zone}{spot}', f'{level}{zone}{spot + 1}', weight=dist)
            
            # mid spots
            for spot in [14,13,12]:
                dist = distance(G, f'{level}A{spot}', f'{level}A{spot - 1}')
                G.add_edge(f'{level}{zone}{spot}', f'{level}{zone}{spot - 1}', weight=dist)
        
        # A11/10 - D11/10
        dist = distance(G, f'{level}A11', f'{level}D11')
        G.add_edge(f'{level}A11', f'{level}D11', weight=dist)
        dist = distance(G, f'{level}A10', f'{level}D10')
        G.add_edge(f'{level}A10', f'{level}D10', weight=dist)
        # B11/10 - C11/10
        dist = distance(G, f'{level}B11', f'{level}C11')
        G.add_edge(f'{level}B11', f'{level}C11', weight=dist)
        dist = distance(G, f'{level}B10', f'{level}C10')
        G.add_edge(f'{level}B10', f'{level}C10', weight=dist)

        pos_adj_per_level += 30
    # from exit to next entrance
    for level in levels:
        if G.nodes.__contains__(f'Entr{level+1}'):
            dist = distance(G, f'Entr{level+1}', f'Lvl{level}')
            G.add_edge(f'Entr{level+1}', f'Lvl{level}', weight=dist)

    distances = nx.dijkstra_predecessor_and_distance(G, f'Entr1')[1]

    return distances

def distance(G, first_node, second_node):
    first_node_pos = G.nodes[first_node]['pos']
    second_node_pos =  G.nodes[second_node]['pos']
    dist = math.sqrt((first_node_pos[0]-second_node_pos[0])**2 + (first_node_pos[1]-second_node_pos[1])**2)
    return round(dist,2)


def delete_all_parkings(request):
    # Parking.objects.all().delete()

    return HttpResponse()