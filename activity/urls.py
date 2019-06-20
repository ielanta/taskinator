from django.conf.urls import url
from activity.views import CommentList, CommentDelete


urlpatterns = [
    url(r'^$', CommentList.as_view(), name='comment-list'),
    url(r'^(?P<pk>\d+)/$', CommentDelete.as_view(), name='comment-delete'),
]
