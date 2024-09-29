from django.urls import path
from .views import MainPageView, SearchView, ScrapListView

urlpatterns = [
    path('main/', MainPageView.as_view(), name='main_page'),
    path('scraps/', ScrapListView.as_view(), name='scrap_list'),
    path('search/', SearchView.as_view(), name='search'),
]
