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

            # Fetch subscription box data from the given endpoint
            response_subs = requests.get('http://35.240.230.131/subscription-box/getAll')
            if response_subs.status_code == 200:
                subscription_boxes = {box['id']: {'name': box['name'], 'subscriptionBoxId': box['id']} for box in response_subs.json()}
                for review in reviews:
                    box_id = int(review['subscriptionBoxId'])
                    subscription_box_data = subscription_boxes.get(box_id, {'name': 'Unknown', 'subscriptionBoxId': box_id})
                    review['subscriptionBoxName'] = subscription_box_data['name']
                    review['subscriptionBoxId'] = subscription_box_data['subscriptionBoxId']
            else:
                messages.error(request, 'Failed to fetch subscription boxes.')
                return render(request, 'review.html', {'reviews': reviews})

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
        review_text = request.POST.get('review')
        subsbox_id = request.POST.get('subscriptionBoxId')

        # Fetch subscription box data from the given endpoint
        response_subs = requests.get('http://35.240.230.131/subscription-box/getAll')
        if response_subs.status_code == 200:
            subscription_boxes = {box['id']: box['name'] for box in response_subs.json()}
            subscription_box_name = subscription_boxes.get(int(subsbox_id), 'Unknown')
        else:
            messages.error(request, 'Failed to fetch subscription boxes.')
            return render(request, 'create_review.html')

        data = {
            'userId' : request.COOKIES.get('username'),
            'ratingScore': rating,
            'review': review_text,
            'subscriptionBoxId': subsbox_id,
            'subscriptionBoxName': subscription_box_name,
        }
        response = requests.post('http://34.87.138.18/api/reviews/create', json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            return redirect('subsbox_review:review_list')
        else:
            messages.error(request, 'Failed to create review.')
            return render(request, 'create_review.html', {'subscription_boxes': subscription_boxes})
    else:
        # Fetch subscription box data from the given endpoint
        response = requests.get('http://35.240.230.131/subscription-box/getAll')
        if response.status_code == 200:
            subscription_boxes = response.json()
            return render(request, 'create_review.html', {'subscription_boxes': subscription_boxes})
        else:
            messages.error(request, 'Failed to fetch subscription boxes.')
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

# def update_status(request):
#     if is_admin(request):



def is_admin(request):
    role = request.COOKIES.get('role')
    if role == 'ADMIN':
        return True
    return False