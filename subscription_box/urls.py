from django.urls import path
from .views import *

app_name = 'subscription_box'

urlpatterns = [
    path('', manager, name='manager'),
    path('box/create', create_subscription, name='create_subscription'),
    path('box/update/<int:id>', update_subscription, name='update_subscription'),
    path('box/delete/<int:id>', delete_subscription, name='delete_subscription'),
    path('item/create', create_item, name='create_item'),
    path('item/update/<int:id>', update_item, name='update_item'),
    path('item/delete/<int:id>', delete_item, name='delete_item'),
    path('box/get/<int:id>', view_subscriptions , name='get_subscription'),
    path('item/get/<int:id>', view_items, name='get_items'),
    path('box/get', get_subscription_ajax, name='all_subscriptions'),
    path('item/get', get_item_ajax, name='all_items'),
]