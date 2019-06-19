# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from task.models import Task
from task.serializers import TaskSerializer


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class TaskDetail(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            emails = [user.email for user in form.users]
            print(emails)
            send_mail('Update: %s' % form.name,
                      'Task data was updated: %s' % form.to_dict(),
                      DEFAULT_FROM_EMAIL, emails)
        return super(TaskDetail, self).put(request, *args, **kwargs)