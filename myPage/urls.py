from django.urls import path
from . import views

urlpatterns = [
    path('api/myPage/<int:userId>/', views.MyPageView.as_view(), name='my_page'),
    path('api/myPage/<int:userId>/interest/', views.MyPageInterestView.as_view(), name='my_page_interest'),
    path('api/myPage/reservationList/<int:userId>/<int:doneType>/', views.ReservationListView.as_view(), name='my_page_interest'),
    path('myPage/api/myPage/interest/new', views.UpdateInterestCategoriesView.as_view(), name='my_page_interest'),
    path('api/myPage/reservationList/remove/<int:userId>/<int:boothID>/', views.RemoveReservationView.as_view(), name='my_page_interest'),
    path('api/myPage/resume/<int:userId>/', views.ResumeView.as_view(), name='my_page_interest'),

]