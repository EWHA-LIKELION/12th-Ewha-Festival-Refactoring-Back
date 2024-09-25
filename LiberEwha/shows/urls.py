from django.urls import path
from django.conf import settings
from booths.views import BoothScrapView

app_name = 'shows'

urlpatterns=[
    path('<int:pk>/scrap/', BoothScrapView.as_view()),

]