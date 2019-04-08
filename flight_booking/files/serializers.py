from rest_framework import serializers
from .models import File
import os

MAX_UPLOAD_SIZE = 2621440
# change to settings
# from django.conf import settings


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'user': {'write_only': True}
        }

        fields = [
            'id',
            'file',
            'user',
        ]

        model = File

    def validate(self, data):
        file_ = data['file']
        ext = os.path.splitext(file_.name)[1]
        valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError(u'Unsupported file extension.')
        if file_.size > MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(u'File size must not exceed 2MB ')
        return data

