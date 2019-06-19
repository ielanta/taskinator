# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    NEW = 'N'
    PROGRESS = 'P'
    COMPLETED = 'C'
    ARCHIVED = 'A'
    STATUS_TYPES = (
        (NEW, 'new'),
        (PROGRESS, 'in progress'),
        (COMPLETED, 'completed'),
        (ARCHIVED, 'archived'),
    )
    name = models.CharField(max_length=300, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_TYPES, default=NEW)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        permissions = [("archive_task", "Can archive the task")]

    def __str__(self):
        return self.name
