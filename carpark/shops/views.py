from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Shops
from django.http import JsonResponse
# Create your views here.


@csrf_exempt
def create(request):
    if request.method == "POST":
        shops = json.loads(request.body.decode('utf-8'))['shops']
        for shop in shops:
            shop_exists = Shops.objects.filter(name=shop['name'])
            if not shop_exists.exists():
                Shops.objects.create(name = shop['name'], zone = shop['zone'])
        
        if not shop_exists.exists():
            return JsonResponse()
        else:
            return JsonResponse({"err": "one or more shops already exist"})