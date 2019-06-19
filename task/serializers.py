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
