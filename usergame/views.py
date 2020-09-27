from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from usergame.controllers import *

# Create your views here.


def index(request):
    return render(request,'index.html')


@api_view(['POST'])
def game_api(request):
    global data
    data = {
        'status' : 'Failed',
        'msg' : 'Operation Failed ',
        'data':'INVALID operation'
    }
    try:
        data = game(request)
    except Exception as e:
        print(e.args)
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def game_get_moves_api(request):
    data = {
        'status' : 'Failed',
        'msg' : 'Operation Failed',
        'data':'Unable to fetch moves'
    }
    try:
        data = game_get_moves(request)
    except Exception as e:
        print(e.args)
    return Response(data=data, status=status.HTTP_200_OK)