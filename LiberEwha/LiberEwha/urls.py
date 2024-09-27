from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    #path('main/', include('main.urls')),
    path('manages/', include('manages.urls')),
    path('booths/', include('booths.urls')),
    path('shows/', include('shows.urls')),
    path('manages/', include('manages.urls')),
    path('notice/', include('notice.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
