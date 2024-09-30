from django.urls import path
from .views import MainPageView, SearchView

app_name = 'main'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('search/', SearchView.as_view(), name='search'),
]