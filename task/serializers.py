from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'name', 'status', 'description', 'users')

    def validate_status(self, value):
        if value == Task.ARCHIVED and not self.context['request'].user.has_perm('archive_task'):
            raise serializers.ValidationError("You don't have permission to archive task")
        return value


class TaskDetailSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ('name', 'status', 'description', 'users')

    def save(self):
        if self.validated_data.get('users'):
            emails = [user.email for user in self.validated_data.get('users')]
            send_mail('Update: %s' % self.validated_data.get('name'),
                      'Task data was updated: %s' % str(self.validated_data),
                      DEFAULT_FROM_EMAIL, emails)
        return super(TaskDetailSerializer, self).save()
