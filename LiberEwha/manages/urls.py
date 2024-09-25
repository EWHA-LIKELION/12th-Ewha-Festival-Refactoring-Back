from django.urls import path
from django.conf import settings
from manages.views import *
<<<<<<< HEAD
from booths.models import *
from booths.serializers import *
from booths.views import *
=======
>>>>>>> 6d5a67236863c53451e1f71d2154ced4dd103fcb

app_name = 'manages'

urlpatterns=[
<<<<<<< HEAD
    path('<int:pk>/guestbook/<int:guestbook_id>/', ReplyManageView.as_view()),
    path('<int:pk>/guestbook/<int:guestbook_id>/<int:reply_id>/', ReplyDeleteView.as_view()),
=======
    path('<int:pk>/realtime_info/', NoticeView.as_view()),
    path('<int:pk>/realtime_info/<int:info_id>/', NoticeDeleteView.as_view()),
>>>>>>> 6d5a67236863c53451e1f71d2154ced4dd103fcb

]