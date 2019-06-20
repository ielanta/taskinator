# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from task.models import Task
from task.serializers import TaskSerializer, TaskDetailSerializer


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class TaskDetail(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated,)

