from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.core import serializers
from django.contrib import messages

# Create your views here.

def get_all_reviews(request):
    username = request.COOKIES.get('username')
    if username:
        try:
            response = requests.get('http://34.87.138.18/api/reviews/all')
            response.raise_for_status()
            all_reviews = response.json()

            # Filter reviews based on username
            reviews = [review for review in all_reviews if review.get('userId') == username]

        except requests.exceptions.RequestException as e:
            print("Error fetching reviews:", e)
            reviews = []
            messages.error(request, 'Failed to fetch reviews.')
    else:
        messages.error(request, 'User is not authenticated.')
        reviews = []

    return render(request, 'review.html', {'reviews': reviews})

def create_review(request):
    if request.method == 'POST':
        rating = request.POST.get('ratingScore')
        review = request.POST.get('review')
        subsbox = request.POST.get('subscriptionBoxId')

        data = {
            'userId' : request.COOKIES.get('username'),
            'ratingScore': rating,
            'review': review,
            'subscriptionBoxId': subsbox,
        }
        response = requests.post('http://34.87.138.18/api/reviews/create', json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print(response)
            return redirect('subsbox_review:review_list')
        else:
            messages.error(request, 'Failed to create review.')
            return render(request, 'create_review.html')
    else:
        messages.info(request, 'Invalid method.')
        return render(request, 'create_review.html')
    
def delete_review(request, review_id):
    username = request.COOKIES.get('username')
    if username:
        try:
            # Fetch the review details
            response = requests.get(f'http://34.87.138.18/api/reviews/{review_id}')
            response.raise_for_status()
            review = response.json()

            # Check if the review belongs to the current user
            if review.get('userId') == username:
                delete_response = requests.delete(f'http://34.87.138.18/api/reviews/delete/{review_id}')
                if delete_response.status_code == 204:
                    messages.success(request, 'Review deleted successfully.')
                else:
                    messages.error(request, 'Failed to delete review.')
            else:
                messages.error(request, 'You are not authorized to delete this review.')
        except requests.exceptions.RequestException as e:
            print("Error fetching or deleting review:", e)
            messages.error(request, 'Failed to delete review.')
    else:
        messages.error(request, 'User is not authenticated.')

    return redirect('subsbox_review:review_list')