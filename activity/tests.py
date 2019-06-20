# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from activity.models import Comment
from task.models import Task


class CommentListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'Password')
        task, _ = Task.objects.get_or_create()
        self.url = reverse('comment-list', kwargs={'task_id': task.pk})
        self.data = {'text': 'My Comment', 'task': task.pk}

    def test_not_authorized(self):
        # check that not authorized users cannot create comment
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check that not authorized users cannot get comment list
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_list(self):
        # login as user
        self.client.force_authenticate(user=self.user)
        # check ability create comment
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().text, self.data['text'])

        # check ability get comment list
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], self.data['text'])


class CommentDeleteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'Password')
        task, _ = Task.objects.get_or_create()
        self.comment, _ = Comment.objects.get_or_create(task=task, user=self.user, text='My text')
        self.url = reverse('comment-delete', kwargs={'task_id': task.pk, 'pk': self.comment.pk})

    def test_delete(self):
        # check that unauthorised can't delete comment
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check that user can't delete comment
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check that admin can delete comment
        admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=admin)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

