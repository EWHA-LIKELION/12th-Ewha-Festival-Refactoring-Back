from django.urls import path
from django.conf import settings
from manages.views import *

app_name = 'manages'

urlpatterns=[
    path('<int:booth_id>/menus/', ManageMenuView.as_view()),
    path('<int:booth_id>/menus/<int:menu_id>/', ManageMenuView.as_view()),
    path('<int:pk>/', ManageBoothView.as_view()),
    path('booths/', ManageView.as_view()),
    path('<int:pk>/guestbook/<int:guestbook_id>/', ReplyManageView.as_view()),
    path('<int:pk>/guestbook/<int:guestbook_id>/<int:reply_id>/', ReplyDeleteView.as_view()),
    path('<int:pk>/realtime_info/', NoticeView.as_view()),
    path('<int:pk>/realtime_info/<int:info_id>/', NoticeDeleteView.as_view()),
]