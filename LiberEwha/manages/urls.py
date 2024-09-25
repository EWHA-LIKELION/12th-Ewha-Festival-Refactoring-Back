from django.urls import path
from django.conf import settings
from manages.views import *
from booths.models import *
from booths.serializers import *
from booths.views import *

app_name = 'manages'

urlpatterns=[
    path('<int:pk>/guestbook/<int:guestbook_id>/', ReplyManageView.as_view()),
    path('<int:pk>/guestbook/<int:guestbook_id>/<int:reply_id>/', ReplyDeleteView.as_view()),
    path('<int:pk>/realtime_info/', NoticeView.as_view()),
    path('<int:pk>/realtime_info/<int:info_id>/', NoticeDeleteView.as_view()),

]