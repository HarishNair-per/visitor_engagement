
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('visitor/', include('visitor.urls', namespace='visitor')),
    path('', include('planner.urls', namespace='planner')), 
    path('', include('users.urls', namespace='users')), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)