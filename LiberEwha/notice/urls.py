from django.urls import path
from .views import NoticeCreateView, NoticeListView, NoticeDetailView

urlpatterns = [
    path('create/', NoticeCreateView.as_view(), name='notice-create'),
    path('list/', NoticeListView.as_view(), name='notice-list'),
    path('list/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]