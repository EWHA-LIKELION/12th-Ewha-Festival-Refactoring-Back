from django.urls import path
from django.conf import settings
from manages.views import *

app_name = 'manages'

urlpatterns=[
    path('<int:pk>/realtime_info/', NoticeView.as_view()),
    path('<int:pk>/realtime_info/<int:info_id>/', NoticeDeleteView.as_view()),

]