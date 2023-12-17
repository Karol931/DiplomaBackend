from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

# def find_user_id(username):
#     user_id = User.objects.get(username=username).id
#     print(user_id)
#     return user_id

@csrf_exempt
def get_id(request):
    if request.method == "POST":
        username = json.loads(request.body.decode('utf-8'))['username']
        
        id = User.objects.get(username=username).id
        print(id)
        return JsonResponse({'id': id})