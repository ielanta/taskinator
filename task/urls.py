from django.conf.urls import url

from task.views import TaskList, TaskDetail


urlpatterns = [
    url(r'^$', TaskList.as_view(), name='task-list'),
    url(r'^<int:pk>/$', TaskDetail.as_view(), name='task-detail'),
]
