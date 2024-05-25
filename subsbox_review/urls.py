from django.urls import include, path
from subsbox_review.views import get_all_reviews

app_name = 'subsbox_review'

urlpatterns = [
    path('', get_all_reviews, name='review_list'),
]