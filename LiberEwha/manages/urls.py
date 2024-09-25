from django.urls import path
from django.conf import settings
from manages.views import *

app_name = 'manages'

urlpatterns=[
    path('<int:booth_id>/menus/', ManageMenuView.as_view()),
    path('<int:booth_id>/menus/<int:menu_id>/', ManageMenuView.as_view()),
    path('<int:pk>/', ManageBoothView.as_view()),
    path('booths/', ManageView.as_view()),
]