# chat/views.py
from django.shortcuts import render
from chat.models import *

def index(request):
    rooms = Room.objects.all()
    my_rooms = []
    # participant = request.user.participant
    total_new_messages = 0

    for r in rooms:
        if request.user.participant in r.participants.all():
            my_rooms.append({
                "id":r.id,
                "participants":r.participants.all(),
                "new_messages_count":r.count_new_messages(request.user)
            })
            
    for my_room in my_rooms:      
        total_new_messages +=my_room['new_messages_count']
    
    return render(request, 'chat/index.html', {
        'my_rooms':my_rooms,
        'total_new_messages':total_new_messages    })

def room(request, room_id):
    room = Room.objects.get(id=room_id)
    message_list = Message.objects.filter(room_id=room_id)
    p = Participant.objects.filter(user=request.user)[0]
    for m in message_list:
        m.readers.add(p)
    return render(request, 'chat/room.html', {
        'room_id': room_id,
        'room':room,
        'message_list':message_list
    })