from django.shortcuts import render
from django.http.response import HttpResponse
from track.classes import CommandCenter
from track.models import ParkingSpot, Item, Drone, ItemDroneHistory
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def view_items(request):
    order_filter = request.POST.get('ord_status', 'ORDERED').strip()
    items = Item.objects.filter(order_status=order_filter)
    return render(request, 'index.html', context={'items': items,
                                                  'order_filter': order_filter,
                                                  'status': 'Deliver' if order_filter == 'ORDERED' else 'View Details'}) 


def item_details(request, item_id):
    try:
        data = ItemDroneHistory.objects.filter(item=item_id).order_by('time_stamp')
        item = Item.objects.get(id=item_id)
        statuses = ['ORDERED', 'PACKED', 'SHIPPED', 'DELIVERED']
        progress_track = ['todo']*4
        for i in range(4):
            if statuses[i] == item.order_status:
                progress_track[i] = 'done'
                break
            progress_track[i] = 'done'
    except:
        data = {}
        progress_track = {}
    return render(request, 'view_item.html', context={'items': data, 'track': progress_track})


def view_drones(request):
    try:
        drones = Drone.objects.all()
    except:
        drones = {}

    return render(request, 'view_drones.html', context={'drones': drones})


def view_parking_slots(request):
    try:
        parking_slots = ParkingSpot.objects.all()
    except:
        parking_slots = {}

    return render(request, 'view_parking_slots.html', context={'slots': parking_slots})

def about(request):
    return render(request, 'about.html', context={})


def deliver(request, item_id):
    instruction = 'PICKUP'
    command = CommandCenter('PICKUP', item_id)
    status = command.send_instruction()
    message = 'Succesessfully deliveried item to given address' if status else 'Something went wrong'
    return render(request, 'index.html', context={'message': message})

