from django.urls import path
from . import views

urlpatterns = [
    path('waitCnt/<int:id>', views.WaitCountView.as_view(), name='wait_count'),
    path('waitList/<int:id>', views.WaitListView.as_view(), name='wait_list'),
]
