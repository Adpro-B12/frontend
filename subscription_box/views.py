from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from django.core import serializers
import django.contrib.messages as message
# Create your views here.

url = 'http://35.240.230.131'

def manager(request):
    response = requests.get('http://35.240.230.131/subscription-box/viewAll')
    box = response.json()
    
    response = requests.get('http://35.240.230.131/item/getAll')
    item = response.json()
    context = {
        'box': box,
        'item' : item
    }
    return render(request, 'subscription_management/manager.html', context)


def create_subscription(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        price = request.POST.get('price')

        data = serializers.serialize('json', [
            {
                'name': name,
                'type': type, 
                'price': price
            }
        ])
        
        response = requests.post('http://35.240.230.131/subscription-box/create', data=data, headers={'Content-Type': 'application/json'})
        res = response.json()
        return HttpResponse(content=res,status=200)
    else:
        message.info(request, 'Invalid request method')
        return HttpResponse(status=405)
    
def update_subscription(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        type = request.POST.get('type')
        price = request.POST.get('price')

        data = serializers.serialize('json', [
            {
                'name': name,
                'type': type, 
                'price': price
            }
        ])
        
        response = requests.put(url+"/subscription-box/update/"+id, data=data, headers={'Content-Type': 'application/json'})
        res = response.json()
        return HttpResponse(content=res,status=200)
    
    else:
        message.info(request, 'Invalid request method')
        return HttpResponse(status=405)
    
def delete_subscription(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        response = requests.delete(url+"/subscription-box/delete/"+id)
        res = response.json()
        return HttpResponse(content=res,status=200)
    
    else:
        message.info(request, 'Invalid request method')
        return HttpResponse(status=405)
    
def create_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        data = serializers.serialize('json', [
            {
                'name': name,
                'quantity': quantity,
            }
        ])
        
        response = requests.post(url+"/item/create", data=data, headers={'Content-Type': 'application/json'})
        res = response.json()
        return HttpResponse(content=res,status=200)
    
    else:
        message.info(request, 'Invalid request method')
        return HttpResponse(status=405)
    
def update_item(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        data = serializers.serialize('json', [
            {
                'name': name,
                'quantity': quantity
            }
        ])
        
        response = requests.put(url+"/item/update/"+id, data=data, headers={'Content-Type': 'application/json'})
        res = response.json()
        return HttpResponse(content=res,status=200)
    
    else:
        message.info(request, 'Invalid request method')
        return HttpResponse(status=405)
    
def delete_item(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        response = requests.delete(url+"/item/delete/"+id)
        res = response.json()
        return HttpResponse(content=res,status=200)
    
    else:
        message.info(request, 'Invalid request method')
        return HttpResponse(status=405)
    
def view_subscriptions(request, id):
    response = requests.get(url+"/subscription-box/view/"+id)
    box = response.json()
    
    context = {
        'box': box,
    }
    return render(request, 'subscription_box/box_detail.html', context)

def view_items(request,id):
    response = requests.get(url+"/item/get/"+id)
    item = response.json()
    context = {
        'item' : item
    }
    return render(request, 'subscription_box/item_detail.html', context)

def get_subscription_ajax(request):
    response = requests.get(url+"/subscription-box/viewAll")
    box = response.json()
    return HttpResponse(content=box, status=200)

def get_item_ajax(request):
    response = requests.get(url+"/item/getAll")
    item = response.json()
    return HttpResponse(content=item, status=200)