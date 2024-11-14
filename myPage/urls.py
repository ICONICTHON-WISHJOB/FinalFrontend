from django.urls import path
from . import views

urlpatterns = [
    path('api/myPage/<int:userId>/', views.MyPageView.as_view(), name='my_page'),

]