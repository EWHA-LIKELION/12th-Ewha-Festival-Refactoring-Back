from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('search/', SearchView.as_view(), name='search'),
    path('scraps/', ScrapListView.as_view(), name='main_scrap_list'),
]
