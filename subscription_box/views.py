from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from django.core import serializers
import django.contrib.messages as message
# Create your views here.

URL = 'http://35.240.230.131'

def manager(request):
    if is_admin(request):
        response = requests.get('http://35.240.230.131/subscription-box/getAll')
        print(response)
        box = response.json()
        print(box)
        
        response = requests.get('http://35.240.230.131/item/getAll')
        print(response)
        item = response.json()
        context = {
            'boxes': box,
            'items' : item
        }
        return render(request, 'manager.html', context)
    return redirect('homepage:show_homepage')


def create_subscription(request):
    if is_admin(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            type = request.POST.get('type')
            price = request.POST.get('price')

            data = {
                    'name': name,
                    'type': type, 
                    'price': price
                    }
            
            response = requests.post(URL+'/subscription-box/create', json=data, headers={'Content-Type': 'application/json'})
            print(response)
            res = response.json()
            print(res)
            return HttpResponse(redirect('subscription_box:manager'), status=200)
        else:
            message.info(request, 'Invalid request method')
            return HttpResponse(status=405)
    return redirect('homepage:show_homepage')
    
def update_subscription(request,id):
    if is_admin(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            type = request.POST.get('type')
            price = request.POST.get('price')

            data = {
                    'name': name,
                    'type': type, 
                    'price': price
                    }
            
            
            response = requests.put(URL+"/subscription-box/update/"+str(id), json=data, headers={'Content-Type': 'application/json'})
            print(response)
            return HttpResponse(status=200)
        
        else:
            message.info(request, 'Invalid request method')
            return HttpResponse(status=405)
    return redirect('homepage:show_homepage')
    
def delete_subscription(request,id):
    if is_admin(request):
        if request.method == 'POST':
            
            response = requests.delete(URL+"/subscription-box/delete/"+str(id))
            res = response.json()
            return HttpResponse(content=res,status=200)
        
        else:
            message.info(request, 'Invalid request method')
            return HttpResponse(status=405)
    return redirect('homepage:show_homepage')
    
def create_item(request):
    if is_admin(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            quantity = request.POST.get('quantity')

            data = {
                    'name': name,
                    'quantity': quantity,
                    }
            
            response = requests.post(URL+"/item/create", json=data, headers={'Content-Type': 'application/json'})
            print(response)
            res = response.json()
            print(res)
            return HttpResponse(redirect('subscription_box:manager'), status=200)
        
        else:
            message.info(request, 'Invalid request method')
            return HttpResponse(status=405)
    return redirect('homepage:show_homepage')
    
def update_item(request,id):
    if is_admin(request):
        if request.method == 'POST':
                name = request.POST.get('name')
                quantity = request.POST.get('quantity')

                print(name)
                print(quantity)

                data = {
                    'name': name,
                    'quantity': quantity
                    }
                
                
                response = requests.put(URL+"/item/edit/"+str(id), json=data, headers={'Content-Type': 'application/json'})
                print(response)
                return HttpResponse(redirect('subscription_box:get_item', id), status=200)
        
        else:
            message.info(request, 'Invalid request method')
            return HttpResponse(status=405)
    return redirect('homepage:show_homepage')
    
def delete_item(request,id):
    if is_admin(request):
        if request.method == 'POST':
            
            response = requests.delete(URL+"/item/delete/"+str(id))
            res = response.json()
            return HttpResponse(content=res,status=200)
        
        else:
            message.info(request, 'Invalid request method')
            return HttpResponse(status=405)
    return redirect('homepage:show_homepage')
    
def view_subscriptions(request, id):
    response = requests.get(URL+"/subscription-box/viewDetails/"+str(id))
    box = response.json()
    print(box)
    
    context = {
        "id": id,
        'box': box,
    }
    return render(request, 'box_detail.html', context)

def view_items(request,id):
    response = requests.get(URL+"/item/get/"+str(id))
    item = response.json()
    context = {
        "id": id,
        'item' : item
    }
    return render(request, 'item_detail.html', context)

def get_subscription_ajax(request):
    response = requests.get(URL+"/subscription-box/getAll")
    box = response.json()
    return HttpResponse(content=box, status=200)

def get_item_ajax(request):
    response = requests.get(URL+"/item/getAll")
    item = response.json()
    return HttpResponse(content=item, status=200)

def is_admin(request):
    role = request.COOKIES.get('role')
    if role == 'ADMIN':
        return True
    return False