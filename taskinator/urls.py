from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^tasks/', include('task.urls')),
    url(r'^admin/', admin.site.urls),
]