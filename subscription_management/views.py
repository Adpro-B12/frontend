from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import requests
from django.shortcuts import render

clar = 'http://35.240.230.131/subscription-box'
def box_list(request):


    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')

    if min_price and max_price:
        response = requests.get(clar + f'/price?minPrice={min_price}&maxPrice={max_price}')
    else:
        response = requests.get(clar+'/getAll')

        
    boxes = response.json()
    return render(request, 'boxes_list.html', {'boxes': boxes})

def box_detail(request, box_id):
    response = requests.get(clar+f'/viewDetails/{box_id}')
    box = []
    try:
        box = response.json()
    except:
        box = []
    print("TESTTT")
    return render(request, 'box_detail_subscription.html', {'box': box})

def subscribe(request, box_id):
    username = request.COOKIES.get('username')
    response = requests.get(clar+f'/viewDetails/{box_id}')
    box = []
    try:
        box = response.json()
    except:
        box = []
    print("TESTTT")
    type = box['type']
    data = {'username': username, 'type':type}
    response = requests.post(f'http://34.143.166.153/api/subscriptions/subscribe/{box_id}', json=data)


    responses = HttpResponseRedirect(reverse('subscription_management:box_list'))
    return responses

def cancel(request, sub_id):
    response = requests.post(f'http://34.143.166.153/api/subscriptions/cancel/{sub_id}')
    return HttpResponseRedirect(reverse('subscription_management:subscription_history'))

def subscription_history(request):
    username = request.COOKIES.get('username')
    data = {'username': username}

    try:
        response = requests.get('http://34.143.166.153/api/subscriptions/subscriptions', json=data)
        subscriptions = response.json()
    except:
        subscriptions = []
    return render(request, 'subscription_history.html', {'subscriptions': subscriptions})

def admin_list(request):
    role = request.COOKIES.get('role')
    if(role!="ADMIN"):
        return HttpResponseForbidden("Access denied: You do not have the necessary permissions to view this page.")
    return render(request, 'subscription_admin.html')

def admin_cancel(request, sub_id):
    role = request.COOKIES.get('role')
    response = requests.post(f'http://34.143.166.153/api/subscriptions/set_status/{sub_id}', json={"status":"CANCELLED","role":role})
    return HttpResponseRedirect(reverse('subscription_management:admin_list'))

def admin_pending(request, sub_id):
    role = request.COOKIES.get('role')
    response = requests.post(f'http://34.143.166.153/api/subscriptions/set_status/{sub_id}', json={"status":"PENDING","role":role})
    return HttpResponseRedirect(reverse('subscription_management:admin_list'))

def admin_approve(request, sub_id):
    role = request.COOKIES.get('role')
    response = requests.post(f'http://34.143.166.153/api/subscriptions/set_status/{sub_id}', json={"status":"APPROVED","role":role})
    return HttpResponseRedirect(reverse('subscription_management:admin_list'))


def fetch_boxes(request):
    # Extract minPrice and maxPrice from the request's query parameters
    min_price = request.GET.get('minPrice', None)
    max_price = request.GET.get('maxPrice', None)
    name = request.GET.get('name', None)

    # Construct the URL based on the provided parameters
    
    url = clar+f'/price?minPrice={min_price}&maxPrice={max_price}'
    response = requests.get(url)
    data = []
    try:
        data = response.json()
    except:
        data = []

    if name:
        url = clar+f'/name?name={name}'

        data2 = []
        try:
            data2 = requests.get(url).json()
        except:
            data2 = []

        dict1 = {item['id']: item for item in data}
        dict2 = {item['id']: item for item in data2}

        # Finding common ids
        intersection_ids = set(dict1.keys()) & set(dict2.keys())

        # Getting the intersection items based on common ids
        intersection = [dict1[id] for id in intersection_ids]

        return JsonResponse(intersection, safe=False)
    
    return JsonResponse(data, safe=False)

def fetch_subscriptions(request):
    status = request.GET.get('status', None)
        
    username = request.COOKIES.get('username')
    data = {'username': username}

    url = 'http://34.143.166.153/api/subscriptions/subscriptions'
    response = requests.get(url, json=data)

    data = []
    try:
        data = response.json()
    except:
        data = []

    if status:
        print("STATUS", status)
        url = f'http://34.143.166.153/api/subscriptions/subscriptions_by_status?status={status}'

        data2 = []
        try: 
            data2 = requests.get(url).json()
        except:
            data2 = []

        dict1 = {item['id']: item for item in data}
        dict2 = {item['id']: item for item in data2}

        # Finding common ids
        intersection_ids = set(dict1.keys()) & set(dict2.keys())

        # Getting the intersection items based on common ids
        intersection = [dict1[id] for id in intersection_ids]

        return JsonResponse(intersection, safe=False)
    
    return JsonResponse(data, safe=False)

def get_all_subscriptions(request):
    url = 'http://34.143.166.153/api/subscriptions/allsubs'
    response = requests.get(url)
    data = []
    try:
        data = response.json()
    except:
        data = []
    return JsonResponse(data, safe=False)

    

