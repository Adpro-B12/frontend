from django.urls import include, path
from subsbox_review.views import get_all_reviews, create_review

app_name = 'subsbox_review'

urlpatterns = [
    path('', get_all_reviews, name='review_list'),
    path('create_review', create_review, name='create_review'),
]