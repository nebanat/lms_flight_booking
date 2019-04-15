from django.conf import settings
from rest_framework import serializers
from .models import File
import os


class FileSerializer(serializers.ModelSerializer):
    """
      file serializer
    """
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
        """
        validate uploaded file
        -----------------
        maximum picture size: 2MB
        only pictures

        :param data:
        :return:
        """
        max_upload_size = settings.MAX_UPLOAD_SIZE
        file_ = data['file']
        ext = os.path.splitext(file_.name)[1]
        valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError(u'Unsupported file extension.')
        if file_.size > max_upload_size:
            raise serializers.ValidationError(u'File size must not exceed 2MB ')
        return data

