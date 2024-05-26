from django.urls import include, path
from . import views

app_name = 'subscription_management'

urlpatterns = [
    path('', views.box_list, name='box_list'),
    path('<int:box_id>/', views.box_detail, name='box_detail'),
    path('history/', views.subscription_history, name='subscription_history'),
    path('subscribe/<int:box_id>/', views.subscribe, name='subscribe'),
    path('cancel/<int:sub_id>/', views.cancel, name='cancel'),

    path('admins/', views.admin_list, name='admin_list'),
    path('admins/cancel/<int:sub_id>/', views.admin_cancel, name='admin_cancel'),
    path('admins/pending/<int:sub_id>/', views.admin_pending, name='admin_pending'),
    path('admins/approve/<int:sub_id>/', views.admin_approve, name='admin_approve'),

    path('fetch_boxes/', views.fetch_boxes, name='fetch_boxes'),
    path('fetch_subscriptions/', views.fetch_subscriptions, name='fetch_subscriptions'),
    path('get_all_subscriptions/', views.get_all_subscriptions, name='get_all_subscriptions')

]