from django.urls import path
from django.conf import settings
from shows.views import *

app_name = 'shows'

urlpatterns=[
    path('main/', ShowsMainView.as_view()),
    path('<int:pk>/', ShowsDetailView.as_view()),

]