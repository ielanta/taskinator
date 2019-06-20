from django.conf.urls import url
from task.views import TaskList, TaskDetail


urlpatterns = [
    url(r'^$', TaskList.as_view(), name='task-list'),
    url(r'^(?P<pk>\d+)/$', TaskDetail.as_view(), name='task-detail'),
]
