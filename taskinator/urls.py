from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^tasks/', include('task.urls')),
    url(r'^tasks/(?P<task_id>\d+)/comments/', include('activity.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'))
]
