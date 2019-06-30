from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from task.models import Task


class TaskListTests(APITestCase):
    url = reverse('task-list')
    data = {'name': 'Test Task', 'description': '-'}

    def test_not_authorized(self):
        # check that not authorized users cannot create task
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check that not authorized users cannot get task list
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_list(self):
        # login as user
        user = User.objects.create_user('username', 'Password')
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
    data = {'name': 'Test Task Detail', 'description': '-'}

    def setUp(self):
        self.user = User.objects.create_user('username', 'user@test.com', 'Password')
        self.task, _ = Task.objects.get_or_create(**self.data)
        self.url = reverse('task-detail', kwargs={'pk': self.task.pk})

    def test_not_authorized(self):
        # check that not authorized users cannot create task
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_permission(self):
        archived_task_data = {'name': 'Test Name', 'status': Task.ARCHIVED}
        # login as user
        self.client.force_authenticate(user=self.user)
        # check that user cannot archive the task
        response = self.client.put(self.url, archived_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check that admin can archive the task
        admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=admin)
        response = self.client.put(self.url, archived_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        # login as user
        self.client.force_authenticate(user=self.user)
        self.data['name'] = 'Updated Test Task Name'
        self.assertNotEqual(Task.objects.get(pk=self.task.pk).name, self.data['name'])
        # check that user can update task name
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=self.task.pk).name, self.data['name'])

    def test_email_send(self):
        self.client.force_authenticate(user=self.user)
        add_user_task_data = {'name': 'Test Name', 'users': [self.user.pk]}
        response = self.client.put(self.url, add_user_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), [self.user.email])
        self.assertEqual(mail.outbox[0].subject, 'Update: %s' % add_user_task_data['name'])

        update_user_task_data = {'name': 'Updated Test Name', 'users': [self.user.pk]}
        response = self.client.put(self.url, update_user_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].recipients(), [self.user.email])
        self.assertEqual(mail.outbox[1].subject, 'Update: %s' % update_user_task_data['name'])
