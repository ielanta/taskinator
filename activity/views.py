from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from activity.models import Comment
from activity.serializers import CommentSerializer


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(task__pk=self.kwargs['task_id'])


class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminUser,)
