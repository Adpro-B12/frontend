import django.contrib.messages as message
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.core import serializers

# Create your views here.

def get_all_reviews(request):
    response = requests.get('http://34.87.138.18/api/reviews/all')
    reviews = response.json()
    return render(request, 'review.html', {'reviews': reviews})

def create_review(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        data = serializers.serialize('json',[
            {
                'rating': rating,
                'review': review,
            }
        ])

        response = requests.post('http://34.87.138.18/api/reviews/create', data=data, headers={'Content-Type': 'application/json'})
        res = response.json()
        return redirect('subsbox_review:review_list')
    else:
        message.info(request, 'Invalid')
        return render(request, 'create_review.html')