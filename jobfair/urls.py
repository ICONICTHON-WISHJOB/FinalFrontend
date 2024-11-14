from django.urls import path
from . import views

urlpatterns = [
    path('reserve-booth/<int:booth_id>/', views.ReserveBoothView.as_view(), name='reserve_booth'),
    path('queue-position/<int:booth_id>/', views.CheckQueuePositionView.as_view(), name='check_queue_position'),
    path('boothList/<str:day>/<str:floor>/', views.BoothListView.as_view(), name='booth_list'),
    path('boothApply/', views.BoothApplyView.as_view(), name='booth_apply'),
]