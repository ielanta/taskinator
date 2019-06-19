# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from task.models import Task


class TaskListTests(APITestCase):
    url = reverse('task-list')
    data = {'name': 'TestApps', 'description': '-'}

    def test_not_authorized(self):
        # check that not authorized users cannot create task
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check that not authorized users cannot get task list
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_list(self):
        # login as user
        user = User.objects.create_user('username', 'Password123')
        self.client.force_authenticate(user=user)
        # check ability create task
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, self.data['name'])

        # check ability get task list
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.data['name'])


class TaskDetailTests(APITestCase):
    url = reverse('task-detail')
    data = {'name': 'TestApps', 'description': '-'}

    def test_not_authorized(self):
        # check that not authorized users cannot create task
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_archive_permission(self):
        # login as user
        user = User.objects.create_user('username', 'Password123')
        self.client.force_authenticate(user=user)
        self.data['status'] = Task.ARCHIVED
        # check that user cannot
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, self.data['name'])

