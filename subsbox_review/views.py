import django.contrib.messages as message
from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.core import serializers

# Create your views here.

def get_all_reviews(request):
    response = requests.get('http://localhost:8080/api/reviews/all')
    reviews = response.json()
    return render(request, 'review.html', {'reviews': reviews})

def create_review(request):
    user_id = requests.GET.get('userId')
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        data = serializers.serialize('json',[
            {
                'rating': rating,
                'review': review,
            }
        ])

        response = request.post('http://localhost:8080/api/reviews/create', data=data, headers={'Content-Type': 'application/json'})
        res = response.json()
        return HttpResponse(content=res, status=200)
    
    else:
        message.info(request, 'Invalid')
        return HttpResponse(status=405)