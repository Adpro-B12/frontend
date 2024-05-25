from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import requests
from django.shortcuts import render

def box_list(request):


    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')

    if min_price and max_price:
        response = requests.get(f'http://localhost:8080/api/subscriptions/price?minPrice={min_price}&maxPrice={max_price}')
    else:
        response = requests.get('http://localhost:8080/api/subscriptions/all')

        
    boxes = response.json()
    return render(request, 'boxes_list.html', {'boxes': boxes})

def box_detail(request, box_id):
    response = requests.get(f'http://localhost:8080/api/subscriptions/{box_id}')
    box = response.json()
    return render(request, 'box_detail.html', {'box': box})

def subscribe(request, box_id):
    username = request.COOKIES.get('username')
    data = {'username': username}
    response = requests.post(f'http://localhost:8080/api/subscriptions/subscribe/{box_id}', json=data)

    subscription = response.json()

    responses = HttpResponseRedirect(reverse('subscription_management:box_list'))
    return responses

def cancel(request, sub_id):
    response = requests.post(f'http://localhost:8080/api/subscriptions/cancel/{sub_id}')
    return HttpResponseRedirect(reverse('subscription_management:subscription_history'))

def subscription_history(request):
    username = request.COOKIES.get('username')
    data = {'username': username}
    response = requests.get('http://localhost:8080/api/subscriptions/subscriptions', json=data)
    subscriptions = response.json()
    return render(request, 'subscription_history.html', {'subscriptions': subscriptions})


def fetch_boxes(request):
    # Extract minPrice and maxPrice from the request's query parameters
    min_price = request.GET.get('minPrice', None)
    max_price = request.GET.get('maxPrice', None)
    name = request.GET.get('name', None)

    # Construct the URL based on the provided parameters
    
    url = f'http://localhost:8080/api/subscriptions/price?minPrice={min_price}&maxPrice={max_price}'
    response = requests.get(url)
    data = response.json()

    if name:
        url = f'http://localhost:8080/api/subscriptions/name?name={name}'
        data2 = requests.get(url).json()

        dict1 = {item['id']: item for item in data}
        dict2 = {item['id']: item for item in data2}

        # Finding common ids
        intersection_ids = set(dict1.keys()) & set(dict2.keys())

        # Getting the intersection items based on common ids
        intersection = [dict1[id] for id in intersection_ids]

        return JsonResponse(intersection, safe=False)
    
    return JsonResponse(data, safe=False)

    

