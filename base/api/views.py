from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomSerializer
from base.models import Room


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id',
    ]
    
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializedrooms = RoomSerializer(rooms, many=True)   

    return Response(serializedrooms.data)

@api_view(['GET'])
def getRoom(request,id):
    room = Room.objects.get(id=id)
    serializedroom = RoomSerializer(room, many=False)   

    return Response(serializedroom.data)
